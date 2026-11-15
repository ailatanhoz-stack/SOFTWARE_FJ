# =====================================================
# SISTEMA DE GESTIÓN SOFTWARE FJ
# NATALIA LALINDE ROMERO
# GRUPO: 213023_588
# Descripción: Gestión de clientes, servicios y reservas
# =====================================================

#Importo las herramientas que necesito para crear clases abstractas.
from abc import ABC, abstractmethod

#Importo la herramienta que utilizo para registrar fechas y horas.
from datetime import datetime

#Importo logging para guardar los eventos y errores del sistema.
import logging




#Configuro el archivo en el que guardo los eventos y errores del sistema.
logging.basicConfig(
    filename="software_fj.log",  #aqui Indico el nombre del archivo donde guardo los registros.
    level=logging.INFO,          #aqui Establezco el nivel de información que quiero registrar.
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

#aqui Registro en el archivo el inicio del sistema.
logging.info("Sistema Software FJ iniciado correctamente")

#Muestro un mensaje para confirmar que el sistema está preparado.
print("Sistema de gestión Software FJ preparado")





#EXCEPCIONES PERSONALIZADAS DEL SISTEMA



class DatosInvalidosError(Exception):                  #aqui Creo esta excepción para identificar datos incorrectos o incompletos.
    pass

                                                       #Creo esta excepción para indicar que un servicio no está disponible.
class ServicioNoDisponibleError(Exception):
    pass


class ReservaInvalidaError(Exception):                 #Creo esta excepción para controlar los problemas que se presentan al crear o gestionar una reserva.
    pass


class OperacionNoPermitidaError(Exception):            #Creo esta excepción para controlar las operaciones que no están permitidas.
    pass




#CLASE ABSTRACTA ENTIDAD


#Creo una clase abstracta que sirve como base para las entidades del sistema.
class Entidad(ABC):

    #Defino el constructor que inicializa los datos de la entidad.
    def __init__(self, identificador):
        self._identificador = identificador

    #aqui Establezco un método abstracto que las clases hijas deben implementar para mostrar información.
    @abstractmethod
    def mostrar_informacion(self):
        pass






#CLASE CLIENTE


class Cliente(Entidad):

    #aqui se define el constructor con los datos que necesito para crear un cliente.
    def __init__(self, identificador, nombre, correo, telefono):

        #Verifico que el cliente tenga todos los datos obligatorios.
        if not nombre or not correo or not telefono:
            raise DatosInvalidosError(
                "Todos los datos del cliente son obligatorios"
            )

        #Compruebo que el correo tenga los caracteres básicos de una dirección válida.
        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError(
                "El correo electrónico no es válido"
            )

        #Llamo al constructor de Entidad para guardar el identificador heredado.
        super().__init__(identificador)

        #Guardo los datos personales como atributos privados para proteger su acceso directo.
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    #Creo propiedades que me permiten consultar los datos privados del cliente.
    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    #aqui Construyo y devuelvo un texto con la información del cliente.
    def mostrar_informacion(self):
        return (
            f"ID: {self._identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )



# CLASE ABSTRACTA SERVICIO


class Servicio(Entidad):

    #se define el constructor con la información general de cada servicio.
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):

        # Verifico que el servicio tenga un nombre.
        if not nombre:
            raise DatosInvalidosError("El nombre es obligatorio")

        #Compruebo que la tarifa sea numérica y mayor que cero.
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero")

        #Inicializo el identificador heredado desde la clase Entidad.
        super().__init__(identificador)

        #Guardo los datos generales del servicio.
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    #Establezco el método que cada tipo de servicio implementa para calcular su costo.
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        pass

    #Establezco el método que cada servicio implementa para generar su descripción.
    @abstractmethod
    def describir(self):
        pass

    #Establezco el método que cada servicio implementa para validar su duración.
    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    #Calculo el valor final aplicando primero el descuento y después el impuesto.
    def calcular_total(self, duracion, descuento=0, impuesto=0.19):

        #Verifico que los porcentajes de descuento e impuesto estén dentro del rango permitido.
        if not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1")

        if not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1")

        #Multiplico la tarifa base por la duración para obtener el subtotal.
        subtotal = self.tarifa_base * duracion
        #Calculo cuánto dinero representa el descuento aplicado.
        valor_descuento = subtotal * descuento
        #Resto el descuento al subtotal para obtener el valor antes de impuestos.
        total_con_descuento = subtotal - valor_descuento
        #Aplico el impuesto al valor que ya tiene descontado el descuento.
        total = total_con_descuento * (1 + impuesto)

        return total



#SERVICIO 1: RESERVA DE SALAS


class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, capacidad, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo")

        self.capacidad = capacidad

    #Compruebo que la duración de la reserva de sala sea un número positivo.
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero")

    #Calculo el costo de la sala según las horas solicitadas.
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    #Construyo una descripción con el nombre de la sala y su capacidad.
    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas"

    def mostrar_informacion(self):
        return self.describir()



#SERVICIO 2: ALQUILER DE EQUIPOS


class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, tipo_equipo, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not tipo_equipo:
            raise DatosInvalidosError("Debe indicar el tipo de equipo")

        self.tipo_equipo = tipo_equipo

    #Compruebo que la cantidad de días del alquiler sea positiva.
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Los días deben ser mayores que cero")

    #Calculo el costo del equipo según los días de alquiler.
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    #Construyo una descripción con el nombre de la sala y su capacidad.
    def describir(self):
        return f"Equipo: {self.nombre} | Tipo: {self.tipo_equipo}"

    def mostrar_informacion(self):
        return self.describir()



#SERVICIO 3: ASESORÍAS ESPECIALIZADAS


class Asesoria(Servicio):

    def __init__(self, identificador, nombre, tarifa_base, especialidad, disponible=True):

        super().__init__(identificador, nombre, tarifa_base, disponible)

        if not especialidad:
            raise DatosInvalidosError("Debe indicar la especialidad")

        self.especialidad = especialidad

    #Compruebo que la duración de la asesoría sea positiva.
    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores que cero")

    #Calculo el costo de la asesoría según las horas solicitadas.
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self.validar_parametros(duracion)
        return self.calcular_total(duracion, descuento, impuesto)

    #Construyo una descripción con el nombre de la sala y su capacidad.
    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad}"

    def mostrar_informacion(self):
        return self.describir()



