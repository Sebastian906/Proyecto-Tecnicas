class InventarioGeneral:
    """
    Manage the overall inventory of books (in the order in which they were added) in the library.

    Attributes:
        libros (list): List containing the books in the inventory.
    """

    def __init__(self):
        """
        Initializes the general inventory with an empty list of books.
        """
        self.libros = []

    def agregar_libro(self, libro):
        """
        Adds a book to the general inventory.

        Args:
            libro (Libro): Book object to add to the inventory.

        Returns:
            bool: True if the book was added successfully. False if the ISBN already exists in the inventory.
        """
        # Verificar que el ISBN no exista en el inventario
        if self.buscar_por_isbn(libro.isbn):
            return False
        
        self.libros.append(libro)
        return True
    
    def agregar_libros(self, lista_libros):
        """
        Add multiple books to the overall inventory.

        Args:
            lista_libros (list): List of Book objects to add to the inventory.

        Returns:
            int: Number of books successfully added.
        """
        agregados = 0
        for libro in lista_libros:
            if self.agregar_libro(libro):
                agregados += 1
        return agregados
    
    def eliminar_libro(self, isbn):
        """
        Removes a book from the general inventory by its ISBN.

        Args:
            isbn (str): ISBN of the book to remove.

        Returns:
            bool: True if the book was removed, False if the book was not found.
        """
        for i, libro in enumerate(self.libros):
            if libro.isbn == isbn:
                del self.libros[i]
                return True
        return False
    
    def buscar_por_isbn(self, isbn):
        """
        Searches for a book in the inventory by its ISBN.

        Args:
            isbn (str): ISBN of the book to search for.

        Returns:
            Libro o None: The book is found, None is not found.
        """
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None
    
    def buscar_por_titulo(self, titulo):
        """
        Search for books in the inventory by their title.

        Args:
            titulo (str): Title of the book to search for.

        Returns:
            list: List of books that match the title.
        """
        titulo_lower = titulo.lower()
        resultados = []

        for libro in self.libros:
            if titulo_lower in libro.titulo.lower():
                resultados.append(libro)
        return resultados
    
    def buscar_por_autor(self, autor):
        """
        Search for books in the inventory by their author.

        Args:
            autor (str): Author of the book to search for.

        Returns:
            list: List of books that match the author.
        """
        autor_lower = autor.lower()
        resultados = []

        for libro in self.libros:
            if autor_lower in libro.autor.lower():
                resultados.append(libro)
        return resultados
    
    def obtener_libros(self):
        """
        Obtains the complete list of books in the inventory.

        Returns:
            list: Copy of all books in the inventory.
        """
        return self.libros.copy()
    
    def cantidad_libros(self):
        """
        Obtains the total number of books in the inventory.

        Returns:
            int: Total number of books in the inventory.
        """
        return len(self.libros)
    
    def esta_vacio(self):
        """
        Checks if the inventory is empty.

        Returns:
            bool: True if the inventory is empty, False otherwise.
        """
        return len(self.libros) == 0
    
    def limpiar_inventario(self):
        """
        Clears all books from the inventory.
        """
        self.libros.clear()

    def obtener_por_indice(self, indice):
        """
        Obtains a book by its index in the inventory list.

        Args:
            indice (int): Index of the book to obtain.

        Returns:
            Libro|None: The book if the index is valid, None if invalid.
        """
        if 0 <= indice < len(self.libros):
            return self.libros[indice]
        return None
    
    def __len__(self):
        """
        Returns the number of books in the inventory when using len().

        Returns:
            int: Total number of books in the inventory.
        """
        return len(self.libros)
    
    def __str__(self):
        return f"InventarioGeneral con {len(self.libros)} libros (orden de carga)."

    def __repr__(self):
        return f"InventarioGeneral(libros={len(self.libros)})"