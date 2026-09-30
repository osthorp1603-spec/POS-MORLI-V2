import sqlite3
from database.conexion import obtener_conexion

def guardar_rf(factura_provisional, nombre_articulo, valor_articulo, cantidad, subtotal):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rf_registros (factura_provisional, nombre_articulo, valor_articulo, cantidad, subtotal, fecha)
            VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
        """, (factura_provisional, nombre_articulo, valor_articulo, cantidad, subtotal))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar RF: {e}")
        return False