import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from steg_encoder import encode_image


class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("LSB Steganography Application")
        self.label_space = tk.Label(master, text="Available Space: 0 characters")
        self.label_space.grid(row=2, column=1)
        self.stealth_slider = tk.Scale(master, from_=1, to=3, orient=tk.HORIZONTAL, label="Stealth Level")
        self.stealth_slider.grid(row=3, column=1)
        tk.Label(master, text="Enter Message:").grid(row=4, column=0)
        self.message_entry = tk.Text(master, height=4, width=40)
        self.message_entry.grid(row=4, column=1)
        



        # Set up the layout here
        tk.Label(master, text="Select Image:").grid(row=0, column=0)
        self.entry_image = tk.Entry(master, width=40)
        self.entry_image.grid(row=0, column=1)
        tk.Button(master, text="Browse", command=self.select_image).grid(row=0, column=2)
        tk.Button(master, text="Encode Message", command=self.encode_message).grid(row=5, column=1)


        # Placeholder for additional UI elements
        # ...
    
    def get_lsb(self, pixel):
        """Get the LSB of each color channel in the pixel."""
        return (pixel[0] & 1, pixel[1] & 1, pixel[2] & 1)

    
    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, file_path)
            self.load_image(file_path)


    def load_image(self, path):
        try:
            self.image = Image.open(path)
            self.calculate_space()
        except IOError:
            messagebox.showerror("Error", "Failed to load image.")
            self.label_space.config(text="Available Space: 0 characters")

    def calculate_space(self):
        if hasattr(self, 'image'):
            width, height = self.image.size
            stealth_level = self.stealth_slider.get()
            bits_per_pixel = stealth_level  # Assuming 1 to 3 bits per pixel
            capacity_in_chars = (width * height * bits_per_pixel) // 8
            self.label_space.config(text=f"Available Space: {capacity_in_chars} characters")
        else:
            self.label_space.config(text="Available Space: 0 characters")


    def encode_message(self):
        if not hasattr(self, 'image'):
            messagebox.showerror("Error", "No image loaded.")
            return

        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encode.")
            return

        stealth_level = self.stealth_slider.get()
        encoded_image = encode_image(self.image, message, stealth_level)

        # Check if the message length exceeds the capacity
        width, height = self.image.size
        max_capacity = (width * height * stealth_level) // 8
        if len(message) > max_capacity:
            messagebox.showerror("Error", "Message is too long for the selected stealth level.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            try:
                encoded_image.save(save_path, "PNG")
                messagebox.showinfo("Success", f"Message encoded. Image saved to {save_path}")
            except IOError:
                messagebox.showerror("Error", "Failed to save the image.")




        # Additional methods for other functionalities will go here
        # ...

# This function can be used to run this window directly for testing
def run():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
