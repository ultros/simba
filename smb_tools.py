import ntpath
import os

import smb.smb_structs
from smb.SMBConnection import SMBConnection


class SmbTools(object):
    def __init__(self, ip: str, port: int, username: str, password: str, remote_name: str, target_name: str):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.remote_name = remote_name
        self.target_name = target_name
        self.smb_connection = ""

    def smb_connect(self):
        try:
            smb_connection = SMBConnection(self.username, self.password,
                                           self.remote_name, self.target_name, use_ntlm_v2=True)
            if smb_connection.connect(self.ip, self.port):
                self.smb_connection = smb_connection
                print("[+] Connected")

            else:
                print("[!] Failed to connect...")

        except Exception as e:
            print(e)

    def smb_disconnect(self):
        try:
            self.smb_connection.close()
            print("[+] Disconnected")
        except Exception as e:
            print(e)

    def smb_list_shares(self):
        try:
            print(f"[{self.ip} - {self.target_name}]")
            for share in self.smb_connection.listShares():
                print(share.name)
        except Exception as e:
            print(f"[!] Failed to connect...")

    def smb_download_file(self, service_name, share_path):
        try:
            with open(ntpath.basename(share_path), 'wb') as file_obj:
                print(
                    f"[+] {self.smb_connection.retrieveFile(service_name, share_path, file_obj)[1]} bytes downloaded!")

        except Exception as e:
            # print(e)
            print(f"[!] File ({service_name} {share_path}) does not exist at provided path...")
            print(f"[!] Removing empty file ({service_name} {share_path}) from local file system...")
            os.remove(share_path)

    def smb_upload_file(self, service_name: str, local_file: str, share_path: str):
        try:
            with open(local_file, 'rb') as file_obj:
                print(f"[+] {self.smb_connection.storeFile(service_name, share_path, file_obj)} bytes uploaded!")
        except FileNotFoundError:
            print("[!] Source file does not exist at specified path!")

    def smb_list_files(self, service_name, share_path="\\"):
        try:
            files_folders = self.smb_connection.listPath(service_name, share_path, 65591, '*', 30)

            for item in files_folders:
                print(f"{item.filename}")


        except smb.smb_structs.OperationFailure:
            print(f"Failed to list {service_name} {share_path}: Verify path "
                  f"(E.g. \directory\pathtofile.exe) OR PERMISSIONS")
