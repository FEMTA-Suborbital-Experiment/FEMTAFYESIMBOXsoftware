 # Collection of commonly-used functions across multiple modules.

def twos_comp(num):
    return num if num >= 0 else 65536 + num
