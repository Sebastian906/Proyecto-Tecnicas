class Prestamo:
    """
    Model corresponding to loans made by users

    Attributes:
        id (str): Unique identifier of the loan.
        usuario_id (str): Identifier of the user who made the loan.
        libro_isbn (str): ISBN of the loaned book.
        fecha_prestamo (str): Date when the loan was made.
        fecha_devolucion_esperada (str): Date when the book should be returned.
        fecha_devolucion_real (str): Date when the book was actually returned.
        estado (str): Status of the loan.
    """

    def __init__(self, id: str, usuario_id: str, libro_isbn: str, fecha_prestamo: str, fecha_devolucion_esperada: str,
                fecha_devolucion_real=None, estado="prestado"):
        self.id = id
        self.usuario_id = usuario_id
        self.libro_isbn = libro_isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado

    def __str__(self):
        return (f"Préstamo {self.id}: Libro {self.libro_isbn} → "f"Usuario {self.usuario_id} (Estado: {self.estado})")
    
    def __repr__(self):
        return (f"Prestamo(id='{self.id}', libro='{self.libro_isbn}', "f"usuario='{self.usuario_id}', estado='{self.estado}'")