#CLASE RESERVA

class Reserva:

    def __init__(self, identificador, cliente, servicio, duracion):

        #Verifico que el objeto recibido corresponda a un cliente válido.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Debe seleccionar un cliente válido")

        #Verifico que el objeto recibido corresponda a un servicio válido.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Debe seleccionar un servicio válido")

        #Compruebo que el servicio esté disponible antes de crear la reserva.
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible")

        #Valido la duración usando las reglas definidas para el tipo de servicio.
        servicio.validar_parametros(duracion)

        self.identificador = identificador
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        #Inicio cada reserva con estado Pendiente hasta que sea confirmada.
        self.estado = "Pendiente"
        #Guardo la fecha y hora exactas en las que creo la reserva.
        self.fecha = datetime.now()

        logging.info(f"Reserva {identificador} creada correctamente")

    #Confirmo la reserva únicamente cuando su estado es Pendiente.
    def confirmar(self):

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        #Actualizo el estado para indicar que la reserva fue confirmada.
        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificador} confirmada")

    #Cancelo la reserva cuando se encuentra Pendiente o Confirmada.
    def cancelar(self):

        if self.estado not in ["Pendiente", "Confirmada"]:
            raise OperacionNoPermitidaError(
                "No se puede cancelar esta reserva"
            )

        #Actualizo el estado para dejar constancia de la cancelación.
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificador} cancelada")

    #Proceso la reserva confirmada y calculo el costo que debe pagar el cliente.
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

            #Cambio el estado cuando el cálculo termina correctamente.
            self.estado = "Procesada"

            logging.info(
                f"Reserva {self.identificador} procesada. Total: {total}"
            )

            return total

        except Exception as error:
            #Registro el error completo y conservo su causa al lanzar la excepción propia.
            logging.exception("Error durante el procesamiento de la reserva")
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error

    #Devuelvo un resumen con los datos principales de la reserva.
    def mostrar_informacion(self):

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado}"
        )



