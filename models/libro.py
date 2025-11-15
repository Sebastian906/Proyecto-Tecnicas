class Libro:
    """
    Modelo correspondiente a los libros dentro del sistema

    Atributos:
        isbn (str): El ISBN único identificador del libro.
        titulo (str): El título del libro.
        autor (str): El autor del libro.
        peso (float): El peso del libro en kilogramos (kg).
        valor (float): El valor monetario del libro en pesos Colombianos (COP).
        genero (str): El género literario del libro.
        cantidad_disponible (int): La cantidad de libros disponibles en inventario.
        cantidad_total (int): La cantidad total de libros en inventario.
        estante_id (int): El identificador del estante donde se encuentra el libro.
    """

    def __init__(self, isbn: str, titulo: str, autor: str, peso: float, valor: float,
                genero: str, cantidad_disponible: int, cantidad_total: int, estante_id: int):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.peso = peso
        self.valor = valor
        self.genero = genero
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_total = cantidad_total
        self.estante_id = estante_id

    def __str__(self):
        return f"Libro: {self.titulo} (ISBN: {self.isbn})"
    
    def __repr__(self):
        return (f"Libro(isbn={self.isbn}, titulo={self.titulo}, autor={self.autor},)")