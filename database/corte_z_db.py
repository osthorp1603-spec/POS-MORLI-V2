import sqlite3
from database.conexion import obtener_conexion

# --- CORTE Z (consultas y marcado) ---
def obtener_resumen_ventas():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.tipo_producto, SUM(dv.cantidad), SUM(dv.subtotal)
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE v.z_cerrado = 0
            GROUP BY i.tipo_producto
        """)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener resumen de ventas: {e}")
        return []

def obtener_resumen_rf():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.tipo_producto, SUM(r.cantidad), SUM(r.subtotal)
            FROM rf_registros r
            LEFT JOIN inventario i ON r.nombre_articulo = i.nombre
            WHERE r.z_cerrado = 0
            GROUP BY i.tipo_producto
        """)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener resumen RF: {e}")
        return []

def obtener_totales_corte():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Totales de dinero (ventas sin cerrar)
        cursor.execute("""
            SELECT 
                SUM(pago_efectivo),
                SUM(pago_qr),
                SUM(pago_tarjeta),
                SUM(total),
                SUM(cambio)
            FROM ventas
            WHERE z_cerrado = 0
        """)
        resultado_dinero = cursor.fetchone()

        # Cantidad y ganancia total (detalle)
        cursor.execute("""
            SELECT 
                SUM(dv.cantidad),
                SUM(dv.subtotal - (IFNULL(i.costo, 0) * dv.cantidad))
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE v.z_cerrado = 0
        """)
        resultado_detalle = cursor.fetchone()

        # Total RF sin cerrar
        cursor.execute("""
            SELECT SUM(subtotal) FROM rf_registros WHERE z_cerrado = 0
        """)
        resultado_rf = cursor.fetchone()

        # Salida de efectivo sin cerrar
        cursor.execute("""
            SELECT SUM(monto) FROM salida_efectivo WHERE z_cerrado = 0
        """)
        resultado_salida = cursor.fetchone()

        conn.close()

        efectivo = resultado_dinero[0] if resultado_dinero[0] is not None else 0
        qr = resultado_dinero[1] if resultado_dinero[1] is not None else 0
        tarjeta = resultado_dinero[2] if resultado_dinero[2] is not None else 0
        total_vendido = resultado_dinero[3] if resultado_dinero[3] is not None else 0
        cambio = resultado_dinero[4] if resultado_dinero[4] is not None else 0

        cantidad_total = resultado_detalle[0] if resultado_detalle[0] is not None else 0
        ganancia_total = resultado_detalle[1] if resultado_detalle[1] is not None else 0

        total_rf = resultado_rf[0] if resultado_rf[0] is not None else 0
        total_salida = resultado_salida[0] if resultado_salida[0] is not None else 0

        efectivo_neto = efectivo - cambio
        efectivo_final = efectivo_neto - total_salida

        return {
            "efectivo": efectivo,
            "qr": qr,
            "tarjeta": tarjeta,
            "total_vendido": total_vendido,
            "cambio": cambio,
            "efectivo_neto": efectivo_neto,
            "cantidad_total": cantidad_total,
            "ganancia_total": ganancia_total,
            "total_rf": total_rf,
            "total_salida": total_salida,
            "efectivo_final": efectivo_final
        }
    except sqlite3.Error as e:
        print(f"Error al obtener totales del corte: {e}")
        return {
            "efectivo": 0, "qr": 0, "tarjeta": 0, "total_vendido": 0,
            "cambio": 0, "efectivo_neto": 0, "cantidad_total": 0,
            "ganancia_total": 0, "total_rf": 0, "total_salida": 0,
            "efectivo_final": 0
        }

def marcar_todo_cerrado():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE ventas SET z_cerrado = 1 WHERE z_cerrado = 0")
        cursor.execute("UPDATE rf_registros SET z_cerrado = 1 WHERE z_cerrado = 0")
        cursor.execute("UPDATE salida_efectivo SET z_cerrado = 1 WHERE z_cerrado = 0")
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al marcar como cerrado: {e}")
        return False        