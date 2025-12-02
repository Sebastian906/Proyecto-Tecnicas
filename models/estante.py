class Estante:
    """
    Model corresponding to the shelves within the system

    Attributes:
        id (str): Shelf identifier.
        cantidad (int): Number of books the shelf can hold.
        peso_maximo (float): Maximum weight the shelf can support in kilograms (kg).
        peso_actual (float): Current weight of the shelf in kilograms (kg).
        libros_asignados (list): List of books assigned to the shelf.
    """

    PESO_MAXIMO = 8.0 # en kilogramos

    def __init__(self, id: str, cantidad: int, peso_maximo: float = None):
        self.id = id
        self.cantidad = cantidad
        self.peso_maximo = peso_maximo if peso_maximo is not None else Estante.PESO_MAXIMO
        self.peso_actual = 0.0
        self.libros_asignados = []

    def __str__(self):
        return (f"Estante {self.id}: {self.peso_actual:.1f}/{self.peso_maximo:.1f} kg "f"({len(self.libros_asignados)}/{self.cantidad} libros")
    
    def __repr__(self):
        return (f"Estante(id={self.id}, cantidad={self.cantidad}, "f"peso={self.peso_actual:.1f}/{self.peso_maximo:.1f})")