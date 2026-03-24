import sqlite3
import csv
from datetime import datetime

def conectar():
    return sqlite3.connect("finanzas_pro.db")

def registrar_movimiento(monto, tipo, cuenta_id, categoria, descripcion=None):
    """Guarda un nuevo registro en la base de datos."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transacciones (monto, tipo, cuenta_id, categoria, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (monto, tipo, cuenta_id, categoria, descripcion))
        conn.commit()

def obtener_balance_total():
    """Calcula el estado financiero actual."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Ingreso'")
        ingresos = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Egreso'")
        egresos = cursor.fetchone()[0] or 0
        return ingresos - egresos

def exportar_cartola_csv():
    """Genera un archivo CSV con el detalle de movimientos."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.fecha, t.descripcion, t.monto, t.tipo, c.nombre, t.categoria 
            FROM transacciones t JOIN cuentas c ON t.cuenta_id = c.id
        """)
        datos = cursor.fetchall()
        
        nombre_archivo = "cartola_finanzas.csv"
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha", "Nota", "Monto", "Tipo", "Plataforma", "Categoría"])
            writer.writerows(datos)
    return nombre_archivo