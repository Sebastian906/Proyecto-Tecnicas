class Prestamo:
    """
    Modelo correspondiente a los préstamos realizados por los usuarios

    Atributos:
        id (str): Identificador único del préstamo.
        usuario_id (str): Identificador del usuario que realizó el préstamo.
        libro_isbn (str): ISBN del libro prestado.
        fecha_prestamo (str): Fecha en que se realizó el préstamo.
        fecha_devolucion_esperada (str): Fecha en que se debe devolver el libro.
        fecha_devolucion_real (str): Fecha en que se devolvió el libro.
        estado (str): Estado del préstamo.
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