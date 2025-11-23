class Estante:
    """
    Modelo correspondiente a los estantes dentro del sistema

    Atributos:
        id (str): Identificador del estante.
        cantidad (int): Cantidad de libros que puede contener el estante.
        peso_maximo (float): Peso máximo que puede soportar el estante en kilogramos (kg).
        peso_actual (float): Peso actual del estante en kilogramos (kg).
        libros_asignados (list): Lista de libros asignados al estante.
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