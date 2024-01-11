import tkinter as tk
from app_ui import SteganographyApp

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
