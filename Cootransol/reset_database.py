import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect("cootransol.db")
cursor = conexion.cursor()

# Eliminar la tabla Conductores si existe
cursor.execute("DROP TABLE IF EXISTS Conductores")
conexion.commit()

# Crear la tabla nuevamente con la columna 'identificacion'
cursor.execute('''
    CREATE TABLE Conductores (
        identificacion INTEGER PRIMARY KEY,
        nombre TEXT,
        vigencia_licencia TEXT
    )
''')
conexion.commit()
conexion.close()

print("Tabla 'Conductores' eliminada y creada nuevamente con la columna 'identificacion'")
