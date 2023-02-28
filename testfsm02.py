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

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_command('sh ip int br', use_textfsm=True)
    print(result)
