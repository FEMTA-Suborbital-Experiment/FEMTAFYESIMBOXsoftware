# Sloppy script for windows to ping all IPv4 addresses in a given range
# i.e. using the arg "192.168.1.0/24" will ping addresses from 192.168.1.0 to 192.168.1.255

import sys
import subprocess


if len(sys.argv) == 1:
    raise RuntimeError("no ip address provided")

address, mask_bits = sys.argv[1].split("/")
address = int("".join([f"{int(byte):02x}" for byte in address.split(".")]), 16)
mask_bits = int(mask_bits)


def num_to_ip(num):
    num = hex(num)[2:]
    return ".".join(str(int(num[i : i + 2], 16)) for i in range(0, 8, 2))


for incr in range(2 ** (32 - mask_bits)):
    command = ["ping", "-n", "1", num_to_ip(address + incr)]
    subprocess.Popen(command, stdout=subprocess.DEVNULL)
    print(" ".join(command))
