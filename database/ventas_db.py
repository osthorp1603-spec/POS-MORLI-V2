import sqlite3
from database.conexion import obtener_conexion

# --- VENTAS (escritura) ---
def guardar_venta(factura,fecha,total,pago_efectivo,pago_qr,pago_tarjeta,cambio):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO ventas
                        (factura,fecha,total,pago_efectivo,pago_qr,pago_tarjeta,cambio)
                        VALUES(?,?,?,?,?,?,?)""",
                        (factura, fecha, total, pago_efectivo, pago_qr, pago_tarjeta, cambio))
        venta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return venta_id
    except sqlite3.Error as e:
        print(f"Error al guardar ventas: {e}")   

def guardar_detalle_venta(venta_id,nombre_articulo,valor_articulo,cantidad,subtotal):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO detalle_ventas
                            (venta_id,nombre_articulo,valor_articulo,cantidad,subtotal)
                            VALUES(?,?,?,?,?)""",
                            (venta_id,nombre_articulo,valor_articulo,cantidad,subtotal))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al guardar detalle venta: {e}")      

# --- VENTAS (lectura) ---
def obtener_siguiente_factura(fecha):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(factura) FROM ventas WHERE date(fecha) = ?", (fecha,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado[0] is None:
            return 1
        else:
            return int(resultado[0]) + 1
    except sqlite3.Error as e:
        print(f"Error al obtener siguiente factura: {e}")
        return 1

def obtener_ventas_pendientes():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas WHERE z_cerrado = 0 ORDER BY fecha ASC")
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener ventas pendientes: {e}")
        return []    