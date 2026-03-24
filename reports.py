import sqlite3
import matplotlib.pyplot as plt

def generar_grafico_gastos():
    """Genera un gráfico de torta con los gastos por categoría."""
    try:
        conexion = sqlite3.connect("finanzas_pro.db")
        cursor = conexion.cursor()
        
        # Agrupamos los egresos por categoría para el gráfico
        cursor.execute("""
            SELECT categoria, SUM(monto) 
            FROM transacciones 
            WHERE tipo = 'Egreso' 
            GROUP BY categoria
        """)
        datos = cursor.fetchall()
        conexion.close()

        if not datos:
            return False

        categorias = [d[0] for d in datos]
        montos = [d[1] for d in datos]

        # Configuración estética del gráfico
        plt.figure(figsize=(6, 5), facecolor='#2b2b2b' if plt.rcParams['axes.facecolor'] == 'black' else 'white')
        plt.pie(montos, labels=categorias, autopct='%1.1f%%', startangle=140, textprops={'color':"gray"})
        plt.title("Distribución de Gastos", color="gray", fontsize=16)
        
        # Guardamos la imagen temporalmente
        plt.savefig("temp_reporte.png", transparent=True)
        plt.close()
        return True
    except Exception as e:
        print(f"Error al generar gráfico: {e}")
        return False