class ColaReservas:
    """
    Implementación de una Cola (FIFO - First In First Out).
    
    Esta clase gestiona la lista de espera de reservas para un libro
    específico que no tiene stock disponible. El primer usuario en
    reservar es el primero en ser atendido.
    
    Attributes:
        _items (list): Lista interna que almacena los elementos de la cola.
        _libro_isbn (str): ISBN del libro para el cual se gestionan las reservas.
    """
    
    def __init__(self, libro_isbn=None):
        """
        Initialize an empty queue.
        
        Args:
            libro_isbn (str, optional): ISBN of the book for this reservation queue.
        """
        self._items = []
        self._libro_isbn = libro_isbn
    
    def encolar(self, reserva):
        """
        Adds a reservation to the end of the queue.
        
        Args:
            reserva (Reserva): Reservation object to add.
        """
        self._items.append(reserva)
    
    def desencolar(self):
        """
        Removes and returns the first reservation in the queue.
        
        Returns:
            Reserva|None: The first reservation or None if the queue is empty.
        """
        if not self.esta_vacia():
            return self._items.pop(0)
        return None
    
    def ver_frente(self):
        """
        Returns the first reservation without removing it.
        
        Returns:
            Reserva|None: The first reservation or None if the queue is empty.
        """
        if not self.esta_vacia():
            return self._items[0]
        return None
    
    def esta_vacia(self):
        """
        Checks if the queue is empty.
        
        Returns:
            bool: True if the queue has no elements.
        """
        return len(self._items) == 0
    
    def tamanio(self):
        """
        Returns the number of reservations in the queue.
        
        Returns:
            int: NNumber of elements in the queue.
        """
        return len(self._items)
    
    def limpiar(self):
        """Removes all reservations from the queue."""
        self._items.clear()
    
    def obtener_todas(self):
        """
        Gets all reservations from the queue.
        
        Returns:
            list: List of all reservations (order: first to last).
        """
        return self._items.copy()
    
    def obtener_pendientes(self):
        """
        Gets only the pending reservations.
        
        Returns:
            list: List of reservations with status "pendiente".
        """
        return [r for r in self._items if r.estado == "pendiente"]
    
    def buscar_reserva_por_usuario(self, usuario_id):
        """
        Check if a user has a reservation in this queue.
        
        Args:
            usuario_id (str): ID of the user to search for.
        
        Returns:
            Reserva|None: The user's reservation or None if they don't have one.
        """
        for reserva in self._items:
            if reserva.usuario_id == usuario_id and reserva.estado == "pendiente":
                return reserva
        return None
    
    def eliminar_reserva(self, reserva_id):
        """
        Removes a specific reservation from the queue (cancelacion).
        
        Args:
            reserva_id (str): ID of the reservation to remove.
        
        Returns:
            bool: True if removed, False if not found.
        """
        for i, reserva in enumerate(self._items):
            if reserva.id == reserva_id:
                del self._items[i]
                return True
        return False
    
    def obtener_posicion(self, usuario_id):
        """
        Gets a user's position in the waiting queue.
        
        Args:
            usuario_id (str): ID of the user.
        
        Returns:
            int: Position in the queue (1 = first) or -1 if not found.
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