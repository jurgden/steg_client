import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("LSB Steganography Application")
        self.label_space = tk.Label(master, text="Available Space: 0 characters")
        self.label_space.grid(row=2, column=1)


        # Set up the layout here
        tk.Label(master, text="Select Image:").grid(row=0, column=0)
        self.entry_image = tk.Entry(master, width=40)
        self.entry_image.grid(row=0, column=1)
        tk.Button(master, text="Browse", command=self.select_image).grid(row=0, column=2)

        # Placeholder for additional UI elements
        # ...

    def load_image(self, path):
        """Load the image and calculate available space."""
        self.image = Image.open(path)
        self.calculate_space()

    def calculate_space(self):
        """Calculate and update the UI with available space for encoding."""
        width, height = self.image.size
        available_space = (width * height * 3) // 8
        self.label_space.config(text=f"Available Space: {available_space} characters")



    def select_image(self):
        # This function will handle the image selection
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, file_path)
            self.load_image(file_path)

        # Additional methods for other functionalities will go here
        # ...

# This function can be used to run this window directly for testing
def run():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
