"""
This package contains the implementations of specialized data
structures for the Library Management System.:

- PilaHistorial: LIFO structure for user loan history
- ColaReservas: FIFO structure for waitlist of out-of-stock books

Use:
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