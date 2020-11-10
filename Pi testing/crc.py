def crc(message):
    poly, val = 0x31, 0xff
    for b in message:
        val ^= b
        for i in range(8):
            if val & 0x80:
                val = ((val << 1) ^ poly) % 256
            else:
                val <<= 1
    return val