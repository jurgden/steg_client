from PIL import Image

def to_bin(data):
    """Convert data to a binary format."""
    return ''.join([format(ord(char), '08b') for char in data])

def encode_image(image, message, stealth_level):
    binary_message = to_bin(message + "####")  # Append a delimiter
    pixels = list(image.getdata())
    new_pixels = []

    msg_index = 0
    for pixel in pixels:
        if msg_index < len(binary_message):
            new_pixel = list(pixel)
            for n in range(stealth_level):  # Modify n LSBs
                if msg_index < len(binary_message):
                    new_pixel[n] = (new_pixel[n] & ~1) | int(binary_message[msg_index])
                    msg_index += 1
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)
    
    image.putdata(new_pixels)
    return image
