"""
This module acts as a facade pattern that coordinates
all the subsystems of the Library Management System.

Responsibilities:
- Manage inventories (general and ordered)
- Coordinate loans and returns
- Manage reservations and waiting queues
- Manage users
- Coordinate shelving
"""

from models import Libro, Usuario, Prestamo, Reserva, Estante
from controllers.listas.inventario_general import InventarioGeneral
from controllers.listas.inventario_ordenado import InventarioOrdenado
from controllers.estructuras.pila_historial import PilaHistorial
from controllers.estructuras.cola_reservas import ColaReservas
from controllers.busqueda.busqueda_binaria import busqueda_binaria_por_isbn
from datetime import datetime, timedelta

class GestorBiblioteca:
    """
    Main class that coordinates the entire library management system.
    
    Implements the Facade pattern to simplify access to subsystems.
    
    Attributes:
        inventario_general (InventarioGeneral): Unordered list of books.
        inventario_ordenado (InventarioOrdenado): Ordered list of books by ISBN.
        usuarios (dict): Dictionary of users by ID.
        colas_reservas (dict): Reservation queues by ISBN.
        estantes (dict): Dictionary of shelves by ID.
        contador_prestamos (int): Counter to generate loan IDs.
        contador_reservas (int): Counter to generate reservation IDs.
    """
    def __init__(self):
        """Initializes the library manager."""
        # Inventories
        self.inventario_general = InventarioGeneral()
        self.inventario_ordenado = InventarioOrdenado()
        
        # Usuarios (dict: {id: Usuario})
        self.usuarios = {}
        
        # Colas de reservas por libro (dict: {isbn: ColaReservas})
        self.colas_reservas = {}
        
        # Estantes (dict: {id: Estante})
        self.estantes = {}
        
        # Contadores para IDs
        self.contador_prestamos = 1
        self.contador_reservas = 1

    # Gestión de Libros

    def agregar_libro(self, libro):
        """
        Adds a book to both inventories.
        
        Args:
            libro (Libro): Book object to add.
        
        Returns:
            bool: True if added successfully.
        """
        # Agregar a inventario general
        if not self.inventario_general.agregar_libro(libro):
            return False
        
        # Agregar a inventario ordenado
        if not self.inventario_ordenado.agregar_libro(libro):
            self.inventario_general.eliminar_libro(libro.isbn)
            return False
        
        return True
    
    def buscar_libro_por_isbn(self, isbn):
        """
        Search for a book by ISBN in the sorted inventory (binary search).
        
        Args:
            isbn (str): Book ISBN.
        
        Returns:
            Libro|None: Found book or None.
        """
        libro, _ = busqueda_binaria_por_isbn(
            self.inventario_ordenado.obtener_libros(), 
            isbn
        )
        return libro
    
    def buscar_libros_por_titulo(self, titulo):
        """
        Search for books by title (linear search).
        
        Args:
            titulo (str): Title or part of the title.
        
        Returns:
            list: List of found books.
        """
        return self.inventario_general.buscar_por_titulo(titulo)
    
    def buscar_libros_por_autor(self, autor):
        """
        Search for books by author (linear search).
        
        Args:
            autor (str): Author or part of the name.
        
        Returns:
            list: List of found books.
        """
        return self.inventario_general.buscar_por_autor(autor)
    
    def eliminar_libro(self, isbn):
        """
        Removes a book from both inventories.
        
        Args:
            isbn (str): ISBN of the book to remove.
        
        Returns:
            bool: True if removed successfully.
        """
        result1 = self.inventario_general.eliminar_libro(isbn)
        result2 = self.inventario_ordenado.eliminar_libro(isbn)
        return result1 and result2
    
    def obtener_todos_los_libros(self):
        """Gets all books from the inventory."""
        return self.inventario_general.obtener_libros()
    
    # Gestión de Usuarios

    def agregar_usuario(self, usuario):
        """
        Add a user to the system.
        
        Args:
            usuario (Usuario): User object to add.
        
        Returns:
            bool: True if added successfully.
        """
        if usuario.id in self.usuarios:
            return False
        
        # Inicializar historial de préstamos
        usuario.historial_prestamos = PilaHistorial(usuario.id)
        self.usuarios[usuario.id] = usuario
        return True
    
    def buscar_usuario(self, usuario_id):
        """
        Search for a user by ID.
        
        Args:
            usuario_id (str): User ID.
        
        Returns:
            Usuario|None: Found user or None.
        """
        return self.usuarios.get(usuario_id)
    
    def eliminar_usuario(self, usuario_id):
        """
        Removes a user from the system.
        
        Args:
            usuario_id (str): ID of the user to remove.
        
        Returns:
            bool: True if removed successfully.
        """
        if usuario_id in self.usuarios:
            del self.usuarios[usuario_id]
            return True
        return False
    
    def listar_usuarios(self):
        """Gets the list of all users."""
        return list(self.usuarios.values())
    
    # Gestión de Préstamos

    def realizar_prestamo(self, usuario_id, isbn, dias_prestamo=15):
        """
        Loan a book to a user.
        
        Args:
            usuario_id (str): User ID.
            isbn (str): Book ISBN.
            dias_prestamo (int, optional): Duration in days. Default: 15.
        
        Returns:
            tuple: (bool, message) indicating success and descriptive message.
        """
        # Verificar usuario
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Verificar libro
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            return False, "Libro no encontrado"
        
        # Verificar disponibilidad
        if not libro.esta_disponible():
            return False, f"Libro no disponible (Stock: {libro.cantidad_disponible})"
        
        # Reducir stock
        libro.cantidad_disponible -= 1
        
        # Crear préstamo
        prestamo_id = f"P{self.contador_prestamos:04d}"
        self.contador_prestamos += 1
        
        fecha_prestamo = datetime.now()
        fecha_devolucion_esperada = fecha_prestamo + timedelta(days=dias_prestamo)
        
        prestamo = Prestamo(
            id=prestamo_id,
            libro_isbn=isbn,
            usuario_id=usuario_id,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_esperada=fecha_devolucion_esperada
        )
        
        # Agregar a historial del usuario (Pila)
        usuario.historial_prestamos.apilar(prestamo)
        
        return True, f"Préstamo realizado exitosamente. ID: {prestamo_id}"
    
    def devolver_libro(self, usuario_id, isbn):
        """
        Process the return of a book.
        
        CRITICAL FLOW: Checks pending reservations using binary search.
        
        Args:
            usuario_id (str): User ID.
            isbn (str): Book ISBN.
        
        Returns:
            tuple: (bool, mensaje) indicating success and descriptive message.
        """
        # Verificar usuario
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Buscar préstamo activo
        prestamo = usuario.historial_prestamos.buscar_prestamo_activo_por_isbn(isbn)
        if not prestamo:
            return False, "No se encontró préstamo activo de este libro"
        
        # Marcar como devuelto
        prestamo.estado = "devuelto"
        prestamo.fecha_devolucion_real = datetime.now()
        
        # Buscar libro en inventario ordenado (BÚSQUEDA BINARIA - CRÍTICO)
        libro, indice = busqueda_binaria_por_isbn(
            self.inventario_ordenado.obtener_libros(),
            isbn
        )
        
        if indice == -1:
            return False, "Error: Libro no encontrado en inventario"
        
        # FLUJO CRÍTICO: Verificar reservas pendientes
        if isbn in self.colas_reservas:
            cola = self.colas_reservas[isbn]
            
            if not cola.esta_vacia():
                # Hay reservas pendientes: asignar al primero en la cola (FIFO)
                reserva = cola.desencolar()
                reserva.estado = "atendida"
                
                mensaje = (f"Libro devuelto y asignado automáticamente a "
                            f"usuario {reserva.usuario_id} (reserva {reserva.id})")
                
                # No incrementar stock disponible
                return True, mensaje
        
        # No hay reservas: incrementar stock disponible
        libro.cantidad_disponible += 1
        
        return True, "Libro devuelto exitosamente"
    
    # Gestión de Reservas

    def crear_reserva(self, usuario_id, isbn):
        """
        Creates a reservation for a book.
        
        Args:
            usuario_id (str): User ID.
            isbn (str): Book ISBN.
        
        Returns:
            tuple: (bool, mensaje) indicating success and descriptive message.
        """
        # Verificar usuario
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Verificar libro
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            return False, "Libro no encontrado"
        
        # Solo reservar si el libro está agotado 
        if libro.cantidad_disponible > 0:
            return False, f"No se puede reservar. El libro tiene {libro.cantidad_disponible} copia(s) disponible(s). Las reservas solo se permiten para libros agotados (stock = 0)"
        
        # Crear cola si no existe
        if isbn not in self.colas_reservas:
            self.colas_reservas[isbn] = ColaReservas(isbn)
        
        cola = self.colas_reservas[isbn]
        
        # Verificar si ya tiene reserva
        if cola.buscar_reserva_por_usuario(usuario_id):
            return False, "El usuario ya tiene una reserva para este libro"
        
        # Crear reserva
        reserva_id = f"R{self.contador_reservas:04d}"
        self.contador_reservas += 1
        
        reserva = Reserva(
            id=reserva_id,
            libro_isbn=isbn,
            usuario_id=usuario_id,
            fecha_reserva=datetime.now()
        )
        
        # Encolar (FIFO)
        cola.encolar(reserva)
        
        posicion = cola.obtener_posicion(usuario_id)
        return True, f"Reserva creada. Posición en cola: {posicion}"
    
    def cancelar_reserva(self, usuario_id, isbn):
        """
        Cancels a reservation for a user.
        
        Args:
            usuario_id (str): User ID.
            isbn (str): Book ISBN.
        
        Returns:
            tuple: (bool, mensaje)
        """
        if isbn not in self.colas_reservas:
            return False, "No hay reservas para este libro"
        
        cola = self.colas_reservas[isbn]
        reserva = cola.buscar_reserva_por_usuario(usuario_id)
        
        if not reserva:
            return False, "No se encontró reserva del usuario"
        
        reserva.estado = "cancelada"
        cola.eliminar_reserva(reserva.id)
        
        return True, "Reserva cancelada exitosamente"
    
    def obtener_reservas_libro(self, isbn):
        """Get the reservation queue for a book."""
        if isbn in self.colas_reservas:
            return self.colas_reservas[isbn].obtener_todas()
        return []
    
    # Gestión de Estantes

    def agregar_estante(self, estante):
        """
        Adds a shelf to the system.
        
        Args:
            estante (Estante): Shelf object.
        
        Returns:
            bool: True if added successfully.
        """
        if estante.id in self.estantes:
            return False
        self.estantes[estante.id] = estante
        return True
    
    def asignar_libro_a_estante(self, isbn, estante_id):
        """
        Assigns a book to a shelf.
        
        Args:
            isbn (str): Book ISBN.
            estante_id (str): Shelf ID.
        
        Returns:
            tuple: (bool, mensaje)
        """
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            return False, "Libro no encontrado"
        
        estante = self.estantes.get(estante_id)
        if not estante:
            return False, "Estante no encontrado"
        
        # Verificar peso
        if estante.peso_actual + libro.peso > estante.peso_maximo:
            return False, f"Excede el peso máximo del estante ({estante.peso_maximo} Kg)"
        
        # Verificar espacio
        if len(estante.libros_asignados) >= estante.cantidad:
            return False, "Estante lleno"
        
        # Asignar
        estante.libros_asignados.append(isbn)
        estante.peso_actual += libro.peso
        libro.estante_id = estante_id
        
        return True, "Libro asignado al estante exitosamente"
    
    def listar_estantes(self):
        """Gets the list of all shelves."""
        return list(self.estantes.values())
    
    # Funciones de utilidades

    def obtener_estadisticas(self):
        """
        Obtains general system statistics.
        
        Returns:
            dict: Dictionary with statistics.
        """
        total_libros = self.inventario_general.cantidad_libros()
        total_usuarios = len(self.usuarios)
        
        # Contar préstamos activos
        prestamos_activos = 0
        for usuario in self.usuarios.values():
            if usuario.historial_prestamos:
                prestamos_activos += len(usuario.historial_prestamos.obtener_activos())
        
        # Contar reservas
        total_reservas = sum(
            cola.tamanio() 
            for cola in self.colas_reservas.values()
        )
        
        return {
            'total_libros': total_libros,
            'total_usuarios': total_usuarios,
            'prestamos_activos': prestamos_activos,
            'total_reservas': total_reservas,
            'total_estantes': len(self.estantes)
        }