class Reserva:
    """
    Modelo correspondiente a las reservas hechas por los usuarios

    Atributos:
        id (str): Identificador único de la reserva.
        usuario_id (str): Identificador del usuario que hizo la reserva.
        libro_isbn (str): ISBN del libro reservado.
        fecha_reserva (str): Fecha en que se hizo la reserva.
        estado (str): Estado de la reserva.
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