from PIL import Image

def imageMaker():
    img = Image.new('RGB', (32, 32), color='black')
    pixels = img.load()
    for i in range(0, 32, 8):
        for j in range(0, 32, 8):
            for x in range(8):
                pixels[i + x, j] = (255, 255, 255)
                pixels[i + x, j + 7] = (255, 255, 255)
                pixels[i, j + x] = (255, 255, 255)
                pixels[i + 7, j + x] = (255, 255, 255)
    return img

def byteToImage(byteFile):
    img = imageMaker()
    pixels = img.load()
    with open(byteFile, 'r') as file:
        data = file.read().split()
        i = 0
        while i < len(data):
            if i + 3 >= len(data):
                print(f"Not enough data for color at index {i}")
                break
            byte = int(data[i], 16)
            screen = byte & 0b00001111
            x = (byte & 0b01110000) >> 4
            y = (byte & 0b10000000) >> 7
            color = (int(data[i + 1], 16), int(data[i + 2], 16), int(data[i + 3], 16))
            pixel_x = (screen % 4) * 8 + x
            pixel_y = (screen // 4) * 8 + y
            pixels[pixel_x, pixel_y] = color
            i += 4
    img.save('byteOutput.jpg')
    return img

def load_image(path):
    img = Image.open(path)
    return list(img.getdata())

def encode_image(image_data):
    encoded_data = []
    for color in image_data:
        encoded_data.append(f"{color[0]:02X} {color[1]:02X} {color[2]:02X}")
    return ' '.join(encoded_data)

def decode_image(encoded_data):
    data = encoded_data.split()
    decoded_data = []
    for i in range(0, len(data), 3):
        decoded_data.append((int(data[i], 16), int(data[i+1], 16), int(data[i+2], 16)))
    return decoded_data

original_image_data = load_image('image.jpg')
encoded_data = encode_image(original_image_data)

with open('encoded_data.bin', 'w') as f:
    f.write(encoded_data)

decoded_image_data = decode_image(encoded_data)

if original_image_data == decoded_image_data:
    print("The encoding and decoding processes are correct.")
else:
    print("There is a mismatch between the original and decoded image data.")
    print("Original Image Data:", original_image_data)
    print("Decoded Image Data:", decoded_image_data)