class InventarioGeneral:
    """
    Gestiona el inventario general de los libros (en orden del que fueron agregados) en la biblioteca.

    Atributos:
        libros (list): Lista que contiene los libros en el inventario.
    """

    def __init__(self):
        """
        Inicia el inventario general con una lista vacía de libros.
        """
        self.libros = []

    def agregar_libro(self, libro):
        """
        Agrega un libro al inventario general.

        Args:
            libro (Libro): Objeto Libro a agregar al inventario.

        Returns:
            bool: True si el libro fue agregado exitosamente. False si el ISBN ya existe en el inventario.
        """
        # Verificar que el ISBN no exista en el inventario
        if self.buscar_por_isbn(libro.isbn):
            return False
        
        self.libros.append(libro)
        return True
    
    def agregar_libros(self, lista_libros):
        """
        Agrega múltiples libros al inventario general.

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
        Elimina un libro del inventario general por su ISBN.

        Args:
            isbn (str): ISBN del libro a eliminar.

        Returns:
            bool: True si se eliminó, False si no se encontró el libro.
        """
        for i, libro in enumerate(self.libros):
            if libro.isbn == isbn:
                del self.libros[i]
                return True
        return False
    
    def buscar_por_isbn(self, isbn):
        """
        Busca un libro en el inventario por su ISBN.

        Args:
            isbn (str): ISBN del libro a buscar.

        Returns:
            Libro o None: El libro si se encuentra, None si no se encuentra.
        """
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None
    
    def buscar_por_titulo(self, titulo):
        """
        Busca libros en el inventario por su título.

        Args:
            titulo (str): Título del libro a buscar.

        Returns:
            list: Lista de libros que coinciden con el título.
        """
        titulo_lower = titulo.lower()
        resultados = []

        for libro in self.libros:
            if titulo_lower in libro.titulo.lower():
                resultados.append(libro)
        return resultados
    
    def buscar_por_autor(self, autor):
        """
        Busca libros en el inventario por su autor.

        Args:
            autor (str): Autor del libro a buscar.

        Returns:
            list: Lista de libros que coinciden con el autor.
        """
        autor_lower = autor.lower()
        resultados = []

        for libro in self.libros:
            if autor_lower in libro.autor.lower():
                resultados.append(libro)
        return resultados
    
    def obtener_libros(self):
        """
        Obtiene la lista completa de libros en el inventario.

        Returns:
            list: Copia de todos los libros en el inventario.
        """
        return self.libros.copy()
    
    def cantidad_libros(self):
        """
        Obtiene la cantidad total de libros en el inventario.

        Returns:
            int: Número total de libros en el inventario.
        """
        return len(self.libros)
    
    def esta_vacio(self):
        """
        Verifica si el inventario está vacío.

        Returns:
            bool: True si el inventario está vacío, False en caso contrario.
        """
        return len(self.libros) == 0
    
    def limpiar_inventario(self):
        """
        Limpia todos los libros del inventario.
        """
        self.libros.clear()

    def obtener_por_indice(self, indice):
        """
        Obtiene un libro por su índice en la lista del inventario.

        Args:
            indice (int): Índice del libro a obtener.

        Returns:
            Libro|None: El libro si el índice es válido, None si es inválido.
        """
        if 0 <= indice < len(self.libros):
            return self.libros[indice]
        return None
    
    def __len__(self):
        """
        Devuelve la cantidad de libros en el inventario al usar len().

        Returns:
            int: Número total de libros en el inventario.
        """
        return len(self.libros)
    
    def __str__(self):
        return f"InventarioGeneral con {len(self.libros)} libros (orden de carga)."

    def __repr__(self):
        return f"InventarioGeneral(libros={len(self.libros)})"