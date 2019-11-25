#Anthony tang


import getpass
import sys
import telnetlib

hostname = "192.168.255.200"
user = "FSW50-103349\\Instrument"
password = "894129"

tn = telnetlib.Telnet(hostname)
print("telnet")

tn.read_until("login: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("ls\n")
tn.write("exit\n")

print (tn.read_all())
