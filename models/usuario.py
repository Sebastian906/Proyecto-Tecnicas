class Usuario:
    """
    Model corresponding to system users

    Attributes:
        id (str): User identifier.
        nombre (str): User's first name.
        apellidos(str): User's last name.
        direccion (str): Address where the user lives.
        historial_prestamos (stack): List of loans made by the user.
    """

    def __init__(self, id: str, nombre: str, apellidos: str, direccion: str):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.direccion = direccion
        self.historial_prestamos = None # Se asigna la pila de forma externa

    def __str__(self):
        return f"Usuario: {self.nombre} {self.apellidos} (ID: {self.id})"
    
    def __repr__(self):
        return (f"Usuario(id={self.id}, nombre={self.nombre}, apellidos={self.apellidos},)")