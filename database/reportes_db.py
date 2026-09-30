import sqlite3
from database.conexion import obtener_conexion

# --- VENTAS (lectura para reporte) ---
def obtener_ventas_reporte(proveedor="", tipo_producto="", fecha_desde="", fecha_hasta=""):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        query = """
            SELECT 
                dv.id,
                v.factura,
                v.fecha,
                dv.nombre_articulo,
                i.tipo_producto,
                i.proveedor,
                dv.cantidad,
                dv.valor_articulo,
                dv.subtotal,
                (dv.subtotal - (i.costo * dv.cantidad)) AS ganancia,
                v.pago_efectivo,
                v.pago_qr,
                v.pago_tarjeta
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
        """

        condiciones = []
        parametros = []

        if proveedor:
            condiciones.append("i.proveedor = ?")
            parametros.append(proveedor)

        if tipo_producto:
            condiciones.append("i.tipo_producto = ?")
            parametros.append(tipo_producto)

        if fecha_desde and fecha_hasta:
            condiciones.append("DATE(v.fecha) BETWEEN ? AND ?")
            parametros.append(fecha_desde)
            parametros.append(fecha_hasta)

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        query += " ORDER BY v.factura DESC, dv.id ASC"

        cursor.execute(query, parametros)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener ventas para reporte: {e}")
        return []

# --- TOTALES (sumas para labels) ---
def obtener_totales_reporte(proveedor="", tipo_producto="", fecha_desde="", fecha_hasta=""):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Totales de dinero (sin duplicar por factura)
        query_dinero = """
            SELECT 
                SUM(v.pago_efectivo),
                SUM(v.pago_qr),
                SUM(v.pago_tarjeta),
                SUM(v.total),
                SUM(v.cambio)
            FROM ventas v
            WHERE v.id IN (
                SELECT DISTINCT dv.venta_id
                FROM detalle_ventas dv
                LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
                WHERE 1=1
        """

        condiciones = []
        parametros = []

        if proveedor:
            condiciones.append(" AND i.proveedor = ?")
            parametros.append(proveedor)

        if tipo_producto:
            condiciones.append(" AND i.tipo_producto = ?")
            parametros.append(tipo_producto)

        if fecha_desde and fecha_hasta:
            condiciones.append(" AND DATE(v.fecha) BETWEEN ? AND ?")
            parametros.append(fecha_desde)
            parametros.append(fecha_hasta)

        query_dinero += "".join(condiciones) + ")"

        cursor.execute(query_dinero, parametros)
        resultado_dinero = cursor.fetchone()

        # Cantidad total vendida (suma de cantidades en detalle)
        query_cantidad = """
            SELECT SUM(dv.cantidad)
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE 1=1
        """

        condiciones_cant = []
        parametros_cant = []

        if proveedor:
            condiciones_cant.append(" AND i.proveedor = ?")
            parametros_cant.append(proveedor)

        if tipo_producto:
            condiciones_cant.append(" AND i.tipo_producto = ?")
            parametros_cant.append(tipo_producto)

        if fecha_desde and fecha_hasta:
            condiciones_cant.append(" AND DATE(v.fecha) BETWEEN ? AND ?")
            parametros_cant.append(fecha_desde)
            parametros_cant.append(fecha_hasta)

        query_cantidad += "".join(condiciones_cant)

        cursor.execute(query_cantidad, parametros_cant)
        resultado_cantidad = cursor.fetchone()

        # Ganancia total del período
        query_ganancia = """
            SELECT SUM(dv.subtotal - (IFNULL(i.costo, 0) * dv.cantidad))
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE 1=1
        """

        condiciones_gan = []
        parametros_gan = []

        if proveedor:
            condiciones_gan.append(" AND i.proveedor = ?")
            parametros_gan.append(proveedor)

        if tipo_producto:
            condiciones_gan.append(" AND i.tipo_producto = ?")
            parametros_gan.append(tipo_producto)

        if fecha_desde and fecha_hasta:
            condiciones_gan.append(" AND DATE(v.fecha) BETWEEN ? AND ?")
            parametros_gan.append(fecha_desde)
            parametros_gan.append(fecha_hasta)

        query_ganancia += "".join(condiciones_gan)

        cursor.execute(query_ganancia, parametros_gan)
        resultado_ganancia = cursor.fetchone()

        conn.close()

        efectivo = resultado_dinero[0] if resultado_dinero[0] is not None else 0
        qr = resultado_dinero[1] if resultado_dinero[1] is not None else 0
        tarjeta = resultado_dinero[2] if resultado_dinero[2] is not None else 0
        total_vendido = resultado_dinero[3] if resultado_dinero[3] is not None else 0
        cambio = resultado_dinero[4] if resultado_dinero[4] is not None else 0
        efectivo = efectivo -cambio
        cantidad_total = resultado_cantidad[0] if resultado_cantidad[0] is not None else 0
        ganancia_total = resultado_ganancia[0] if resultado_ganancia[0] is not None else 0

        return {
            "efectivo": efectivo,
            "qr": qr,
            "tarjeta": tarjeta,
            "total_vendido": total_vendido,
            "cantidad_total": cantidad_total,
            "ganancia_total": ganancia_total
        }
    except sqlite3.Error as e:
        print(f"Error al obtener totales del reporte: {e}")
        return {"efectivo": 0, "qr": 0, "tarjeta": 0, "total_vendido": 0, "cantidad_total": 0}   

