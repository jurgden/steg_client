from PIL import Image

def to_bin(data):
    """Convert data to binary."""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, int):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode_image(img, message):
    image = Image.open(img, 'r')
    message += "####"  # Delimiter to identify end of message
    data = to_bin(message)
    data_len = len(data)

    iter_pixels = iter(image.getdata())

    for i in range(data_len):
        # Extract 3 pixels at a time
        pixel = [value for value in next(iter_pixels)[:3] +
                 next(iter_pixels)[:3] +
                 next(iter_pixels)[:3]]
        
        # Modify the least significant bit
        for j in range(0, 8):
            if data[i][j] == '0' and pixel[j]%2 != 0:
                pixel[j] -= 1
            elif data[i][j] == '1' and pixel[j]%2 == 0:
                if pixel[j] != 0:
                    pixel[j] -= 1
                else:
                    pixel[j] += 1
        
        # Check if it's the 8th pixel
        if i == data_len - 1:
            if pixel[-1] % 2 == 0:
                if pixel[-1] != 0:
                    pixel[-1] -= 1
                else:
                    pixel[-1] += 1
        else:
            if pixel[-1] % 2 != 0:
                pixel[-1] -= 1

        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]

def process_image(img, message, output_img):
    image = Image.open(img, 'r')
    new_image = image.copy()
    w, h = new_image.size
    (x, y) = (0, 0)

    for pixel in encode_image(img, message):
        new_image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1
    
    new_image.save(output_img, "PNG")
    return output_img

# Example Usage
input_image = "input.jpg"  # Path to the input image
output_image = "output.png"  # Path to save the output image
secret_message = "Your secret message here"
process_image(input_image, secret_message, output_image)
