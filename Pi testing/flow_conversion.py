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

def twos_comp(num):
    return num if num >= 0 else 65536 + num

def flow_to_bytes(flow_data, temp_data): #Input flow in ml/min, temp in C
    #Initialize output bytes
    output = [0] * 9
    
    #Prepare flags
    air = 0
    if abs(flow) > 65:
        high_flow = 1
        flow_data = 0
    else:
        high_flow = 0
    
    #Scale data and make flags byte
    flow_data *= 500
    temp_data *= 200
    flow_data = twos_comp(flow_data)
    temp_data = twos_comp(temp_data)
    flags = 0 | (0x1 if air else 0x0) | (0x2 if high_flow else 0x0)
    
    #Set output bytes
    output[0] = flow_data // 256
    output[1] = flow_data % 256
    output[3] = temp_data // 256
    output[4] = temp_data % 256
    output[7] = flags
    
    #Calculate crcs
    output[2] = crc(output[0], output[1])
    output[5] = crc(output[3], output[4])
    output[8] = crc(output[6], output[7])
    
    return output