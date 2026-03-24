import sqlite3
from datetime import datetime, timedelta

def conectar():
    return sqlite3.connect("finanzas_pro.db")

# --- FUNCIONES DE LECTURA (R de CRUD) ---

def obtener_cuentas():
    """Trae la lista de plataformas (Efectivo, MACH, etc.)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM cuentas")
        return cursor.fetchall()

def obtener_balance_total():
    """Calcula el saldo neto sumando todos los ingresos y restando egresos."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Ingreso'")
        ingresos = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(monto) FROM transacciones WHERE tipo = 'Egreso'")
        egresos = cursor.fetchone()[0] or 0
        return ingresos - egresos

# --- FUNCIONES DE ESCRITURA (C, U, D de CRUD) ---

def registrar_movimiento(monto, tipo, cuenta_id, categoria, descripcion=None):
    """
    Registra un ingreso o gasto. 
    La descripción es opcional.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transacciones (monto, tipo, cuenta_id, categoria, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (monto, tipo, cuenta_id, categoria, descripcion))
        conn.commit()

# --- LÓGICA DE PERIODOS Y AUTOMATIZACIÓN ---

def procesar_pagos_pendientes():
    """
    Revisa si hay pagos programados (ej. día 5) que deban ejecutarse hoy.
    """
    hoy = datetime.now()
    dia_actual = hoy.day
    
    with conectar() as conn:
        cursor = conn.cursor()
        # Buscamos programaciones cuyo día de pago sea hoy
        cursor.execute("SELECT * FROM programacion WHERE dia_pago = ?", (dia_actual,))
        pendientes = cursor.fetchall()
        
        for p in pendientes:
            id_prog, desc, monto, tipo, freq, dia, cuenta_id, ultima_ejec = p
            
            # Verificamos que no se haya ejecutado ya este mes
            mes_actual = hoy.strftime("%Y-%m")
            if ultima_ejec is None or not ultima_ejec.startswith(mes_actual):
                # Registrar el movimiento en la tabla principal
                registrar_movimiento(monto, tipo, cuenta_id, f"Programado: {freq}", desc)
                
                # Actualizar la fecha de última ejecución
                cursor.execute("UPDATE programacion SET ultima_ejecucion = ? WHERE id = ?", 
                               (hoy.date(), id_prog))
        conn.commit()
    
    