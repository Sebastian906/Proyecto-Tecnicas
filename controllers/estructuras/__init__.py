"""
Este paquete contiene las implementaciones de estructuras de datos
especializadas para el Sistema de Gestión de Bibliotecas:

- PilaHistorial: Estructura LIFO para historial de préstamos por usuario
- ColaReservas: Estructura FIFO para lista de espera de libros agotados

Uso:
    from controllers.estructuras import PilaHistorial, ColaReservas
    
    pila = PilaHistorial("U001")
    cola = ColaReservas("978-123-456-789-0")
"""

from .pila_historial import PilaHistorial
from .cola_reservas import ColaReservas

__all__ = [
    'PilaHistorial',
    'ColaReservas'
]