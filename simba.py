#!/usr/bin/env python3
import argparse
import smb.SMBConnection
import smb_tools


def main():
    parser = argparse.ArgumentParser(description="simba - tool for working with SMB")

    parser.add_argument('-p', '--port', required=True, type=int,
                        default=139, dest="port",
                        help='Specify port to connect to (default: 139).')

    parser.add_argument('-i', '--ip', required=True, type=str,
                        dest="ip",
                        help='Specify IP to connect to.')

    parser.add_argument('--username', required=False, type=str,
                        dest='username',
                        help='Specify Account Username')

    parser.add_argument('--password', required=False, type=str,
                        dest='password',
                        help='Specify Account Password')

    parser.add_argument('--remote_name', required=False, type=str,
                        dest='remote_name',
                        help='Specify target ipaddress')

    parser.add_argument('-t', '--target_system', required=True, type=str,
                        dest='target_system',
                        help='Specify the system name (E.g. laptop01) to connect to.')

    parser.add_argument("--html", required=False, type=str,
                        default=None, dest="html",
                        help='Specify HTML report name')

    parser.add_argument("--pdf", required=False, type=str,
                        default=None, dest="pdf",
                        help='Specify PDF report name')

    args = parser.parse_args()

    ip = args.ip
    port = args.port
    username = args.username
    password = args.password
    remote_name = args.remote_name
    target_system = args.target_system

    smb_client = smb_tools.SmbTools(ip, port, username, password, remote_name, target_system)
    smb_client.smb_connect()
    smb_client.smb_list_shares()

    while True:
        print("smb > ", end="")
        command = input()

        match command:
            case "help":
                print("Commands:")
                print("  smb > connect (connect session)")
                print("  smb > disconnect (disconnect session)")
                print("  smb > shares (list all shares)")
                print("  smb > use (specify service/share name)")
                print("  smb > username (retrieve login username)")
                print("  smb > password (retrieve login password)")

            case "username":
                print(smb_client.username)

            case "password":
                print(smb_client.password)

            case "connect":
                smb_client.smb_connect()

            case "disconnect":
                smb_client.smb_disconnect()

            case "shares":
                smb_client.smb_list_shares()

            case "use":
                print("[smb > use] > Enter service name (share name e.g. test-share): ", end="")
                service_name = input()
                while True:
                    print(f"[{service_name}] > Enter command and path (e.g. command \\abc\\def): ", end="")
                    share_path = input()

                    if share_path == "help":
                        print("ls (list files and directories)")
                        print("download filename (download the specified file)")
                        print("upload (specify a file to copy and the destination path on the service/share name)")
                        print("exit (exit to main menu)")

                    if share_path == "exit":
                        break

                    if share_path[:2] == "ls":
                        try:
                            smb_client.smb_list_files(service_name, share_path[3:])
                        except smb.SMBConnection.NotReadyError as e:
                            print(e)

                    if share_path[:8] == "download":
                        smb_client.smb_download_file(service_name, share_path[9:])

                    if share_path[:6] == "upload":
                        print("Type full path to local file: ", end='')
                        local_file = input()
                        print("Type full path to the remote file destination: ", end='')
                        share_path = input()

                        smb_client.smb_upload_file(service_name, local_file, share_path)

            case "exit":
                print("[!] Closing application...")
                smb_client.smb_disconnect()
                exit(0)


if __name__ == '__main__':
    main()
