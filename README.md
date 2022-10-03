# simba

Tool used to interact with SMB shares.

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
