# simba

Tool used to interact with SMB shares.

smb > help  
Commands:

    shares (list service names/shares)  
    use SERVICE_NAME (connect to specified service name/share)  
    username (get username)  
    password (get password)  
    remote_name (get remote_name)  
    domain_name (get system domain name)  

smb > use test-share  
[test-share] > help

    ls PATH (list files and directories)  
    download REMOTE_FILENAME LOCAL_FILENAME    
    upload LOCAL_FILE REMOTE_FILE  
    exit (exit to main menu)

---

$ ./simba.py -i 192.168.254.100 -p 139 --username john --password P@ssw0rd --remote_name '' -t dc

    [+] Connected  
    [192.168.254.100 - dc]  
    ADMIN$  
    C$  
    IPC$  
    NETLOGON  
    SYSVOL  
    test-share

$ smb > use test-share

    $ [test-share] > ls  
    .  
    ..  
    .hidden.txt  
    test.txt

$ [test-share] > download test.txt /tmp/tempfile.txt

    15 bytes downloaded!

$ [test-share] > upload /tmp/tempfile.txt /directory/test22.txt

    15 bytes uploaded!  

$ smb > exit

    [+] Closing application...  
    [+] Disconnected  
