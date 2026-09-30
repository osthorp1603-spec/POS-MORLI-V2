import sqlite3
from database.conexion import obtener_conexion

def verificar_codigo_existe(codigo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM codigos WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] > 0
    except sqlite3.Error as e:
        print(f"Error al verificar código: {e}")
        return False            

def insertar_codigo(codigo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO codigos (codigo) VALUES (?)", (codigo,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al insertar código: {e}")
        return False    