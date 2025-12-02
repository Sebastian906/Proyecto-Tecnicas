class Libro:
    """
    Model corresponding to the books within the system

    Attributes:
        isbn (str): The unique ISBN identifier of the book.
        titulo (str): The title of the book.
        autor (str): The author of the book.
        peso (float): The weight of the book in kilograms (kg).
        valor (float): The monetary value of the book in Colombian pesos (COP).
        genero (str): The literary genre of the book.
        cantidad_disponible (int): The number of available copies in inventory.
        cantidad_total (int): The total number of copies in inventory.
        estante_id (int): The identifier of the shelf where the book is located.
    """

    def __init__(self, isbn, titulo, autor, peso, valor, genero, cantidad_disponible=1, cantidad_total=1, estante_id=None):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.peso = peso
        self.valor = valor
        self.genero = genero
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_total = cantidad_total
        self.estante_id = estante_id

    def esta_disponible(self):
        """
        Checks if the book is available for loan.
        
        Returns:
            bool: True if there is at least one copy available, False otherwise.
        """
        return self.cantidad_disponible > 0

    def __str__(self):
        return f"Libro: {self.titulo} (ISBN: {self.isbn})"
    
    def __repr__(self):
        return (f"Libro(isbn={self.isbn}, titulo={self.titulo}, autor={self.autor},)")