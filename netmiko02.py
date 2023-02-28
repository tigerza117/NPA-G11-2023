import os

from netmiko import ConnectHandler

device_ip = '172.31.111.4'
username = 'admin'
password = 'cisco'

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'key_file': os.path.expanduser("~/.ssh/id_rsa"),
}

commands = ["int lo0", "ip add 1.1.1.1 255.255.255.0", "no shut"]

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_config_set(commands)
    print(result)
