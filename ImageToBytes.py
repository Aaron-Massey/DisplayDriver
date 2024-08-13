import os

from PIL import Image


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


def byte1Calc(x, y):
    byte = (y & 0b00001111) << 4  # Y
    byte |= (x & 0b00001111)  # X
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


def ImageToBytes(imageName, printHex=False, printBin=False, PrintDec=False, printFormatted=False):
    colors = imageToData(imageName)
    multiplePrints = sum([printHex, printBin, PrintDec, printFormatted]) >= 2

    # Loop through each pixel in the 8x8 grid of the current screen
    for y in range(32):
        for x in range(32):
            # Calculate the color index
            color_index = y * 32 + x
            # Extract the RGB components
            color = colors[color_index]
            # Calculate the four bytes
            byte1 = byte1Calc(x, y)
            byte2 = color[0]
            byte3 = color[1]
            byte4 = color[2]
            # Write to the pixel (Screen, X, Y, Color)
            output.append(f"{byte1:02X} {byte2:02X} {byte3:02X} {byte4:02X}")
            if printHex:
                print(f"{byte1:02X} {byte2:02X} {byte3:02X} {byte4:02X}")
            if printBin:
                print(f"{byte1:08b} {byte2:08b} {byte3:08b} {byte4:08b}")
            if PrintDec:
                print(f"{byte1} {byte2} {byte3} {byte4}")
            if printFormatted:
                print(f"X: {x}, Y: {y}, Color: {color}")
            if multiplePrints:
                print("-------------------------------------------------")

    output_str = "\n".join(output)
    print("Image converted to bytecode")
    return output_str