#CLASE ADMINISTRADORA DEL SISTEMA

class SistemaSoftwareFJ:

    def __init__(self):

        #Creo listas internas para almacenar los clientes, servicios y reservas registrados.
        #Inicializo la lista donde almaceno los objetos Cliente.
        self.clientes = []
        #Inicializo la lista donde almaceno los objetos Servicio.
        self.servicios = []
        #Inicializo la lista donde almaceno los objetos Reserva.
        self.reservas = []

    #Registro un cliente después de verificar su tipo y que su identificador no esté repetido.
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto no es un cliente válido")

        for cliente_existente in self.clientes:
            if cliente_existente._identificador == cliente._identificador:
                raise DatosInvalidosError("El identificador del cliente ya existe")

        #Agrego el cliente a la lista después de superar las validaciones.
        self.clientes.append(cliente)

        logging.info(f"Cliente registrado: {cliente.nombre}")

    #Registro un servicio después de verificar su tipo y que su identificador no esté repetido.
    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto no es un servicio válido")

        for servicio_existente in self.servicios:
            if servicio_existente._identificador == servicio._identificador:
                raise DatosInvalidosError("El identificador del servicio ya existe")

        #Agrego el servicio a la lista después de superar las validaciones.
        self.servicios.append(servicio)

        logging.info(f"Servicio registrado: {servicio.nombre}")

    #Creo la reserva, la agrego a la lista y controlo los errores que puedan presentarse.
    def crear_reserva(self, identificador, cliente, servicio, duracion):

        try:
            reserva = Reserva(identificador, cliente, servicio, duracion)
            # Guardo la reserva creada en la lista del sistema.
            self.reservas.append(reserva)

            logging.info(f"Reserva {identificador} agregada al sistema")

            return reserva

        except Exception as error:
            # Registro el problema y lo convierto en una excepción propia de reservas.
            logging.exception("Error al crear una reserva")
            raise ReservaInvalidaError(
                "No se pudo crear la reserva"
            ) from error

    #Recorro la lista y muestro la información de cada cliente registrado.
    def mostrar_clientes(self):

        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    #Recorro la lista y muestro la información de cada servicio registrado.
    def mostrar_servicios(self):

        for servicio in self.servicios:
            print(servicio.mostrar_informacion())

    #Recorro la lista y muestro la información de cada reserva registrada.
    def mostrar_reservas(self):

        for reserva in self.reservas:
            print(reserva.mostrar_informacion())



#PRUEBAS DEL SISTEMA SOFTWARE FJ


#Creo el objeto principal que administra las listas y operaciones del sistema.
sistema = SistemaSoftwareFJ()

print("\n========================================")
print(" PRUEBAS DEL SISTEMA SOFTWARE FJ")
print("========================================")


#En esta prueba registro un cliente con datos válidos.
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


#En esta prueba intento registrar un cliente con un correo incorrecto.
print("\nOPERACIÓN 2: Registro de cliente con correo incorrecto")

try:
    cliente2 = Cliente(
        2, "María López", "mariagmail.com", "3101234567"
    )

    sistema.registrar_cliente(cliente2)

except DatosInvalidosError as error:
    logging.error(f"Operación 2: {error}")
    print("Error controlado:", error)


#en esta prueba intento registrar un cliente al que le falta un dato obligatorio.
print("\nOPERACIÓN 3: Registro de cliente con datos incompletos")

try:
    cliente3 = Cliente(3, "", "ana@gmail.com", "3201234567")
    sistema.registrar_cliente(cliente3)

except DatosInvalidosError as error:
    logging.error(f"Operación 3: {error}")
    print("Error controlado:", error)


#en esta prueba creo y registro un servicio de reserva de sala.
print("\nOPERACIÓN 4: Crear servicio de sala")

try:
    sala1 = ReservaSala(101, "Sala de reuniones", 50000, 15)

    sistema.registrar_servicio(sala1)

    print("Servicio creado:", sala1.describir())

except DatosInvalidosError as error:
    logging.exception("Error en operación 4")
    print("Error:", error)


