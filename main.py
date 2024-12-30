# main.py

import tkinter as tk
from ui.app_gui import AppGUI

def main():
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
