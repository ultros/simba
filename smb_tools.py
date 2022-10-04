import ntpath
import os

import smb.smb_structs
from smb.SMBConnection import SMBConnection
from nmb.NetBIOS import NetBIOS


class SmbTools(object):
    def __init__(self, ip: str, port: int, username: str, password: str, remote_name: str, target_system_name: str):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.remote_name = remote_name
        self.target_system_name = target_system_name
        self.smb_connection = ""

    def smb_connect(self):
        try:
            print(f"[+] Automatically querying for NetBIOS name...")
            netbios = NetBIOS()
            netbios_name = netbios.queryIPForName(self.ip, port=137, timeout=5)
            if netbios_name is None:
                print("[!] Could not determine system target (NetBIOS Name) automatically...")
                print("[+] Try using nmap to get NetBIOS name (target system name):\n "
                      "nmap --script smb-os-discovery.nse -p445 10.10.10.10")
            else:
                print(f'[+] Target system name: "{netbios_name[0]}" discovered.')
                self.target_system_name = netbios_name[0]
            netbios.close()

            smb_connection = SMBConnection(self.username, self.password,
                                           self.remote_name, self.target_system_name, use_ntlm_v2=True)
            if smb_connection.connect(self.ip, self.port):
                self.smb_connection = smb_connection
                print("[+] Connected")

            else:
                print("[!] Failed to connect...")

        except Exception as e:
            #print(e)
            pass

    def smb_disconnect(self):
        try:
            self.smb_connection.close()
            print("[+] Disconnected")
        except Exception as e:
            print(e)

    def smb_list_shares(self):
        try:
            print(f"[{self.ip} - {self.target_system_name}]")
            for share in self.smb_connection.listShares():
                print(share.name)
        except Exception as e:
            print(f"[!] Failed to connect...")

    def smb_download_file(self, service_name: str, source: str, destination: str):
        try:
            if os.path.isdir(destination):
                destination_file = f"{destination}/{ntpath.basename(source)}"
            else:
                destination_file = destination

            with open(destination_file, 'wb') as file_obj:
                response = self.smb_connection.retrieveFile(service_name, source, file_obj)
                print(f"[+] {response[1]} bytes downloaded")

        except smb.smb_structs.OperationFailure:
            print(f"[!] Unable to open file (permissions)")
            print(f"[!] Erasing empty local file...")
            os.remove(destination)
        except TypeError:
            print(f"[!] Source file does not exist or permissions error")
        except IsADirectoryError:
            print(f"[!] Specify full path including destination file name.")


    def smb_upload_file(self, service_name: str, local_file: str, share_path: str):
        try:
            if share_path[-1:] == "/":
                destination_file = f"{share_path}{ntpath.basename(local_file)}"
            else:
                destination_file = share_path

            with open(local_file, 'rb') as file_obj:
                print(f"[+] {self.smb_connection.storeFile(service_name, destination_file, file_obj)} bytes uploaded!")
        except FileNotFoundError:
            print("[!] Source file does not exist at specified path!")
        except smb.smb_structs.OperationFailure:
            print(f"[!] Failed to store on {service_name}: Unable to open file")

    def smb_list_files(self, service_name: str, share_path="\\"):
        try:
            files_folders = self.smb_connection.listPath(service_name, share_path, 65591, '*', 30)

            for item in files_folders:
                print(f"{item.filename}")

        except smb.smb_structs.OperationFailure:
            print(f"Failed to list {service_name} {share_path}: Verify path "
                  f"(E.g. \directory\pathtofile.exe) OR PERMISSIONS")
