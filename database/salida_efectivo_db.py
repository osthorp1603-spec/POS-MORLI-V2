import sqlite3
from database.conexion import obtener_conexion

def guardar_salida(monto,motivo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO salida_efectivo (monto,motivo,fecha)
                        VALUES (?,? , datetime('now','localtime'))
                    """,(monto,motivo))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar salida de efectivo: {e}")
        return False