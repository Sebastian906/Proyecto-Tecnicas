class ColaReservas:
    """
    Implementación de una Cola (FIFO - First In First Out).
    
    Esta clase gestiona la lista de espera de reservas para un libro
    específico que no tiene stock disponible. El primer usuario en
    reservar es el primero en ser atendido.
    
    Attributes:
        _items (list): Lista interna que almacena los elementos de la cola.
        _libro_isbn (str): ISBN del libro para el cual se gestionan las reservas.
    
    Example:
        >>> cola = ColaReservas("978-123-456-789-0")
        >>> cola.encolar(reserva1)
        >>> cola.encolar(reserva2)
        >>> primera = cola.ver_frente()  # reserva1 (primera en la cola)
        >>> atendida = cola.desencolar()  # Remueve reserva1
    """
    
    def __init__(self, libro_isbn=None):
        """
        Inicializa una cola vacía.
        
        Args:
            libro_isbn (str, optional): ISBN del libro para esta cola de reservas.
        """
        self._items = []
        self._libro_isbn = libro_isbn
    
    def encolar(self, reserva):
        """
        Agrega una reserva al final de la cola.
        
        Args:
            reserva (Reserva): Objeto Reserva a agregar.
        """
        self._items.append(reserva)
    
    def desencolar(self):
        """
        Remueve y retorna la primera reserva de la cola.
        
        Returns:
            Reserva|None: La primera reserva o None si la cola está vacía.
        """
        if not self.esta_vacia():
            return self._items.pop(0)
        return None
    
    def ver_frente(self):
        """
        Retorna la primera reserva sin removerla.
        
        Returns:
            Reserva|None: La primera reserva o None si la cola está vacía.
        """
        if not self.esta_vacia():
            return self._items[0]
        return None
    
    def esta_vacia(self):
        """
        Verifica si la cola está vacía.
        
        Returns:
            bool: True si la cola no tiene elementos.
        """
        return len(self._items) == 0
    
    def tamanio(self):
        """
        Retorna la cantidad de reservas en la cola.
        
        Returns:
            int: Número de elementos en la cola.
        """
        return len(self._items)
    
    def limpiar(self):
        """Elimina todas las reservas de la cola."""
        self._items.clear()
    
    def obtener_todas(self):
        """
        Obtiene todas las reservas de la cola.
        
        Returns:
            list: Lista de todas las reservas (orden: primera a última).
        """
        return self._items.copy()
    
    def obtener_pendientes(self):
        """
        Obtiene solo las reservas pendientes.
        
        Returns:
            list: Lista de reservas con estado "pendiente".
        """
        return [r for r in self._items if r.estado == "pendiente"]
    
    def buscar_reserva_por_usuario(self, usuario_id):
        """
        Busca si un usuario tiene una reserva en esta cola.
        
        Args:
            usuario_id (str): ID del usuario a buscar.
        
        Returns:
            Reserva|None: La reserva del usuario o None si no la tiene.
        """
        for reserva in self._items:
            if reserva.usuario_id == usuario_id and reserva.estado == "pendiente":
                return reserva
        return None
    
    def eliminar_reserva(self, reserva_id):
        """
        Elimina una reserva específica de la cola (cancelación).
        
        Args:
            reserva_id (str): ID de la reserva a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        for i, reserva in enumerate(self._items):
            if reserva.id == reserva_id:
                del self._items[i]
                return True
        return False
    
    def obtener_posicion(self, usuario_id):
        """
        Obtiene la posición de un usuario en la cola de espera.
        
        Args:
            usuario_id (str): ID del usuario.
        
        Returns:
            int: Posición en la cola (1 = primero) o -1 si no está.
        """
        for i, reserva in enumerate(self._items):
            if reserva.usuario_id == usuario_id and reserva.estado == "pendiente":
                return i + 1  # Posición basada en 1
        return -1
    
    def __len__(self):
        return len(self._items)
    
    def __str__(self):
        return f"ColaReservas({self._libro_isbn}): {len(self._items)} reservas"
    
    def __repr__(self):
        return f"ColaReservas(libro_isbn='{self._libro_isbn}', items={len(self._items)})"