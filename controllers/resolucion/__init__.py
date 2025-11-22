"""
Este paquete contiene algoritmos para resolver problemas de estanterías:

- Fuerza Bruta: Encuentra TODAS las combinaciones peligrosas (> 8 Kg)

- Backtracking: Encuentra la combinación ÓPTIMA (maximizar valor ≤ 8 Kg)

Uso:
    from controllers.resolucion import (
        encontrar_combinaciones_peligrosas,
        optimizar_estanteria_backtracking
    )
    
    # Fuerza bruta: encontrar combinaciones peligrosas
    peligrosas = encontrar_combinaciones_peligrosas(libros)
    
    # Backtracking: encontrar estantería óptima
    mejor = optimizar_estanteria_backtracking(libros, peso_maximo=8.0)
"""

from .fuerza_bruta import (
    encontrar_combinaciones,
    demostrar_exploracion_fuerza_bruta
)

from .backtracking import (
    SolucionEstanteria,
    optimizar_estanteria,
    demostrar_backtracking
)

__all__ = [
    # Fuerza Bruta
    'encontrar_combinaciones',
    'demostrar_exploracion_fuerza_bruta',
    
    # Backtracking
    'SolucionEstanteria',
    'optimizar_estanteria',
    'demostrar_backtracking'
]