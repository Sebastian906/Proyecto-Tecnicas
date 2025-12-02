class InventarioOrdenado:
    """
    Manage the organized inventory of books in the library (According to ISBN).

    When a book is added, an insertion algorithm is used to maintain order by ISBN.

    Attributes:
        libros (list): List containing the books in the inventory ordered by ISBN.
    """

    def __init__(self):
        """
        Initializes the general inventory with an empty list of books.
        """
        self.libros = []

    def agregar_libro(self, libro):
        """
        Adds a book to the inventory ordered by ISBN.

        An insertion sort algorithm is used to maintain the list ordered.

        Args:
            libro (Libro): Book object to add to the inventory.

        Returns:
            bool: True if the book was added successfully. False if the ISBN already exists in the inventory.
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
        Adds multiple books to the inventory ordered by ISBN.

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
        Removes a book from the inventory ordered by its ISBN.

        Args:
            isbn (str): ISBN of the book to remove.
        Returns:
            bool: True if the book was removed, False if the book was not found.
        """
        # Se usa búsqueda binaria para encontrar el libro
        indice = self.buscar_indice_binario(isbn)
        if indice != -1:
            del self.libros[indice]
            return True
        return False
    
    def buscar_por_isbn(self, isbn):
        """
        Searches for a book in the inventory by its ISBN using binary search.

        Args:
            isbn (str): ISBN of the book to search for.

        Returns:
            Libro|None: Book object if found, None if not found.
        """
        indice = self.buscar_indice_binario(isbn)
        if indice != -1:
            return self.libros[indice]
        return None
    
    def buscar_indice_binario(self, isbn):
        """
        Searches for the index of a book in the list using binary search.

        Args:
            isbn (str): ISBN of the book to search for.

        Returns:
            int: Index of the book if found, -1 if not found.
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
        Obtains the complete list of books in the ordered inventory.

        Returns:
            list: List of Book objects in the inventory.
        """
        return self.libros

    def cantidad_libros(self):
        """
        Obtains the total number of books in the ordered inventory.

        Returns:
            int: Number of books in the inventory.
        """
        return len(self.libros)
    
    def estar_vacio(self):
        """
        Checks if the ordered inventory is empty.

        Returns:
            bool: True if the inventory is empty, False otherwise.
        """
        return len(self.libros) == 0
    
    def limpiar_inventario(self):
        """
        Clears all books from the ordered inventory.
        """
        self.libros.clear()

    def verificar_orden(self):
        """
        Checks if the list of books is ordered by ISBN.

        Returns:
            bool: True if the list is ordered, False otherwise.
        """
        for i in range(1, len(self.libros)):
            if self.libros[i].isbn < self.libros[i-1].isbn:
                return False
        return True
    
    def obtener_por_indice(self, indice):
        """
        Obtains a book by its index in the ordered list.

        Args:
            indice (int): Index of the book to obtain.

        Returns:
            Libro|None: Book object if the index is valid, None otherwise.
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