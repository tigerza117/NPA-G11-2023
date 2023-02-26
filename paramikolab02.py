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
        pre_cmd = [
            "ip access-list extended block-management",
            "deny tcp any any eq 22",
            "deny tcp any any eq 23",
            "permit ip any any",
        ]
        self.cmds.insert(0, "conf t")
        self.cmds[1:1] = pre_cmd
        self.cmds.append("do write")

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
        "int gi0/1",
        "ip access-group block-management in",
        "ip add 172.31.111.17 255.255.255.240",
        "no shut",
        "int gi0/2",
        "ip access-group block-management in",
        "ip add 172.31.111.34 255.255.255.240",
        "no shut",
        "exit",
        "router ospf 1 vrf control-data",
        "router-id 1.1.1.1",
        "network 172.31.111.16 0.0.0.15 area 0",
        "network 172.31.111.32 0.0.0.15 area 0",
        "network 1.1.1.1 0.0.0.0 area 0",
    ]),
    Device("R2", '172.31.111.5', cmds=[
        "int g0/1",
        "ip access-group block-management in",
        "ip add 172.31.111.33 255.255.255.240",
        "no shut",
        "int g0/2",
        "ip access-group block-management in",
        "ip add 172.31.111.50 255.255.255.240",
        "no shut",
        "exit",
        "router ospf 1 vrf control-data",
        "router-id 2.2.2.2",
        "network 172.31.111.32 0.0.0.15 area 0",
        "network 172.31.111.48 0.0.0.15 area 0",
        "network 2.2.2.2 0.0.0.0 area 0",
    ]),
    Device("R3", '172.31.111.6', cmds=[
        "int g0/1",
        "ip access-group block-management in",
        "ip add 172.31.111.49 255.255.255.240",
        "ip nat inside",
        "no shut",
        "int g0/2",
        "ip access-group block-management in",
        "ip add dhcp",
        "ip nat outside",
        "no shut",
        "exit",
        "ip route vrf control-data 0.0.0.0 0.0.0.0 dhcp",
        "router ospf 1 vrf control-data",
        "router-id 3.3.3.3",
        "network 172.31.111.48 0.0.0.15 area 0",
        "network 3.3.3.3 0.0.0.0 area 0",
        "default-information originate",
        "access-list 1 permit 172.31.111.16 0.0.0.15",
        "access-list 1 permit 172.31.111.32 0.0.0.15",
        "access-list 1 permit 172.31.111.48 0.0.0.15",
        "ip nat inside source list 1 int g0/2 vrf control-data overload",
    ])
]

threads = list()

for device in devices:
    x = threading.Thread(target=device.exec)
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()
