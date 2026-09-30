import sqlite3
from utils.rutas import ruta_base
import sys
import os

db_name = os.path.join(ruta_base(), "database.db")

def obtener_conexion():
    return sqlite3.connect(db_name)