from PIL import Image


path = "img.bmp"

img = Image.open(path)
pixels = img.load()
width, height = img.size
max_len = width * height * 3 // 4

print(f"Max length: {max_len}")

msg = "Hello man"


counter = 0

for y in range(height):
    for x in range(width):
        p = []
        for b in pixels[x, y]:
            p.append(b | )
            counter += 1
            if counter == 4:
                counter = 0
                idx += 1
        pixels[x, y] = tuple(p)


img.save(path)




