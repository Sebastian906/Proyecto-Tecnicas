"""

This package contains algorithms for solving shelving problems:

- Brute Force: Finds ALL dangerous combinations (> 8 Kg)

- Backtracking: Finds the OPTIMAL combination (maximize value ≤ 8 Kg)
Use:
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