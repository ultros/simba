# simba
Tools used to interact with SMB shares.

$ ./simba.py -i 10.10.10.10 -p 139 --username billy --password P@ssw0rd --remote_name 'PC01' --domain PC01  
[+] Connected  
[10.10.10.10 - PC01]    
ADMIN$    
C$  
Backup  

...

$ smb > cd  
$ [cd] > Enter service name (share name e.g. C$):  c$

...

[c$] > Enter command and path (e.g. command \abc\def): ls tools  
.  
..  
CyberChef_v9.37.3  
getip.exe  
hashcat-6.2.5