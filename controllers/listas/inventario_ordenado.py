class InventarioOrdenado:
    """
    Gestiona el inventario ordenado de los libros en la biblioteca (De acuerdo al ISBN).

    Al agregarse un libro, se usa algoritmo de inserción para mantener el orden por ISBN.

    Atributos:
        libros (list): Lista que contiene los libros en el inventario ordenado por ISBN.
    """

    def __init__(self):
        """
        Inicia el inventario general con una lista vacía de libros.
        """
        self.libros = []

    def agregar_libro(self, libro):
        """
        Agrega un libro al inventario ordenado por ISBN.

        Se usa el ordenamiento por inserción para mantener la lista ordenada.

        Args:
            libro (Libro): Objeto Libro a agregar al inventario.

        Returns:
            bool: True si el libro fue agregado exitosamente. False si el ISBN ya existe en el inventario.
        """
        # Verificar que el ISBN no exista en el inventario
        if self.buscar_por_isbn(libro.isbn):
            return False
        
        # Agregar al final
        self.libros.append(libro)
        
        # Insertar el libro en la posición correcta para mantener el orden por ISBN
        i = len(self.libros) - 1
        while i > 0 and self.libros[i].isbn < self.libros[i-1].isbn:
            # Se intercambia con el elemento anterior
            self.libros[i], self.libros[i-1] = self.libros[i-1], self.libros[i]
            i -= 1
        return True
    
    def agregar_libros(self, lista_libros):
        """
        Agrega múltiples libros al inventario ordenado por ISBN.

        Args:
            lista_libros (list): Lista de objetos Libro a agregar al inventario.

        Returns:
            int: Número de libros agregados exitosamente.
        """
        agregados = 0
        for libro in lista_libros:
            if self.agregar_libro(libro):
                agregados += 1
        return agregados
    
    def eliminar_libro(self, isbn):
        """
        Elimina un libro del inventario ordenado por su ISBN.

        Args:
            isbn (str): ISBN del libro a eliminar.
        Returns:
            bool: True si se eliminó, False si no se encontró el libro.
        """
        # Se usa búsqueda binaria para encontrar el libro
        indice = self.buscar_indice_binario(isbn)
        if indice != -1:
            del self.libros[indice]
            return True
        return False
    
    def buscar_por_isbn(self, isbn):
        """
        Busca un libro en el inventario por su ISBN usando búsqueda binaria.

        Args:
            isbn (str): ISBN del libro a buscar.

        Returns:
            Libro|None: Objeto Libro si se encuentra, None si no se encuentra.
        """
        indice = self.buscar_indice_binario(isbn)
        if indice != -1:
            return self.libros[indice]
        return None
    
    def buscar_indice_binario(self, isbn):
        """
        Busca el índice de un libro en la lista usando búsqueda binaria.

        Args:
            isbn (str): ISBN del libro a buscar.

        Returns:
            int: Índice del libro si se encuentra, -1 si no se encuentra.
        """
        izquierda = 0
        derecha = len(self.libros) - 1
        
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            isbn_medio = self.libros[medio].isbn
            if isbn_medio == isbn:
                return medio
            elif isbn_medio < isbn:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return -1 # No encontrado
    
    def obtener_libros(self):
        """
        Obtiene la lista completa de libros en el inventario ordenado.

        Returns:
            list: Lista de objetos Libro en el inventario.
        """
        return self.libros

    def cantidad_libros(self):
        """
        Obtiene la cantidad total de libros en el inventario ordenado.

        Returns:
            int: Cantidad de libros en el inventario.
        """
        return len(self.libros)
    
    def estar_vacio(self):
        """
        Verifica si el inventario ordenado está vacío.

        Returns:
            bool: True si el inventario está vacío, False en caso contrario.
        """
        return len(self.libros) == 0
    
    def limpiar_inventario(self):
        """
        Limpia todos los libros del inventario ordenado.
        """
        self.libros.clear()

    def verificar_orden(self):
        """
        Verifica si la lista de libros está ordenada por ISBN.

        Returns:
            bool: True si la lista está ordenada, False en caso contrario.
        """
        for i in range(1, len(self.libros)):
            if self.libros[i].isbn < self.libros[i-1].isbn:
                return False
        return True
    
    def obtener_por_indice(self, indice):
        """
        Obtiene un libro por su índice en la lista ordenada.

        Args:
            indice (int): Índice del libro a obtener.

        Returns:
            Libro|None: Objeto Libro si el índice es válido, None en caso contrario.
        """
        if 0 <= indice < len(self.libros):
            return self.libros[indice]
        return None
    
    def __len__(self):
        return len(self.libros)

    def __str__(self):
        return f"InventarioOrdenado con {len(self.libros)} libros ordenados por ISBN."
    
    def __repr__(self):
        return f"InventarioOrdenado({self.libros})"