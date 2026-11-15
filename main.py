# =====================================================
# SISTEMA DE GESTIÓN SOFTWARE FJ
# NATALIA LALINDE ROMERO
# GRUPO: 213023_588
# Descripción: Gestión de clientes, servicios y reservas
# =====================================================

# Importar herramientas para trabajar con clases abstractas
from abc import ABC, abstractmethod

# Importar herramientas para manejar fechas
from datetime import datetime

# Importar herramientas para registrar eventos y errores
import logging




# Configurar el archivo donde se guardarán los eventos y errores
logging.basicConfig(
    filename="software_fj.log",  # Nombre del archivo de registro
    level=logging.INFO,          # Registrar información, advertencias y errores
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Registrar el inicio del sistema
logging.info("Sistema Software FJ iniciado correctamente")

# Mostrar un mensaje de confirmación
print("Sistema de gestión Software FJ preparado")




# =====================================================
# EXCEPCIONES PERSONALIZADAS DEL SISTEMA
# =====================================================

# Excepción para datos incorrectos o incompletos
class DatosInvalidosError(Exception):
    pass


# Excepción cuando un servicio no está disponible
class ServicioNoDisponibleError(Exception):
    pass


# Excepción cuando una reserva presenta algún problema
class ReservaInvalidaError(Exception):
    pass


# Excepción para operaciones que no están permitidas
class OperacionNoPermitidaError(Exception):
    pass




# =====================================================
# CLASE ABSTRACTA ENTIDAD
# =====================================================

# Crear una clase abstracta para las entidades del sistema
class Entidad(ABC):

    # Método constructor de la clase
    def __init__(self, identificador):
        self._identificador = identificador

    # Método abstracto para mostrar información
    @abstractmethod
    def mostrar_informacion(self):
        pass





# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Entidad):

    # Constructor de la clase Cliente
    def __init__(self, identificador, nombre, correo, telefono):

        # Validar que los datos sean obligatorios
        if not nombre or not correo or not telefono:
            raise DatosInvalidosError(
                "Todos los datos del cliente son obligatorios"
            )

        # Validar el formato básico del correo
        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError(
                "El correo electrónico no es válido"
            )

        # Inicializar la clase padre
        super().__init__(identificador)

        # Guardar los datos personales de forma privada
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    # Métodos para consultar los datos privados
    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Mostrar la información del cliente
    def mostrar_informacion(self):
        return (
            f"ID: {self._identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(Entidad):

    # Constructor de la clase Servicio
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):

        # Validar el nombre del servicio
        if not nombre:
            raise DatosInvalidosError("El nombre es obligatorio")

        # Validar la tarifa
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero")

        super().__init__(identificador)

        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    # Método abstracto para calcular costos
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        pass

    # Método abstracto para describir el servicio
    @abstractmethod
    def describir(self):
        pass

    # Método abstracto para validar parámetros
    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    # Método para calcular el costo con descuento e impuesto
    def calcular_total(self, duracion, descuento=0, impuesto=0.19):

        # Validar los porcentajes
        if not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1")

        if not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1")

        subtotal = self.tarifa_base * duracion
        valor_descuento = subtotal * descuento
        total_con_descuento = subtotal - valor_descuento
        total = total_con_descuento * (1 + impuesto)

        return total


# =====================================================
# SERVICIO 1: RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, capacidad, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo")

        self.capacidad = capacidad

    # Validar la duración de la reserva
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero")

    # Calcular el costo por horas
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    # Describir el servicio
    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas"

    def mostrar_informacion(self):
        return self.describir()


# =====================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, tipo_equipo, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not tipo_equipo:
            raise DatosInvalidosError("Debe indicar el tipo de equipo")

        self.tipo_equipo = tipo_equipo

    # Validar la cantidad de días
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Los días deben ser mayores que cero")

    # Calcular el costo del alquiler
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    # Describir el servicio
    def describir(self):
        return f"Equipo: {self.nombre} | Tipo: {self.tipo_equipo}"

    def mostrar_informacion(self):
        return self.describir()


# =====================================================
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# =====================================================

class Asesoria(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, especialidad, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not especialidad:
            raise DatosInvalidosError("Debe indicar la especialidad")

        self.especialidad = especialidad

    # Validar la duración de la asesoría
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero")

    # Calcular el costo de la asesoría
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    # Describir el servicio
    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad}"

    def mostrar_informacion(self):
        return self.describir()


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    def __init__(self, identificador, cliente, servicio, duracion):

        # Verificar que se haya seleccionado un cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Debe seleccionar un cliente válido")

        # Verificar que se haya seleccionado un servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Debe seleccionar un servicio válido")

        # Verificar la disponibilidad del servicio
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible")

        # Validar la duración
        servicio.validar_parametros(duracion)

        self.identificador = identificador
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.fecha = datetime.now()

        logging.info(f"Reserva {identificador} creada correctamente")

    # Confirmar una reserva
    def confirmar(self):

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificador} confirmada")

    # Cancelar una reserva
    def cancelar(self):

        if self.estado not in ["Pendiente", "Confirmada"]:
            raise OperacionNoPermitidaError(
                "No se puede cancelar esta reserva"
            )

        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificador} cancelada")

    # Procesar una reserva y calcular su costo
    def procesar(self, descuento=0, impuesto=0.19):

        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada para procesarse"
            )

        try:
            total = self.servicio.calcular_costo(
                self.duracion, descuento, impuesto
            )

            if not isinstance(total, (int, float)) or total < 0:
                raise DatosInvalidosError("El cálculo del costo no es válido")

            self.estado = "Procesada"

            logging.info(
                f"Reserva {self.identificador} procesada. Total: {total}"
            )

            return total

        except Exception as error:
            logging.exception("Error durante el procesamiento de la reserva")
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error

    # Mostrar la información de la reserva
    def mostrar_informacion(self):

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado}"
        )


