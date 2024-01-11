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

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        root.title("LSB Steganography")

        tk.Label(root, text="Select Image:").grid(row=0, column=0)
        self.entry_image = tk.Entry(root, width=40)
        self.entry_image.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.select_image).grid(row=0, column=2)

        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.grid(row=1, columnspan=3, pady=10)

        tk.Label(root, text="Available Space:").grid(row=2, column=0)
        self.label_space = tk.Label(root, text="0 characters")
        self.label_space.grid(row=2, column=1)

        tk.Label(root, text="Enter Message:").grid(row=3, column=0)
        self.entry_message = tk.Entry(root, width=40)
        self.entry_message.grid(row=3, column=1)

        tk.Button(root, text="Encode and Save", command=self.encode).grid(row=4, column=1)

        self.image = None

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, file_path)
            self.load_image(file_path)

    def load_image(self, path):
        # Load the image in a separate thread to keep the UI responsive
        threading.Thread(target=self.calculate_space, args=(path,)).start()

    def calculate_space(self, path):
        # Dummy function to simulate space calculation
        self.image = Image.open(path)
        # Update progress bar and available space label
        self.progress['value'] = 50  # Update this based on actual progress
        self.label_space.config(text=f"{self.get_available_space()} characters")

    def get_available_space(self):
        # Calculate and return the available space for message encoding
        return 1000  # Placeholder value

    def encode(self):
        message = self.entry_message.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message to encode.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png")])
        if not output_path:
            return

        # Encode the message in a separate thread
        threading.Thread(target=self.encode_message, args=(message, output_path)).start()

    def encode_message(self, message, output_path):
        # Update progress bar during encoding
        self.progress['value'] = 0
        # Dummy encoding process
        for i in range(100):
            self.progress['value'] += 1
            time.sleep(0.1)  # Simulate encoding time

        # Save the encoded image
        self.image.save(output_path, "PNG")
        messagebox.showinfo("Success", f"Image saved to {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()