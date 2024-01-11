import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os

### Below is the lsb encoding/decoding functionality

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

### Above is the encode/decode functionality, below is tkinter implementation

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_image.delete(0, tk.END)
        entry_image.insert(0, file_path)

def encode():
    image_path = entry_image.get()
    message = entry_message.get()
    if not image_path or not message:
        messagebox.showerror("Error", "Please select an image and enter a message.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png")])
    if not output_path:
        return

    try:
        process_image(image_path, message, output_path)
        messagebox.showinfo("Success", f"Image saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

### instantiate the app

app = tk.Tk()
app.title("LSB Steganography")

tk.Label(app, text="Select Image:").grid(row=0, column=0, padx=10, pady=10)
entry_image = tk.Entry(app, width=40)
entry_image.grid(row=0, column=1, padx=10, pady=10)
button_browse = tk.Button(app, text="Browse", command=select_image)
button_browse.grid(row=0, column=2, padx=10, pady=10)

tk.Label(app, text="Enter Message:").grid(row=1, column=0, padx=10, pady=10)
entry_message = tk.Entry(app, width=40)
entry_message.grid(row=1, column=1, padx=10, pady=10)

button_encode = tk.Button(app, text="Encode and Save", command=encode)
button_encode.grid(row=2, column=1, padx=10, pady=10)

app.mainloop()