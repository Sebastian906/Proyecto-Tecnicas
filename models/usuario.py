class Usuario:
    """
    Modelo correspondiente a los usuarios del sistema

    Atributos:
        id (str): Identificador del usuario.
        nombre (str): Nombre del usuario.
        apellidos(str): Apellidos del usuario.
        direccion (str): Dirección donde vive el usuario.
        historial_prestamos (pila): Lista de préstamos realizados por el usuario.
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