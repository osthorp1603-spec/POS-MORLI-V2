import sqlite3
from database.conexion import obtener_conexion

def guardar_decoracion(nombre, precio_venta, costo_total, componentes):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO inventario 
            (nombre, proveedor, precio, costo, stock, tipo_producto, codigo_barras, umbral_stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, "morli", precio_venta, costo_total, 1000, "decoracion", "", 5))

        id_decoracion = cursor.lastrowid

        for id_componente, cantidad in componentes:
            cursor.execute("""
                INSERT INTO decoraciones_detalle (id_decoracion, id_componente, cantidad)
                VALUES (?, ?, ?)
            """, (id_decoracion, id_componente, cantidad))

        conn.commit()
        conn.close()
        return id_decoracion

    except sqlite3.Error as e:
        print(f"Error al guardar decoración: {e}")
        return None

def obtener_productos_para_decoracion():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, stock, precio FROM inventario")
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener productos: {e}")
        return []

def obtener_costo_por_id(producto_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT costo FROM inventario WHERE id = ?", (producto_id,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print(f"Error al obtener costo: {e}")
        return None    
