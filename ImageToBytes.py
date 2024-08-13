import os
from PIL import Image
import pyperclip

def ensure_temp_directory():
    if not os.path.exists('temp'):
        os.makedirs('temp')

def imageToData(name):
    try:
        image = Image.open(name)
        if image.size != (32, 32):
            reduceImage(name)
        pixel_colors = []
        for y in range(32):
            for x in range(32):
                pixel_color = image.getpixel((x, y))
                pixel_colors.append(pixel_color)
        return pixel_colors
    except Exception as e:
        print(f"Error: {e}")
        return []

def byte1Calc(screen, x, y):
    byte = (y & 0b00000001) << 7  # 1 LSBs of Y
    byte |= (x & 0b00000111) << 4  # 3 LSBs of X
    byte |= (screen & 0b00001111)  # 4 LSBs of Screen number
    return byte

def byte2Calc(y, color):
    byte = (color[0] & 0b01111110) << 1  # 6 MSBs of red
    byte |= (y & 0b00000110) >> 1  # 2 LSBs of Y
    return byte

def byte3Calc(color):
    byte = (color[1] & 0b11111110)  # 7 MSBs of green
    byte |= (color[0] & 0b10000000) >> 7  # LSB of red
    return byte

def byte4Calc(color):
    byte = (color[2] & 0b11111110) >> 1  # 7 MSBs of blue
    return byte

def reduceImage(name):
    try:
        ensure_temp_directory()
        image = Image.open(name)

        # Check if the image is a PNG
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            # Create a new image with an opaque background
            alpha = image.convert('RGBA').split()[-1]
            background = Image.new("RGBA", image.size, (255, 255, 255, 255))
            background.paste(image, mask=alpha)
            image = background.convert('RGB')

        image = image.resize((32, 32))
        image.save("temp/reduced.jpg")
    except Exception as e:
        print(f"Error: {e}")

output = []

def clear_output():
    global output
    output = []

# Define the screen addresses in sequential order
screens = [
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 13, 14, 15
]

def ImageToBytes(imageName, printHex=False, printBin=False, PrintDec=False, printFormatted=False):
    colors = imageToData(imageName)
    multiplePrints = sum([printHex, printBin, PrintDec, printFormatted]) >= 2

    for i in range(4):
        for j in range(4):
            # Current screen address
            screen = screens[i * 4 + j]
            # Loop through each pixel in the 8x8 grid of the current screen
            for y in range(8):
                for x in range(8):
                    # Calculate the color index
                    color_index = ((i * 8 + y) * 32) + (j * 8 + x)
                    # Extract the RGB components
                    color = colors[color_index]
                    # Calculate the four bytes
                    byte1 = byte1Calc(screen, x, y)
                    byte2 = byte2Calc(y, color)
                    byte3 = byte3Calc(color)
                    byte4 = byte4Calc(color)
                    # Write to the pixel (Screen, X, Y, Color)
                    output.append(f"{byte1:02X} {byte2:02X} {byte3:02X} {byte4:02X}")
                    if(printHex):
                        print(f"{byte1:02X} {byte2:02X} {byte3:02X} {byte4:02X}")
                    if(printBin):
                        print(f"{byte1:08b} {byte2:08b} {byte3:08b} {byte4:08b}")
                    if(PrintDec):
                        print(f"{byte1} {byte2} {byte3} {byte4}")
                    if(printFormatted):
                        print(f"Screen: {screen}, X: {x}, Y: {y}, Color: {color}")
                    if multiplePrints:
                        print("-------------------------------------------------")


    output_str = "\n".join(output)
    print("Image converted to bytecode")
    return output_str