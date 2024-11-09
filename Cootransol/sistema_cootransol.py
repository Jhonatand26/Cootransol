from datetime import datetime
from enum import Enum
from DataBase import agregar_vehiculo, agregar_conductor, registrar_movimiento, consultar_historial_conductor  # Importar funciones al inicio

# Enum for the routes
class Ruta(Enum):
    Ruta1 = "La sirena"
    Ruta2 = "Los chorros"
    Ruta3 = "La estrella"
    Ruta4 = "La cruz"
    Ruta5 = "El Jordán"
    Ruta6 = "El mortiñal"
    Ruta7 = "Siloé"
    Ruta8 = "Las palmas"
    Ruta9 = "Nápoles"
    Ruta10 = "4 esquinas"
    Ruta11 = "Menga"

# Clase Usuario
class Usuario:
    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol

    def iniciarSesion(self, username, password):
        # Lógica para autenticación
        return self.username == username and self.password == password

    def consultarHistorialConductor(self, id_conductor):
        # Llamar a la función de DataBase para consultar el historial de movimientos
        return consultar_historial_conductor(id_conductor)

# Clase Administrador
class Administrador(Usuario):
    def modificarRuta(self, idMovimiento, nuevaRuta):
        # Lógica para modificar una ruta asignada
        movimiento = registrar_movimiento(idMovimiento)
        if movimiento:
            movimiento['rutaAsignada'] = nuevaRuta
            registrar_movimiento(movimiento)  # Actualizar base de datos
            return True
        return False
    
    def agregarVehiculo(self, nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica):
        # Llamar a la función de agregar vehículo en la base de datos
        agregar_vehiculo(nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica)
        return "Vehículo agregado correctamente."

    def agregarConductor(self,id, nombre, vigencia_licencia):
        # Llamar a la función de agregar conductor en la base de datos
        agregar_conductor(id,nombre, vigencia_licencia)
        return "Conductor agregado correctamente."

    def agregarRuta(self, nuevaRuta):
        # Aquí iría la lógica para agregar una nueva ruta, si es necesario
        pass

# Clase Despachador
class Despachador(Usuario):
    def gestionarPago(self, idConductor, montoPago):
        # Registrar el pago de un conductor
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        registrar_movimiento(fecha_actual, 0, montoPago, None, None, idConductor, None, None)
        return "Pago registrado correctamente."

    def asignarRuta(self, idConductor, ruta):
        # Asignar una nueva ruta a un conductor
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_inicio = datetime.now().strftime("%H:%M:%S")
        registrar_movimiento(fecha_actual, 0, 0, ruta, None, idConductor, hora_inicio, None)
        return "Ruta asignada correctamente."

# Clase Vehiculo
class Vehiculo:
    def __init__(self, nro_interno, placa, UltMant, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica):
        self.nro_interno = nro_interno
        self.placa = placa
        self.ultMant = UltMant
        self.modelo = modelo
        self.vigencia_soat = vigencia_soat
        self.vigencia_tarjeta = vigencia_tarjeta
        self.vigencia_poliza = vigencia_poliza
        self.vigencia_tecnomecanica = vigencia_tecnomecanica

    def agregarVehiculo(self):
        # Llamar a la función para agregar el vehículo en la base de datos
        agregar_vehiculo(self.nro_interno, self.placa, self.ultMant, self.modelo, self.vigencia_soat, self.vigencia_tarjeta, self.vigencia_poliza, self.vigencia_tecnomecanica)
        return "Vehículo agregado."

    def modificarVehiculo(self, idVehiculo):
        # Aquí iría la lógica para modificar un vehículo, si es necesario
        pass

# Clase Conductor
class Conductor:
    def __init__(self, idConductor, nombre, vigencia_licencia):
        self.idConductor = idConductor
        self.nombre = nombre
        self.vigencia_licencia = vigencia_licencia

    def consultarHistorial(self):
        # Consultar el historial de movimientos del conductor
        return consultar_historial_conductor(self.idConductor)

# Clase Movimiento
class Movimiento:
    def __init__(self, idMovimiento, fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, numeroInternoVehiculo, horaInicio, horaFin):
        self.idMovimiento = idMovimiento
        self.fecha = fecha
        self.vueltas = vueltas
        self.montoPago = montoPago
        self.rutaAsignada = rutaAsignada
        self.placaVehiculo = placaVehiculo
        self.numeroInternoVehiculo = numeroInternoVehiculo
        self.horaInicio = horaInicio
        self.horaFin = horaFin

    def registrarMovimiento(self):
        # Llamar a la función para registrar el movimiento en la base de datos
        registrar_movimiento(self.fecha, self.vueltas, self.montoPago, self.rutaAsignada, self.placaVehiculo, self.numeroInternoVehiculo, self.horaInicio, self.horaFin)
        return "Movimiento registrado."


