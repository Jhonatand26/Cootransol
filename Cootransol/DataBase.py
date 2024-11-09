import sqlite3

# Conexión a la base de datos
# Conexión a la base de datos
def conectar_db(retornar_cursor=False):
    conexion = sqlite3.connect("D:/Asus/Escritorio/Psergio/cootransol.db")
    if retornar_cursor:
        cursor = conexion.cursor()
        return conexion, cursor  # Retorna tanto la conexión como el cursor
    else:
        return conexion  # Retorna solo la conexión

    # Crear tabla Vehiculos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vehiculos (
            idVehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            nro_interno INTEGER,
            placa TEXT,
            estado TEXT,
            modelo TEXT,
            vigencia_soat TEXT,
            vigencia_tarjeta TEXT,
            vigencia_poliza TEXT,
            vigencia_tecnomecanica TEXT,
            idConductor INTEGER,
            FOREIGN KEY(idConductor) REFERENCES Conductores(identificacion)
        )
    ''')

    # Crear tabla Conductores con identificación, nombre y vigencia_licencia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Conductores (
            identificacion INTEGER PRIMARY KEY,
            nombre TEXT,
            vigencia_licencia TEXT
        )
    ''')

    # Crear tabla Movimientos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Movimientos (
            idMovimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            vueltas INTEGER,
            montoPago REAL,
            rutaAsignada TEXT,
            placaVehiculo TEXT,
            numeroInternoVehiculo INTEGER,
            horaInicio TEXT,
            horaFin TEXT
        )
    ''')

    conexion.commit()
    return conexion

# Función para cerrar la conexión a la base de datos
def cerrar_db(conexion):
    conexion.close()
    
# Método para agregar un vehículo con id_conductor
def agregar_vehiculo(nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica, id_conductor):
    conexion, cursor = conectar_db(retornar_cursor=True)  # Retorna tanto conexión como cursor

    cursor.execute('''
        INSERT INTO Vehiculos (nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica, idConductor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica, id_conductor))

    conexion.commit()
    conexion.close()

# Metodo para eliminar un vehículo
def eliminar_vehiculo_db(placa):
    # Este código va en `DataBase.py`
    conexion = sqlite3.connect("cootransol.db")
    cursor = conexion.cursor()

    # Desvincular el vehículo del conductor
    cursor.execute("UPDATE Vehiculos SET idConductor = NULL WHERE placa = ?", (placa,))
    # Eliminar el vehículo
    cursor.execute("DELETE FROM Vehiculos WHERE placa = ?", (placa,))

    conexion.commit()
    conexion.close()

# Método para agregar un conductor
def agregar_conductor(identificacion, nombre, vigencia_licencia):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO Conductores (identificacion, nombre, vigencia_licencia)
        VALUES (?, ?, ?)
    ''', (identificacion, nombre, vigencia_licencia))  # Asegúrate de pasar los tres valores
    conexion.commit()
    cerrar_db(conexion)

# Método para eliminar un conductor
def eliminar_conductor_db(identificacion):

    # Este código va en `DataBase.py`
    conexion = sqlite3.connect("cootransol.db")
    cursor = conexion.cursor()

    # Desvincular el conductor del vehículo
    cursor.execute("UPDATE Vehiculos SET idConductor = NULL WHERE idConductor = ?", (identificacion,))
    # Eliminar el conductor
    cursor.execute("DELETE FROM Conductores WHERE identificacion = ?", (identificacion,))

    conexion.commit()
    conexion.close()

# Método para obtener conductores que no tienen vehículo asignado
def obtener_conductores_disponibles():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT identificacion, nombre 
        FROM Conductores 
        WHERE identificacion NOT IN (SELECT idConductor FROM Vehiculos WHERE idConductor IS NOT NULL)
    ''')

    conductores_disponibles = cursor.fetchall()
    cerrar_db(conexion)
    return conductores_disponibles

# Método para verificar si un conductor ya tiene un vehículo asignado
def verificar_conductor_disponible(idConductor):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT COUNT(*) FROM Vehiculos WHERE idConductor = ?
    ''', (idConductor,))

    resultado = cursor.fetchone()[0]
    cerrar_db(conexion)

    # Si el resultado es 0, el conductor está disponible
    return resultado == 0


# Método para registrar un movimiento
def registrar_movimiento(fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, numeroInternoVehiculo, horaInicio, horaFin):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute('''
        INSERT INTO Movimientos (fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, numeroInternoVehiculo, horaInicio, horaFin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, numeroInternoVehiculo, horaInicio, horaFin))

    conexion.commit()
    cerrar_db(conexion)

# Método para consultar el historial de movimientos de un conductor
def consultar_historial_conductor(idConductor):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT * FROM Movimientos
        WHERE numeroInternoVehiculo IN (
            SELECT nro_interno FROM Vehiculos
            WHERE idVehiculo IN (
                SELECT idVehiculo FROM Conductores WHERE idConductor = ?
            )
        )
    ''', (idConductor,))

    movimientos = cursor.fetchall()
    cerrar_db(conexion)
    return movimientos
if __name__ == "__main__":
    conectar_db()
    print("Tablas creadas exitosamente.")
