"""
Este módulo actúa como fachada (Facade Pattern) que coordina todos
los subsistemas del Sistema de Gestión de Bibliotecas.

Responsabilidades:
- Gestionar inventarios (general y ordenado)
- Coordinar préstamos y devoluciones
- Gestionar reservas y colas de espera
- Administrar usuarios
- Coordinar estanterías
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
    Clase principal que coordina todo el sistema de gestión de bibliotecas.
    
    Implementa el patrón Facade para simplificar el acceso a los subsistemas.
    
    Attributes:
        inventario_general (InventarioGeneral): Lista desordenada de libros.
        inventario_ordenado (InventarioOrdenado): Lista ordenada por ISBN.
        usuarios (dict): Diccionario de usuarios por ID.
        colas_reservas (dict): Colas de reservas por ISBN.
        estantes (dict): Diccionario de estantes por ID.
        contador_prestamos (int): Contador para generar IDs de préstamos.
        contador_reservas (int): Contador para generar IDs de reservas.
    """
    def __init__(self):
        """Inicializa el gestor de biblioteca."""
        # Inventarios
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
        Agrega un libro a ambos inventarios.
        
        Args:
            libro (Libro): Objeto Libro a agregar.
        
        Returns:
            bool: True si se agregó exitosamente.
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
        Busca un libro por ISBN en el inventario ordenado (búsqueda binaria).
        
        Args:
            isbn (str): ISBN del libro.
        
        Returns:
            Libro|None: Libro encontrado o None.
        """
        libro, _ = busqueda_binaria_por_isbn(
            self.inventario_ordenado.obtener_libros(), 
            isbn
        )
        return libro
    
    def buscar_libros_por_titulo(self, titulo):
        """
        Busca libros por título (búsqueda lineal).
        
        Args:
            titulo (str): Título o parte del título.
        
        Returns:
            list: Lista de libros encontrados.
        """
        return self.inventario_general.buscar_por_titulo(titulo)
    
    def buscar_libros_por_autor(self, autor):
        """
        Busca libros por autor (búsqueda lineal).
        
        Args:
            autor (str): Autor o parte del nombre.
        
        Returns:
            list: Lista de libros encontrados.
        """
        return self.inventario_general.buscar_por_autor(autor)
    
    def eliminar_libro(self, isbn):
        """
        Elimina un libro de ambos inventarios.
        
        Args:
            isbn (str): ISBN del libro a eliminar.
        
        Returns:
            bool: True si se eliminó exitosamente.
        """
        result1 = self.inventario_general.eliminar_libro(isbn)
        result2 = self.inventario_ordenado.eliminar_libro(isbn)
        return result1 and result2
    
    def obtener_todos_los_libros(self):
        """Obtiene todos los libros del inventario."""
        return self.inventario_general.obtener_libros()
    
    # Gestión de Usuarios

    def agregar_usuario(self, usuario):
        """
        Agrega un usuario al sistema.
        
        Args:
            usuario (Usuario): Objeto Usuario a agregar.
        
        Returns:
            bool: True si se agregó exitosamente.
        """
        if usuario.id in self.usuarios:
            return False
        
        # Inicializar historial de préstamos
        usuario.historial_prestamos = PilaHistorial(usuario.id)
        self.usuarios[usuario.id] = usuario
        return True
    
    def buscar_usuario(self, usuario_id):
        """
        Busca un usuario por ID.
        
        Args:
            usuario_id (str): ID del usuario.
        
        Returns:
            Usuario|None: Usuario encontrado o None.
        """
        return self.usuarios.get(usuario_id)
    
    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario del sistema.
        
        Args:
            usuario_id (str): ID del usuario a eliminar.
        
        Returns:
            bool: True si se eliminó exitosamente.
        """
        if usuario_id in self.usuarios:
            del self.usuarios[usuario_id]
            return True
        return False
    
    def listar_usuarios(self):
        """Obtiene la lista de todos los usuarios."""
        return list(self.usuarios.values())
    
    # Gestión de Préstamos

    def realizar_prestamo(self, usuario_id, isbn, dias_prestamo=15):
        """
        Realiza un préstamo de libro a un usuario.
        
        Args:
            usuario_id (str): ID del usuario.
            isbn (str): ISBN del libro.
            dias_prestamo (int, optional): Días de duración. Default: 15.
        
        Returns:
            tuple: (bool, mensaje) indicando éxito y mensaje descriptivo.
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
        Procesa la devolución de un libro.
        
        FLUJO CRÍTICO: Verifica reservas pendientes usando búsqueda binaria.
        
        Args:
            usuario_id (str): ID del usuario.
            isbn (str): ISBN del libro.
        
        Returns:
            tuple: (bool, mensaje) indicando éxito y mensaje descriptivo.
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
        Crea una reserva para un libro.
        
        Args:
            usuario_id (str): ID del usuario.
            isbn (str): ISBN del libro.
        
        Returns:
            tuple: (bool, mensaje) indicando éxito y mensaje descriptivo.
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
        Cancela una reserva de un usuario.
        
        Args:
            usuario_id (str): ID del usuario.
            isbn (str): ISBN del libro.
        
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
        """Obtiene la cola de reservas de un libro."""
        if isbn in self.colas_reservas:
            return self.colas_reservas[isbn].obtener_todas()
        return []
    
    # Gestión de Estantes

    def agregar_estante(self, estante):
        """
        Agrega un estante al sistema.
        
        Args:
            estante (Estante): Objeto Estante.
        
        Returns:
            bool: True si se agregó exitosamente.
        """
        if estante.id in self.estantes:
            return False
        self.estantes[estante.id] = estante
        return True
    
    def asignar_libro_a_estante(self, isbn, estante_id):
        """
        Asigna un libro a un estante.
        
        Args:
            isbn (str): ISBN del libro.
            estante_id (str): ID del estante.
        
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
        """Obtiene la lista de todos los estantes."""
        return list(self.estantes.values())
    
    # Funciones de utilidades

    def obtener_estadisticas(self):
        """
        Obtiene estadísticas generales del sistema.
        
        Returns:
            dict: Diccionario con estadísticas.
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