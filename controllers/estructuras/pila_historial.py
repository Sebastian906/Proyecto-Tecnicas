class PilaHistorial:
    """
    Implementation of a Stack (LIFO - Last In First Out)

    Manages a user's loan history,
    where the most recent loan is the first to be returned (top of the stack).
    
    Attributes:
        _items (list): List that stores the elements of the stack.
        _usuario_id (str): Identifier of the user associated with the history.
    """

    def __init__(self, usuario_id=None):
        """
        Initializes an empty stack for a user's loan history.
        
        Args:
            usuario_id (str, optional): Identifier of the user. Default is None.
        """
        self._items = []
        self._usuario_id = usuario_id

    def apilar(self, prestamo):
        """
        Adds a loan to the top of the stack.

        Args:
            prestamo (Prestamo): The loan to add to the stack.
        """
        self._items.append(prestamo)

    def desapilar(self):
        """
        Removes and returns the loan at the top of the stack.

        Returns:
            Prestamo|None: The most recent loan or None if the stack is empty.
        """
        if not self.esta_vacia():
            return self._items.pop()
        return None
    
    def ver_tope(self):
        """
        Returns the loan at the top without removing it.
        
        Returns:
            Prestamo|None: The most recent loan or None if the stack is empty.
        """
        if not self.esta_vacia():
            return self._items[-1]
        return None
    
    def esta_vacia(self):
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack has no elements.
        """
        return len(self._items) == 0
    
    def tamanio(self):
        """
        Returns the number of loans in the stack.

        Returns:
            int: Number of elements in the stack.
        """
        return len(self._items)
    
    def limpiar(self):
        """
        Clears all loans from the stack.
        """
        self._items.clear()

    def obtener_todos(self):
        """
        Returns a list with all loans in the stack.

        Returns:
            list: List of all loans in the stack. (from oldest to most recent)
        """
        return self._items.copy()
    
    def obtener_activos(self):
        """
        Returns only the active loans (not returned).
        
        Returns:
            list: List of loans with status "prestado".
        """
        return [p for p in self._items if p.estado == "prestado"]
    
    def obtener_historico(self):
        """
        Returns the loans that have been returned.
        
        Returns:
            list: List of loans with status "devuelto".
        """
        return [p for p in self._items if p.estado == "devuelto"]
    
    def buscar_prestamo_activo_por_isbn(self, isbn):
        """
        Search for an active loan of a specific book.
        
        Args:
            isbn (str): ISBN of the book to search for.
        
        Returns:
            Prestamo|None: The active loan of the book or None.
        """
        for prestamo in reversed(self._items):  # Buscar desde el más reciente
            if prestamo.libro_isbn == isbn and prestamo.estado == "prestado":
                return prestamo
        return None
    
    def __len__(self):
        return len(self._items)
    
    def __str__(self):
        return f"PilaHistorial({self._usuario_id}): {len(self._items)} préstamos"
    
    def __repr__(self):
        return f"PilaHistorial(usuario_id='{self._usuario_id}', items={len(self._items)})"