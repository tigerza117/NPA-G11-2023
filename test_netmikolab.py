import threading

from netmikolab import *


def validate_ip(param, tests):
    for test in tests:
        assert get_ip(param, test[0]) == test[1]


def validate_subnet(param, tests):
    for test in tests:
        assert get_subnet(param, test[0]) == test[1]


def validate_description_and_stat(param, tests):
    for test in tests:
        data = get_iface_stat(param, test[0])
        assert data == test[1]


def test_ip():
    threads = list()
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        x = threading.Thread(target=validate_ip, args=(param, device["tests"]["iface_ip"]))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()


def test_subnet():
    threads = list()
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        x = threading.Thread(target=validate_subnet, args=(param, device["tests"]["iface_subnet"]))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()


def test_description_and_stat():
    threads = list()
    for device in devices_config.values():
        param = dict(params, ip=device["mgmt_ip"])
        x = threading.Thread(target=validate_description_and_stat,
                             args=(param, device["tests"]["iface_description_and_stat"]))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
