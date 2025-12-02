class Reserva:
    """
    Model corresponding to reservations made by users
    
    Attributes:
        id (str): Unique identifier of the reservation.
        usuario_id (str): Identifier of the user who made the reservation.
        libro_isbn (str): ISBN of the reserved book.
        fecha_reserva (str): Date when the reservation was made.
        estado (str): Status of the reservation.
    """

    def __init__(self, id: str, usuario_id: str, libro_isbn: str, fecha_reserva: str, estado="pendiente"):
        self.id = id
        self.usuario_id = usuario_id
        self.libro_isbn = libro_isbn
        self.fecha_reserva = fecha_reserva
        self.estado = estado

    def __str__(self):
        return (f"Reserva {self.id}: Libro {self.libro_isbn} → "f"Usuario {self.usuario_id} (Estado: {self.estado})")
    
    def __repr__(self):
        return (f"Reserva(id='{self.id}', libro='{self.libro_isbn}', "f"usuario='{self.usuario_id}', estado='{self.estado}'")