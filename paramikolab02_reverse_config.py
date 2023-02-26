import os
import threading
import time

import paramiko

USERNAME = 'admin'


class Device:
    ip: str
    key_file: str
    cmds: list[str]

    def __init__(self, name, ip, key_file=os.path.expanduser("~/.ssh/id_rsa"), cmds=None):
        if cmds is None:
            cmds = []
        self.name = name
        self.ip = ip
        self.key_file = key_file
        self.cmds = cmds
        self.cmds.insert(0, "conf t")

    def exec(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.ip, username=USERNAME, key_filename=self.key_file,
                       look_for_keys=False)
        print("Connecting to {} {} ...".format(self.name, self.ip))

        def send(c: str, read_output=False) -> str:
            print("Sending cmd {} -> {}".format(c, self.name))
            ssh.send(bytes(c + "\n", 'ascii'))
            time.sleep(1)
            return ssh.recv(1000).decode('ascii')

        with client.invoke_shell() as ssh:
            print("Connected to {} {} ...".format(self.name, self.ip))
            send("terminal length 0")
            for cmd in self.cmds:
                send(cmd)
            print(send("do sh ip int br", read_output=True))


devices = [
    Device("R1", '172.31.111.4', cmds=[
        "no access-list 1",
        "no ip access-list extended block-management",
        "no router ospf 1",
        "int g0/1",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat inside",
        "shut",
        "int g0/2",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat outside",
        "no ip nat outside",
        "no ip nat inside source list 1 int g0/2 vrf control-data overload",
    ]),
    Device("R2", '172.31.111.5', cmds=[
        "no access-list 1",
        "no ip access-list extended block-management",
        "no router ospf 1",
        "int g0/1",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat inside",
        "shut",
        "int g0/2",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat outside",
        "no ip nat outside",
        "no ip nat inside source list 1 int g0/2 vrf control-data overload",
    ]),
    Device("R3", '172.31.111.6', cmds=[
        "no access-list 1",
        "no ip access-list extended block-management",
        "no router ospf 1",
        "int g0/1",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat inside",
        "shut",
        "int g0/2",
        "no ip address",
        "no ip access-group block-management in",
        "no ip nat outside",
        "no ip nat outside",
        "no ip nat inside source list 1 int g0/2 vrf control-data overload",
        "yes",
    ])
]

threads = list()

for device in devices:
    x = threading.Thread(target=device.exec)
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()
