import sqlite3

def conectar():
    """Establece conexión con la base de datos."""
    return sqlite3.connect("finanzas_pro.db")

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. Tabla de Monedas (Para soportar CLP, USD, EUR, etc.) 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monedas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            simbolo TEXT NOT NULL,
            tasa_respecto_clp REAL DEFAULT 1.0
        )
    ''')

    # 2. Tabla de Cuentas (Efectivo, Banco, Tenpo, MACH, etc.) 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuentas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            moneda_id INTEGER,
            FOREIGN KEY (moneda_id) REFERENCES monedas (id)
        )
    ''')

    # 3. Tabla de Transacciones (El corazón del CRUD) 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE DEFAULT CURRENT_DATE,
            descripcion TEXT, -- Opcional según requerimiento 
            monto REAL NOT NULL,
            tipo TEXT CHECK(tipo IN ('Ingreso', 'Egreso')),
            cuenta_id INTEGER,
            categoria TEXT NOT NULL,
            FOREIGN KEY (cuenta_id) REFERENCES cuentas (id)
        )
    ''')

    # 4. Tabla de Programación (Para gastos/ingresos periódicos) 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS programacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            monto REAL NOT NULL,
            tipo TEXT CHECK(tipo IN ('Ingreso', 'Egreso')),
            frecuencia TEXT, -- 'Semanal', 'Mensual'
            dia_pago INTEGER, -- Ejemplo: 5 para los días 5 de cada mes
            cuenta_id INTEGER,
            ultima_ejecucion DATE,
            FOREIGN KEY (cuenta_id) REFERENCES cuentas (id)
        )
    ''')

    # Datos iniciales para que el programa no esté vacío
    cursor.execute("INSERT OR IGNORE INTO monedas (nombre, simbolo, tasa_respecto_clp) VALUES ('Peso Chileno', 'CLP', 1.0)")
    cursor.execute("INSERT OR IGNORE INTO cuentas (nombre, moneda_id) VALUES ('Efectivo', 1), ('Banco Estado', 1), ('MACH', 1), ('Tenpo', 1)")

    conexion.commit()
    conexion.close()
    print("Base de datos 'finanzas_pro.db' creada y configurada con éxito.")

if __name__ == "__main__":
    crear_tablas()