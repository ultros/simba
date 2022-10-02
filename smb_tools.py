from smb.SMBConnection import SMBConnection
import ntpath


class SmbTools(object):
    def __init__(self, ip: str, port: int, username: str, password: str, remote_name: str, domain: str):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.remote_name = remote_name
        self.domain = domain
        self.smb_connection = ""


    def smb_connect(self):
        try:
            smb_connection = SMBConnection(self.username, self.password,
                                           self.remote_name, self.domain, use_ntlm_v2=True)
            if smb_connection:
                smb_connection.connect(self.ip, self.port)
                self.smb_connection = smb_connection

            else:
                print("Failed to connect...")

        except Exception as e:
            print(e)

    def smb_disconnect(self):
        try:
            self.smb_connection.close()
        except Exception as e:
            print(e)

    def smb_list_shares(self):
        try:
            print(f"[{self.ip} - {self.remote_name}]")
            for share in self.smb_connection.listShares():
                print(share.name)
        except Exception as e:
            print(e)

    def smb_download_file(self, service_name, share_path):
        try:
            with open(ntpath.basename(share_path[10:]), 'wb') as file_obj:
                self.smb_connection.retrieveFile(service_name, share_path, file_obj)
        except Exception as e:
            print(e)

    def smb_list_files(self, service_name, share_path="\\"):
        try:
            folders = self.smb_connection.listPath(service_name, share_path, 0x10)
            files = self.smb_connection.listPath(service_name, share_path)

            for folder in folders:
                print(f"[DIR] {folder.filename}")

            for file in files:
                print(f"[FILE] {file.filename}")

        except Exception as e:
            print(e)

    def smb_connect_username(self):
        '''Returns currently logged in user.'''
        return self.username

    def smb_connect_password(self):
        '''Returns logged in user password.'''
        return self.password