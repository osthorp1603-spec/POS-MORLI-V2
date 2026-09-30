import customtkinter as ctk
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

from core.manager import Manager

if __name__ == "__main__":
    app = Manager()
    app.mainloop()