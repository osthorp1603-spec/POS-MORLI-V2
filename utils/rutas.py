import sys
import os

def ruta_base():
    try:
        return sys._MEIPASS
    except AttributeError:
        return os.path.abspath(".")

  