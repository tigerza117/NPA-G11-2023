import os
import time

import paramiko

USERNAME = 'admin'
PASSWORD = 'cisco'

devices_ip = ['172.31.111.4', '172.31.111.5', '172.31.111.6']

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, key_filename=os.path.expanduser("~/.ssh/id_rsa"),
                   look_for_keys=False)
    print("Connecting to {} ...".format(ip))
    with client.invoke_shell() as ssh:
        print("Connected to {} ...".format(ip))

        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("sh ip int br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)
