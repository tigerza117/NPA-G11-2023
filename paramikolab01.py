import time

import paramiko

USERNAME = 'admin'
PASSWORD = 'cisco'

devices_ip = ['172.31.111.4', '172.31.111.5', '172.31.111.6']

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, password=PASSWORD, look_for_keys=False)

    commands = ['sh ip int br']
    for cmd in commands:
        print("Executing {}".format(cmd))
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print("Errors")
        print(stderr.read().decode())
        time.sleep(1)
    client.close()
