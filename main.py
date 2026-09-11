from PIL import Image

def get_bit(num, pos):
    return (num >> pos) & 1

def turn_on_bit(num, pos):
    return num | (1 << pos)

def turn_off_bit(num, pos):
    return num & ~(1 << pos)

def set_bit_pair(num, pos, b1, b2):
    # byte:  0b10010111
    # set bit pair 1 0
    res = num
    print("set bit pair", pos, b1, b2)
    if b1:
        res = turn_on_bit(res, pos)
    else:
        res = turn_off_bit(res, pos)
    if b2:
        res = turn_on_bit(res, pos + 1)
    else:
        res = turn_off_bit(res, pos + 1)
    return res


path = "img.bmp"


def write_message(path, msg):
    img = Image.open(path)
    pixels = img.load()
    width, height = img.size
    max_len = width * height * 3 // 4

    print(f"Max length: {max_len}")

    msg += "\x03"
    print("=======", len(msg))
    print("----", ord(msg[-1]))

    counter = 0
    idx = 0

    for y in range(height):
        for x in range(width):
            p = []
            for b in pixels[x, y]:
                print("byte: ", bin(b))
                res = set_bit_pair(
                    b,
                    counter * 2,
                    get_bit(ord(msg[idx]), counter * 2),
                    get_bit(ord(msg[idx]), counter * 2 + 1)
                )
                print("res:  ", bin(res))
                p.append(res)
                counter += 1
                if counter == 4:
                    counter = 0
                    idx += 1
                    print(idx)
                    if idx >= len(msg):
                        pixels[x, y] = tuple(p)
                        img.save(path)
                        return
            pixels[x, y] = tuple(p)


def read_message(path):
    img = Image.open(path)
    pixels = img.load()
    width, height = img.size
    
    counter = 0
    idx = 0

    ch = 0
    
    res = ""

    for y in range(height):
        for x in range(width):
            for b in pixels[x, y]:
                print("*************** ", bin(b))
                print(counter, idx, ch, res)
                ch = set_bit_pair(
                    ch,
                    counter * 2,
                    get_bit(b, counter * 2),
                    get_bit(b, counter * 2 + 1)
                )
                counter += 1
                if counter == 4:
                    counter = 0
                    print("++++++++++++", ch, chr(ch))
                    res += chr(ch)
                    ch = 0
                    if len(res) > 15:
                        return res

write_message("img.bmp", "hello lohman")


read = read_message("img.bmp")
print(read)