# =====================================================
# CLASE ADMINISTRADORA DEL SISTEMA
# =====================================================

class SistemaSoftwareFJ:

    def __init__(self):

        # Listas internas para almacenar los objetos
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # Registrar un cliente
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto no es un cliente válido")

        for cliente_existente in self.clientes:
            if cliente_existente._identificador == cliente._identificador:
                raise DatosInvalidosError("El identificador del cliente ya existe")

        self.clientes.append(cliente)

        logging.info(f"Cliente registrado: {cliente.nombre}")

    # Registrar un servicio
    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto no es un servicio válido")

        for servicio_existente in self.servicios:
            if servicio_existente._identificador == servicio._identificador:
                raise DatosInvalidosError("El identificador del servicio ya existe")

        self.servicios.append(servicio)

        logging.info(f"Servicio registrado: {servicio.nombre}")

    # Crear una reserva
    def crear_reserva(self, identificador, cliente, servicio, duracion):

        try:
            reserva = Reserva(identificador, cliente, servicio, duracion)
            self.reservas.append(reserva)

            logging.info(f"Reserva {identificador} agregada al sistema")

            return reserva

        except Exception as error:
            logging.exception("Error al crear una reserva")
            raise ReservaInvalidaError(
                "No se pudo crear la reserva"
            ) from error

    # Mostrar los clientes registrados
    def mostrar_clientes(self):

        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    # Mostrar los servicios registrados
    def mostrar_servicios(self):

        for servicio in self.servicios:
            print(servicio.mostrar_informacion())

    # Mostrar las reservas registradas
    def mostrar_reservas(self):

        for reserva in self.reservas:
            print(reserva.mostrar_informacion())


# =====================================================
# PRUEBAS DEL SISTEMA SOFTWARE FJ
# =====================================================

# Crear el objeto principal del sistema
sistema = SistemaSoftwareFJ()

print("\n========================================")
print(" PRUEBAS DEL SISTEMA SOFTWARE FJ")
print("========================================")


# OPERACIÓN 1: Registrar un cliente válido
print("\nOPERACIÓN 1: Registro de cliente válido")

try:
    cliente1 = Cliente(
        1, "Carlos Ramírez", "carlos@gmail.com", "3001234567"
    )

    sistema.registrar_cliente(cliente1)

    print("Cliente registrado:", cliente1.nombre)

except DatosInvalidosError as error:
    logging.exception("Error en operación 1")
    print("No se pudo registrar el cliente:", error)


# OPERACIÓN 2: Registrar un cliente con correo incorrecto
print("\nOPERACIÓN 2: Registro de cliente con correo incorrecto")

try:
    cliente2 = Cliente(
        2, "María López", "mariagmail.com", "3101234567"
    )

    sistema.registrar_cliente(cliente2)

except DatosInvalidosError as error:
    logging.error(f"Operación 2: {error}")
    print("Error controlado:", error)


# OPERACIÓN 3: Registrar un cliente con datos incompletos
print("\nOPERACIÓN 3: Registro de cliente con datos incompletos")

try:
    cliente3 = Cliente(3, "", "ana@gmail.com", "3201234567")
    sistema.registrar_cliente(cliente3)

except DatosInvalidosError as error:
    logging.error(f"Operación 3: {error}")
    print("Error controlado:", error)


# OPERACIÓN 4: Crear un servicio de reserva de sala
print("\nOPERACIÓN 4: Crear servicio de sala")

try:
    sala1 = ReservaSala(101, "Sala de reuniones", 50000, 15)

    sistema.registrar_servicio(sala1)

    print("Servicio creado:", sala1.describir())

except DatosInvalidosError as error:
    logging.exception("Error en operación 4")
    print("Error:", error)


# OPERACIÓN 5: Crear un servicio de alquiler de equipo
print("\nOPERACIÓN 5: Crear servicio de alquiler de equipo")

