import ipaddress

import pexpect

PROMPT = '#'
IP = '10.0.15.111'
USERNAME = 'admin'
PASSWORD = 'cisco'
COMMAND = 'sh ip int bri'
devices = {
    '172.31.111.4': '1.1.1.1/32',
    '172.31.111.5': '2.2.2.2/32',
    '172.31.111.6': '3.3.3.3/32'
}


def connect(device_ip):
    child = pexpect.spawn('telnet ' + device_ip)
    child.expect('Username')
    child.sendline(USERNAME)
    child.expect('Password')
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    return child


def send_command(con, cmd, expect=PROMPT):
    con.sendline(cmd)
    con.expect(expect)


def set_loop_back(con, lop_ip):
    ip_iface = ipaddress.ip_interface(lop_ip)
    send_command(con, "conf t")
    send_command(con, "int lo0")
    send_command(con, "ip addr %s %s" % (ip_iface.ip, ip_iface.netmask))
    send_command(con, "no shut")
    send_command(con, "exit")
    send_command(con, "exit")
    send_command(con, "sh ip int br")
    print(get_result(con))


def get_result(con):
    result = con.before
    return result.decode('UTF-8')


def main():
    for device_ip in devices.keys():
        loop_back_ip = devices[device_ip]
        con = connect(device_ip)
        set_loop_back(con, loop_back_ip)


main()
