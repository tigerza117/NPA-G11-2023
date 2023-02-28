from netmikolab import *


def test_ip():
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        for test in device["tests"]["iface_ip"]:
            assert get_ip(param, test[0]) == test[1]


def test_subnet():
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        for test in device["tests"]["iface_subnet"]:
            assert get_subnet(param, test[0]) == test[1]


def test_description_and_stat():
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        for test in device["tests"]["iface_description_and_stat"]:
            assert get_iface_stat(param, test[0]) == test[1]