try:
    equipo1 = AlquilerEquipo(
        102, "Computador portátil", 80000, "Computador"
    )

    sistema.registrar_servicio(equipo1)

    print("Servicio creado:", equipo1.describir())

except DatosInvalidosError as error:
    logging.exception("Error en operación 5")
    print("Error:", error)


# OPERACIÓN 6: Crear un servicio de asesoría
print("\nOPERACIÓN 6: Crear servicio de asesoría")

try:
    asesoria1 = Asesoria(
        103, "Asesoría tecnológica", 100000, "Tecnología"
    )

    sistema.registrar_servicio(asesoria1)

    print("Servicio creado:", asesoria1.describir())

except DatosInvalidosError as error:
    logging.exception("Error en operación 6")
    print("Error:", error)


# OPERACIÓN 7: Intentar crear un servicio con tarifa inválida
print("\nOPERACIÓN 7: Crear servicio con tarifa incorrecta")

try:
    servicio_invalido = ReservaSala(
        104, "Sala pequeña", -50000, 10
    )

    sistema.registrar_servicio(servicio_invalido)

except DatosInvalidosError as error:
    logging.error(f"Operación 7: {error}")
    print("Error controlado:", error)


# OPERACIÓN 8: Crear una reserva válida
print("\nOPERACIÓN 8: Crear reserva válida")

try:
    reserva1 = sistema.crear_reserva(
        201, cliente1, sala1, 2
    )

    print("Reserva creada:", reserva1.mostrar_informacion())

except ReservaInvalidaError as error:
    logging.exception("Error en operación 8")
    print("Error:", error)


# OPERACIÓN 9: Confirmar la reserva
print("\nOPERACIÓN 9: Confirmar reserva")

try:
    reserva1.confirmar()

    print("Reserva confirmada correctamente")

except OperacionNoPermitidaError as error:
    logging.error(f"Operación 9: {error}")
    print("Error:", error)


# OPERACIÓN 10: Procesar la reserva y calcular su costo
print("\nOPERACIÓN 10: Procesar reserva")

try:
    total = reserva1.procesar()

    print(f"Costo total de la reserva: ${total:,.2f}")

except ReservaInvalidaError as error:
    logging.exception("Error en operación 10")
    print("Error:", error)


# OPERACIÓN 11: Intentar cancelar una reserva ya procesada
print("\nOPERACIÓN 11: Cancelar reserva procesada")

try:
    reserva1.cancelar()

except OperacionNoPermitidaError as error:
    logging.error(f"Operación 11: {error}")
    print("Error controlado:", error)


# OPERACIÓN 12: Intentar crear una reserva con servicio no disponible
print("\nOPERACIÓN 12: Reserva de servicio no disponible")

try:
    sala_no_disponible = ReservaSala(
        105, "Sala ocupada", 60000, 10, False
    )

    sistema.registrar_servicio(sala_no_disponible)

    reserva2 = sistema.crear_reserva(
        202, cliente1, sala_no_disponible, 2
    )

except ReservaInvalidaError as error:
    logging.exception("Operación 12: reserva no válida")
    print("Error controlado:", error)


# OPERACIÓN 13: Probar el uso de descuento
print("\nOPERACIÓN 13: Calcular costo con descuento")

try:
    costo_con_descuento = sala1.calcular_costo(
        2, descuento=0.10, impuesto=0.19
    )

    print(f"Costo con descuento: ${costo_con_descuento:,.2f}")

except DatosInvalidosError as error:
    logging.error(f"Operación 13: {error}")
    print("Error:", error)


# OPERACIÓN 14: Intentar calcular un costo con duración inválida
print("\nOPERACIÓN 14: Cálculo con duración incorrecta")

try:
    costo = equipo1.calcular_costo(-3)

except DatosInvalidosError as error:
    logging.error(f"Operación 14: {error}")
    print("Error controlado:", error)


# =====================================================
# RESUMEN FINAL DEL SISTEMA
# =====================================================

print("\n========================================")
print(" RESUMEN DEL SISTEMA")
print("========================================")

print("\nCLIENTES REGISTRADOS:")
sistema.mostrar_clientes()

print("\nSERVICIOS REGISTRADOS:")
sistema.mostrar_servicios()

print("\nRESERVAS REGISTRADAS:")
sistema.mostrar_reservas()


# =====================================================
# DEMOSTRACIÓN DE TRY, EXCEPT, ELSE Y FINALLY
# =====================================================

print("\nPRUEBA DE MANEJO DE EXCEPCIONES")

try:
    print("Consultando cantidad de clientes...")
    cantidad = len(sistema.clientes)

except Exception as error:
    logging.exception("Error al consultar los clientes")
    print("Se presentó un error:", error)

else:
    print("Consulta realizada correctamente")
    print("Cantidad de clientes:", cantidad)

finally:
    print("Finalizó la consulta, el sistema continúa funcionando")


# Registrar la finalización de las pruebas
logging.info("Pruebas del sistema Software FJ finalizadas")

print("\n========================================")