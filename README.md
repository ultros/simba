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

$ smb > use  
$ [smb > use] > Enter service name (share name e.g. test-share): test-share  
$ [test-share] > Enter command and path (e.g. command \abc\def): ls  
.  
..  
.hidden.txt  
test.txt

$ [test-share] > Enter command and path (e.g. command \abc\def): download test.txt    
15 bytes downloaded!

$ [test-share] > Enter command and path (e.g. command \abc\def): upload  
Type full path to local file: /tmp/test.txt  
Type full path to the remote file destination: test22.txt  
15 bytes uploaded!  

$ smb > exit  
[+] Closing application...  
[+] Disconnected  
