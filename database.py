import sqlite3

def conectar():
    """Establece la conexión con el archivo de base de datos."""
    return sqlite3.connect("finanzas_pro.db")

def crear_tablas():
    """Crea la estructura necesaria para el CRUD y los periodos."""
    with conectar() as conn:
        cursor = conn.cursor()

        # Tabla de Monedas (Requerimiento de múltiples divisas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monedas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                simbolo TEXT NOT NULL
            )
        ''')

        # Tabla de Cuentas (Plataformas: Efectivo, Banco, Tenpo, MACH, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                moneda_id INTEGER,
                FOREIGN KEY (moneda_id) REFERENCES monedas (id)
            )
        ''')

        # Tabla de Transacciones (Con mensaje opcional)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT CURRENT_DATE,
                descripcion TEXT, -- Mensaje opcional
                monto REAL NOT NULL,
                tipo TEXT CHECK(tipo IN ('Ingreso', 'Egreso')),
                cuenta_id INTEGER,
                categoria TEXT NOT NULL,
                FOREIGN KEY (cuenta_id) REFERENCES cuentas (id)
            )
        ''')

        # Tabla de Programación (Para gastos/ingresos periódicos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT,
                monto REAL NOT NULL,
                tipo TEXT CHECK(tipo IN ('Ingreso', 'Egreso')),
                frecuencia TEXT, -- Semanal, Mensual
                dia_pago INTEGER, 
                cuenta_id INTEGER,
                ultima_ejecucion DATE,
                FOREIGN KEY (cuenta_id) REFERENCES cuentas (id)
            )
        ''')

        # Datos iniciales de configuración
        cursor.execute("INSERT OR IGNORE INTO monedas (nombre, simbolo) VALUES ('Peso Chileno', 'CLP')")
        plataformas = [('Efectivo', 1), ('Banco Estado', 1), ('MACH', 1), ('Tenpo', 1), ('Mercado Pago', 1)]
        cursor.executemany("INSERT OR IGNORE INTO cuentas (nombre, moneda_id) VALUES (?, ?)", plataformas)
        conn.commit()

if __name__ == "__main__":
    crear_tablas()
    print("✅ Base de datos lista.")