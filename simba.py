#!/usr/bin/env python3

import smb_tools
import argparse


def main():

    parser = argparse.ArgumentParser(description="simba - tools for working with SMB")

    parser.add_argument('-p', '--port', required=True, type=int,
                        default=445, dest="port",
                        help='Specify port to connect to (default: 445).')

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

    parser.add_argument('-d', '--domain', required=True, type=str,
                        dest='domain',
                        help='Specify domain name of target IP address.')

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
    domain = args.domain

    smb_client = smb_tools.SmbTools(ip, port, username, password, remote_name, domain)
    smb_client.smb_connect()
    smb_client.smb_list_shares()

    while True:
        print("smb > ", end="")
        command = input()

        match command:
            case "help":
                print("Commands:")
                print("  smb > connect")
                print("  smb > disconnect")
                print("  smb > shares")
                print("  smb > ls")
                print("  smb > username")
                print("  smb > password")

            case "username":
                print(smb_client.smb_connect_username())

            case "password":
                print(smb_client.smb_connect_password())

            case "connect":
                smb_client.smb_connect()

            case "disconnect":
                smb_client.smb_disconnect()

            case "shares":
                smb_client.smb_list_shares()

            case "ls":
                print("[ls] > Enter service name (share name e.g. C$): ", end="")
                service_name = input()

                while True:
                    print(f"[{service_name}] > Enter share path (e.g. \\abc\\def): ", end="")
                    share_path = input()

                    if share_path == "help":
                        print("ls - List files and directories")
                        print("download filename - Download a file from share")
                        print("exit - Exit to main menu")

                    if share_path == "exit":
                        break

                    if share_path[:2] == "ls":
                        smb_client.smb_list_files(service_name, share_path[4:])

                    if share_path[:8] == "download":
                        smb_client.smb_download_file(service_name, share_path[10:])

                    # if share_path[:2] == "cd":
                    #     working_directory = share_path[10:]
                    #     smb_client.smb_working_directory(service_name, working_directory)

            case "exit":
                print("Closing application...")
                smb_client.smb_disconnect()
                exit(0)

if __name__ == '__main__':
    main()
