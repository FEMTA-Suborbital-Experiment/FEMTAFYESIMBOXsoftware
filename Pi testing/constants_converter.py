# Hacked-together script to convert the matlab constants to Python

def convert(block):
    output = str()
    block = list(map(lambda s: s.split("  "), block.split("\n")))
    block = [[item.strip(" #") for item in line if item] for line in block]
    max_len = max([len(l[0]) + 2 + len(l[2]) for l in block]) + 2
    for line in block:
        start = line[0] + " #" + line[2]
        output += start + " "*(max_len - len(start)) + line[1] + "\n"
    return output

if __name__ == "__main__":
    inpt = """"""
    print(convert(inpt))