# --- VENTAS DEL DÍA (solo hoy) ---
def obtener_ventas_del_dia():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                dv.id,
                v.factura,
                dv.nombre_articulo,
                dv.cantidad,
                dv.valor_articulo,
                dv.subtotal,
                v.pago_efectivo,
                v.pago_qr,
                v.pago_tarjeta,
                (dv.subtotal - (IFNULL(i.costo, 0) * dv.cantidad)) AS ganancia
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE DATE(v.fecha) = DATE('now', 'localtime') OR v.z_cerrado = 0
            ORDER BY v.factura DESC, dv.id ASC
        """)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener ventas del día: {e}")
        return []     

# --- TOTALES DEL DÍA ---
def obtener_totales_del_dia():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Totales de dinero (sin duplicar por factura)
        cursor.execute("""
            SELECT 
                SUM(v.pago_efectivo),
                SUM(v.pago_qr),
                SUM(v.pago_tarjeta),
                SUM(v.total),
                SUM(v.cambio)
            FROM ventas v
            WHERE DATE(v.fecha) = DATE('now', 'localtime') OR v.z_cerrado = 0
        """)
        resultado_dinero = cursor.fetchone()

        # Cantidad y ganancia total
        cursor.execute("""
            SELECT 
                SUM(dv.cantidad),
                SUM(dv.subtotal - (IFNULL(i.costo, 0) * dv.cantidad))
            FROM detalle_ventas dv
            LEFT JOIN ventas v ON dv.venta_id = v.id
            LEFT JOIN inventario i ON dv.nombre_articulo = i.nombre
            WHERE DATE(v.fecha) = DATE('now', 'localtime') OR v.z_cerrado = 0
        """)
        resultado_detalle = cursor.fetchone()

        conn.close()

        efectivo = resultado_dinero[0] if resultado_dinero[0] is not None else 0
        qr = resultado_dinero[1] if resultado_dinero[1] is not None else 0
        tarjeta = resultado_dinero[2] if resultado_dinero[2] is not None else 0
        total_vendido = resultado_dinero[3] if resultado_dinero[3] is not None else 0
        cambio = resultado_dinero[4] if resultado_dinero[4] is not None else 0
        efectivo = efectivo - cambio

        cantidad_total = resultado_detalle[0] if resultado_detalle[0] is not None else 0
        ganancia_total = resultado_detalle[1] if resultado_detalle[1] is not None else 0

        return {
            "efectivo": efectivo,
            "qr": qr,
            "tarjeta": tarjeta,
            "total_vendido": total_vendido,
            "cantidad_total": cantidad_total,
            "ganancia_total": ganancia_total
        }
    except sqlite3.Error as e:
        print(f"Error al obtener totales del día: {e}")
        return {"efectivo": 0, "qr": 0, "tarjeta": 0, "total_vendido": 0, "cantidad_total": 0, "ganancia_total": 0}    