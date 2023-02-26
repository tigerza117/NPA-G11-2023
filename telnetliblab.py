import getpass
import telnetlib
import time

host = "172.31.111.4"
user = input("Enter username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host, 23, 5)

tn.read_until(b"Username:")
tn.write(user.encode('ascii') + b"\n")
time.sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
time.sleep(1)


def send(cmd):
    tn.write(bytes("%s\n" % cmd, 'ascii'))
    time.sleep(2)


send("conf t")
send("int gi0/1")
send("ip address 172.31.111.17 255.255.255.240")
send("no shut")
send("exit")
send("exit")
send("show ip int br")

output = tn.read_very_eager()
print(output.decode('ascii'))
tn.close()
