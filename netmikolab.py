import os
import re

from netmiko import ConnectHandler

params = {
    'device_type': 'cisco_ios',
    'ip': '0.0.0.0',
    'username': 'admin',
    'key_file': os.path.expanduser("~/.ssh/id_rsa"),
}

devices_config = {
    "R1": {
        "mgmt_ip": "172.31.111.4",
        "cmds": [
            "int G0/0",
            "description Connect to G0/2 of S0",
            "int G0/1",
            "description Connect to G0/2 of S1",
            "int G0/2",
            "description Connect to G0/1 of R2",
            "int G0/3",
            "description Not Use",
            "do wr"
        ],
        "tests": {
            "iface_ip": [
                ("G0/0", "172.31.111.4"),
                ("G0/1", "172.31.111.17"),
                ("G0/2", "172.31.111.34"),
                ("G0/3", "unassigned"),
            ],
            "iface_subnet": [
                ("G0/0", "255.255.255.240"),
                ("G0/1", "255.255.255.240"),
                ("G0/2", "255.255.255.240"),
                ("G0/3", "no ip address"),
            ],
            "iface_description_and_stat": [
                ("G0/0", ("Connect to G0/2 of S0", ("up", "up"))),
                ("G0/1", ("Connect to G0/2 of S1", ("up", "up"))),
                ("G0/2", ("Connect to G0/1 of R2", ("up", "up"))),
                ("G0/3", ("Not Use", ("admin down", "down")))
            ],
        }
    },
    "R2": {
        "mgmt_ip": "172.31.111.5",
        "cmds": [
            "int G0/0",
            "description Connect to G0/3 of S0",
            "int G0/1",
            "description Connect to G0/2 of R1",
            "int G0/2",
            "description Connect to G0/1 of R3",
            "int G0/3",
            "description Not Use",
            "do wr"
        ],
        "tests": {
            "iface_ip": [
                ("G0/0", "172.31.111.5"),
                ("G0/1", "172.31.111.33"),
                ("G0/2", "172.31.111.50"),
                ("G0/3", "unassigned"),
            ],
            "iface_subnet": [
                ("G0/0", "255.255.255.240"),
                ("G0/1", "255.255.255.240"),
                ("G0/2", "255.255.255.240"),
                ("G0/3", "no ip address"),
            ],
            "iface_description_and_stat": [
                ("G0/0", ("Connect to G0/3 of S0", ("up", "up"))),
                ("G0/1", ("Connect to G0/2 of R1", ("up", "up"))),
                ("G0/2", ("Connect to G0/1 of R3", ("up", "up"))),
                ("G0/3", ("Not Use", ("admin down", "down")))
            ],
        }
    },
    "R3": {
        "mgmt_ip": "172.31.111.6",
        "cmds": [
            "int G0/0",
            "description Connect to G1/0 of S0",
            "int G0/1",
            "description Connect to G0/2 of R2",
            "int G0/2",
            "description Connect to WAN",
            "int G0/3",
            "description Not Use",
            "do wr"
        ],
        "tests": {
            "iface_ip": [
                ("G0/0", "172.31.111.6"),
                ("G0/1", "172.31.111.49"),
                ("G0/3", "unassigned"),
            ],
            "iface_subnet": [
                ("G0/0", "255.255.255.240"),
                ("G0/1", "255.255.255.240"),
                ("G0/2", "dhcp"),
                ("G0/3", "no ip address"),
            ],
            "iface_description_and_stat": [
                ("G0/0", ("Connect to G1/0 of S0", ("up", "up"))),
                ("G0/1", ("Connect to G0/2 of R2", ("up", "up"))),
                ("G0/2", ("Connect to WAN", ("up", "up"))),
                ("G0/3", ("Not Use", ("admin down", "down")))
            ],
        }
    },
}


def get_data_from_device(device_params, cmd):
    with ConnectHandler(**device_params) as ssh:
        result_cmd = ssh.send_command(cmd)
        return result_cmd


def get_ip(device_params, iface):
    data = get_data_from_device(device_params, 'sh ip int br {}'.format(iface))
    return re.search(r'(\d+.\d+.\d+.\d+|unassigned)', data)[0]


def get_subnet(device_params, iface):
    data = get_data_from_device(device_params, "sh run int {}".format(iface))
    for line in data.strip().split("\n"):
        if len(line) > 0 and line[0] != " ":
            continue
        line = line.strip()
        intf_subnet = re.search(r"(\d+\.\d+\.\d+\.\d+$|dhcp|no ip address)", line)
        if intf_subnet is not None:
            intf_subnet = intf_subnet.group(0)
            return intf_subnet


def get_iface_stat(device_params, iface):
    data = get_data_from_device(device_params, "sh int {} description".format(iface))
    lines = data.strip().split('\n')
    intf_data = re.search(r"(up|admin down)\s+(up|down)\s+(.+)", lines[1])
    status, status_proto, desc = intf_data.groups()
    return desc, (status, status_proto)


if __name__ == '__main__':
    for value in devices_config.values():
        with ConnectHandler(**dict(params, ip=value["mgmt_ip"])) as ssh:
            result = ssh.send_config_set(value["cmds"])
            print(result)