#En esta prueba creo y registro un servicio de alquiler de equipo.
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


#En esta prueba creo y registro un servicio de asesoría especializada.
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


#En esta prueba intento crear un servicio con una tarifa negativa para comprobar la validación.
print("\nOPERACIÓN 7: Crear servicio con tarifa incorrecta")

try:
    servicio_invalido = ReservaSala(
        104, "Sala pequeña", -50000, 10
    )

    sistema.registrar_servicio(servicio_invalido)

except DatosInvalidosError as error:
    logging.error(f"Operación 7: {error}")
    print("Error controlado:", error)


#En esta prueba creo una reserva válida con el cliente y la sala registrados.
print("\nOPERACIÓN 8: Crear reserva válida")

try:
    reserva1 = sistema.crear_reserva(
        201, cliente1, sala1, 2
    )

    print("Reserva creada:", reserva1.mostrar_informacion())

except ReservaInvalidaError as error:
    logging.exception("Error en operación 8")
    print("Error:", error)


#En esta prueba confirmo la reserva que quedó en estado Pendiente.
print("\nOPERACIÓN 9: Confirmar reserva")

try:
    reserva1.confirmar()

    print("Reserva confirmada correctamente")

except OperacionNoPermitidaError as error:
    logging.error(f"Operación 9: {error}")
    print("Error:", error)


#En esta prueba proceso la reserva confirmada y obtengo su costo total.
print("\nOPERACIÓN 10: Procesar reserva")

try:
    total = reserva1.procesar()

    print(f"Costo total de la reserva: ${total:,.2f}")

except ReservaInvalidaError as error:
    logging.exception("Error en operación 10")
    print("Error:", error)


#En esta prueba intento cancelar una reserva procesada para comprobar que el sistema lo impide.
print("\nOPERACIÓN 11: Cancelar reserva procesada")

try:
    reserva1.cancelar()

except OperacionNoPermitidaError as error:
    logging.error(f"Operación 11: {error}")
    print("Error controlado:", error)


#En esta prueba intento reservar una sala que se encuentra marcada como no disponible.
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


#En esta prueba calculo el costo de la sala aplicando un descuento del 10 % y el impuesto.
print("\nOPERACIÓN 13: Calcular costo con descuento")

try:
    costo_con_descuento = sala1.calcular_costo(
        2, descuento=0.10, impuesto=0.19
    )

    print(f"Costo con descuento: ${costo_con_descuento:,.2f}")

except DatosInvalidosError as error:
    logging.error(f"Operación 13: {error}")
    print("Error:", error)


#En esta prueba ingreso una duración negativa para comprobar que el sistema la rechaza.
print("\nOPERACIÓN 14: Cálculo con duración incorrecta")

try:
    costo = equipo1.calcular_costo(-3)

except DatosInvalidosError as error:
    logging.error(f"Operación 14: {error}")
    print("Error controlado:", error)



#RESUMEN FINAL DEL SISTEMA


print("\n========================================")
print(" RESUMEN DEL SISTEMA")
print("========================================")

print("\nCLIENTES REGISTRADOS:")
sistema.mostrar_clientes()

print("\nSERVICIOS REGISTRADOS:")
sistema.mostrar_servicios()

print("\nRESERVAS REGISTRADAS:")
sistema.mostrar_reservas()



#DEMOSTRACIÓN DE TRY, EXCEPT, ELSE Y FINALLY


print("\nPRUEBA DE MANEJO DE EXCEPCIONES")

try:
    print("Consultando cantidad de clientes...")
    cantidad = len(sistema.clientes)

except Exception as error:
    logging.exception("Error al consultar los clientes")
    print("Se presentó un error:", error)

else:
    #Ejecuto este bloque solamente si la consulta no generó excepciones.
    print("Consulta realizada correctamente")
    print("Cantidad de clientes:", cantidad)

finally:
    #Ejecuto este bloque tanto si hubo error como si la consulta fue exitosa.
    print("Finalizó la consulta, el sistema continúa funcionando")


#Registro que todas las pruebas del sistema han finalizado.
logging.info("Pruebas del sistema Software FJ finalizadas")

print("\n========================================")