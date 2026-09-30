import sqlite3
from database.conexion import obtener_conexion

# --- PRODUCTOS (lectura) ---
def obtener_nombres_productos():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM inventario")
        productos = cursor.fetchall()
        conn.close()
        return productos
    except sqlite3.Error as e:
        print("Error al obtener productos:", e)
        return []

def obtener_todos_los_productos():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventario ORDER BY tipo_producto ASC, proveedor ASC, nombre ASC")
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al obtener productos: {e}")
        return []    

def obtener_precio_producto(nombre):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print("Error al obtener precio:", e)
        return None    

def obtener_stock_producto(nombre):
    try:
        conn  = obtener_conexion()
        cursor =conn.cursor()
        cursor.execute("""SELECT stock FROM inventario
                            WHERE nombre = ?""",(nombre,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print(f"Error al verificar Stock: {e}")
        return None        

def buscar_productos_por_nombre(texto):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""SELECT nombre FROM inventario
                            WHERE nombre LIKE ?""",(f"%{texto}%",))
        productos = cursor.fetchall()
        conn.close()
        return productos
    except sqlite3.Error as e:
        print("Error al buscar productos:", e)
        return []

def buscar_productos_completos_por_nombre(texto):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM inventario
            WHERE LOWER(TRIM(nombre)) LIKE ?
            ORDER BY tipo_producto ASC, proveedor ASC, nombre ASC
        """, (f"%{texto.lower()}%",))
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al buscar productos por nombre: {e}")
        return []

def buscar_producto_por_codigo(codigo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, precio FROM inventario WHERE codigo_barras = ?", (codigo,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"Error al buscar por código: {e}")
        return None    

def obtener_precio_por_id(producto_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT precio FROM inventario WHERE id = ?", (producto_id,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print(f"Error al obtener precio por ID: {e}")
        return None    

# --- PRODUCTOS (escritura) ---
def insertar_producto(nombre, proveedor, precio, costo, stock, tipo_producto, codigo_barras="", umbral_stock=1):
    try:
        nombre = nombre.strip()
        proveedor = proveedor.strip()
        tipo_producto = tipo_producto.strip()
        codigo_barras = codigo_barras.strip()
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventario (nombre, proveedor, precio, costo, stock, tipo_producto, codigo_barras, umbral_stock)
            VALUES (?,?,?,?,?,?,?,?)
            """,(nombre, proveedor, precio, costo, stock, tipo_producto, codigo_barras, umbral_stock))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al insertar producto: {e}")
        return False

def actualizar_producto(producto_id, nombre, proveedor, precio, costo, stock, tipo_producto):
    try:
        nombre = nombre.strip()
        proveedor = proveedor.strip()
        tipo_producto = tipo_producto.strip()
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventario
            SET nombre = ?, proveedor = ?, precio = ?, costo = ?, stock = ?, tipo_producto = ?
            WHERE id = ?
        """, (nombre, proveedor, precio, costo, stock, tipo_producto, producto_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar producto: {e}")
        return False        

def eliminar_producto_por_id(producto_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventario WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al eliminar producto: {e}")
        return False

# --- STOCK ---
def restar_stock_producto(nombre, cantidad):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            return False
        stock_actual = resultado[0]
        if stock_actual < cantidad:
            conn.close()
            return False
        cursor.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad, nombre))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al restar stock: {e}")
        return False  

def hay_stock_suficiente(nombre, cantidad):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        if not resultado:
            return False
        return resultado[0] >= cantidad
    except sqlite3.Error as e:
        print(f"Error al verificar stock suficiente: {e}")
        return False    

def restar_stock_con_componentes(nombre, cantidad):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            return False
        producto_id = resultado[0]
        cursor.execute("UPDATE inventario SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
        cursor.execute("SELECT id_componente, cantidad FROM decoraciones_detalle WHERE id_decoracion = ?", (producto_id,))
        componentes = cursor.fetchall()
        for id_componente, cant_componente in componentes:
            cursor.execute("UPDATE inventario SET stock = stock - ? WHERE id = ?", (cant_componente * cantidad, id_componente))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al restar stock con componentes: {e}")
        return False

def hay_stock_suficiente_con_componentes(nombre, cantidad):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            return True, ""
        producto_id, stock_producto = resultado
        if stock_producto < cantidad:
            conn.close()
            return False, f"Stock insuficiente de '{nombre}'"
        cursor.execute("SELECT id_componente, cantidad FROM decoraciones_detalle WHERE id_decoracion = ?", (producto_id,))
        componentes = cursor.fetchall()
        for id_componente, cant_componente in componentes:
            cursor.execute("SELECT nombre, stock FROM inventario WHERE id = ?", (id_componente,))
            comp = cursor.fetchone()
            if comp:
                nombre_comp, stock_comp = comp
                if stock_comp < cant_componente * cantidad:
                    conn.close()
                    return False, f"Stock insuficiente del componente '{nombre_comp}'"
        conn.close()
        return True, ""
    except sqlite3.Error as e:
        print(f"Error al verificar stock con componentes: {e}")
        return False, "Error al verificar stock"    
    

# --- CÓDIGO DE BARRAS ---
def verificar_codigo_duplicado(codigo, producto_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre FROM inventario
            WHERE codigo_barras = ? AND id != ?
        """, (codigo, producto_id))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Error al verificar código duplicado: {e}")
        return None

def actualizar_codigo_barras(producto_id, codigo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventario SET codigo_barras = ? WHERE id = ?", (codigo, producto_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar código de barras: {e}")
        return False

# --- UMBRAL ---
def obtener_umbral_producto(nombre):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT umbral_stock FROM inventario WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        print(f"Error al obtener umbral: {e}")
        return None 

def actualizar_umbral_producto(producto_id, nuevo_umbral):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventario SET umbral_stock = ? WHERE id = ?", (nuevo_umbral, producto_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar umbral: {e}")
        return False  

# --- PROVEEDORES ---
def obtener_proveedores():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT TRIM(proveedor) FROM inventario WHERE proveedor IS NOT NULL AND TRIM(proveedor) != '' ORDER BY TRIM(proveedor) ASC")
        proveedores = cursor.fetchall()
        conn.close()
        return proveedores
    except sqlite3.Error as e:
        print(f"Error al obtener proveedores: {e}")
        return []
        
def obtener_tipos_producto():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT TRIM(tipo_producto) FROM inventario WHERE tipo_producto IS NOT NULL AND TRIM(tipo_producto) != '' ORDER BY TRIM(tipo_producto) ASC")
        tipos = cursor.fetchall()
        conn.close()
        return tipos
    except sqlite3.Error as e:
        print(f"Error al obtener tipos de producto: {e}")
        return []
        
