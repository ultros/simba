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

    parser.add_argument('--remote_name', required=True, type=str,
                        dest='remote_name',
                        help='Specify target ipaddress')

    parser.add_argument('-t', '--target_system_name', required=True, type=str,
                        dest='target_system_name',
                        help='Specify the system name (E.g. laptop01) to connect to.')

    parser.add_argument("--pdf", required=False, type=str,
                        default=None, dest="pdf",
                        help='Specify PDF report name')

    args = parser.parse_args()

    ip = args.ip
    port = args.port
    username = args.username
    password = args.password
    remote_name = args.remote_name
    target_system_name = args.target_system_name

    smb_client = smb_tools.SmbTools(ip, port, username, password, remote_name, target_system_name)
    smb_client.smb_connect()
    smb_client.smb_list_shares()

    while True:
        print("smb > ", end="")
        command = input()

        if command == "help":
            print(f"    Commands:")
            print(f"    shares (list service names/shares)")
            print(f"    use SERVICE_NAME (connect to specified service name/share)")
            print(f"    username (get username)")
            print(f"    password (get password)")
            print(f"    remote_name (get remote_name)")
            print(f"    target_system_name (get target system name)")

        if command == "username":
            print(smb_client.username)

        if command == "password":
            print(smb_client.password)

        if command == "remote_name":
            print(smb_client.remote_name)

        if command == "target_system_name":
            print(smb_client.target_system_name)

        if command == "connect":
            smb_client.smb_connect()

        if command == "disconnect":
            smb_client.smb_disconnect()

        if command == "shares":
            smb_client.smb_list_shares()

        if command == "exit":
            smb_client.smb_disconnect()
            exit(0)

        if command[0:4] == "use ":
            service_name = command[4:]

            while True:
                print(f"[{service_name}] > ", end = "")
                command = input()

                if command == "exit":
                    print("Disconnecting from service...")
                    break

                if command[:2] == "ls":
                    try:
                        smb_client.smb_list_files(service_name, command[3:]) # ls /TO/PATH
                    except smb.SMBConnection.NotReadyError as e:
                        print(e)

                if command[:8] == "download":
                    download_command = command.split(" ", 3)
                    smb_client.smb_download_file(service_name,
                                                 download_command[1],
                                                 download_command[2]) # download REMOTE_FILE LOCAL_DEST

                if command[:6] == "upload":
                    upload_command = command.split(" ", 3)
                    smb_client.smb_upload_file(service_name, upload_command[1], upload_command[2])

                if command == "help":
                    print("   Commands:")
                    print("   ls PATH (list files and directories)")
                    print("   download REMOTE_FILE LOCAL_FILE")
                    print("   upload LOCAL_FILE REMOTE_FILE")
                    print("   exit (exit to main menu)")


if __name__ == '__main__':
    main()
