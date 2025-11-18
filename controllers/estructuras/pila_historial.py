class PilaHistorial:
    """
    Implementación de una Pila (LIFO - Last In First Out)

    Gestiona el historial de préstamos de un usuario,
    donde el prestamo más reciente es el primero en ser devuelto (tope de la pila).
    
    Atributos:
        _items (list): Lista que almacena los elementos de la pila.
        _usuario_id (str): Identificador del usuario asociado al historial.
    
    Ejemplo:
        >>> pila = PilaHistorial(usuario_id="U001")
        >>> pila.apilar("préstamo1")
        >>> pila.apilar("préstamo2")
        >>> último = pila.ver_tope() # prestamo más reciente (prestamo2)
    """

    def __init__(self, usuario_id=None):
        """
        Inicializa una pila vacía para el historial de préstamos de un usuario.
        
        Args:
            usuario_id (str, optional): Identificador del usuario. Por defecto es None.
        """
        self._items = []
        self._usuario_id = usuario_id

    def apilar(self, prestamo):
        """
        Agrega un préstamo al tope de la pila.

        Args:
            prestamo (Prestamo): El préstamo a agregar a la pila.
        """
        self._items.append(prestamo)

    def desapilar(self):
        """
        Remueve y retorna el préstamo del tope de la pila.

        Returns:
            Prestamo|None: El préstamo más reciente o None si la pila está vacía.
        """
        if not self.esta_vacia():
            return self._items.pop()
        return None
    
    def ver_tope(self):
        """
        Retorna el préstamo del tope sin removerlo.
        
        Returns:
            Prestamo|None: El préstamo más reciente o None si la pila está vacía.
        """
        if not self.esta_vacia():
            return self._items[-1]
        return None
    
    def esta_vacia(self):
        """
        Verifica si la pila está vacía.

        Returns:
            bool: True si la pila no tiene elementos.
        """
        return len(self._items) == 0
    
    def tamanio(self):
        """
        Retorna la cantidad de préstamos en la pila.

        Returns:
            int: Cantidad de elementos en la pila.
        """
        return len(self._items)
    
    def limpiar(self):
        """
        Limpia todos los préstamos de la pila.
        """
        self._items.clear()

    def obtener_todos(self):
        """
        Retorna una lista con todos los préstamos en la pila.

        Returns:
            list: Lista de todos los préstamos en la pila. (del más antiguo al más reciente)
        """
        return self._items.copy()
    
    def obtener_activos(self):
        """
        Obtiene solo los préstamos activos (no devueltos).
        
        Returns:
            list: Lista de préstamos con estado "prestado".
        """
        return [p for p in self._items if p.estado == "prestado"]
    
    def obtener_historico(self):
        """
        Obtiene los préstamos ya devueltos.
        
        Returns:
            list: Lista de préstamos con estado "devuelto".
        """
        return [p for p in self._items if p.estado == "devuelto"]
    
    def buscar_prestamo_activo_por_isbn(self, isbn):
        """
        Busca un préstamo activo de un libro específico.
        
        Args:
            isbn (str): ISBN del libro a buscar.
        
        Returns:
            Prestamo|None: El préstamo activo del libro o None.
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