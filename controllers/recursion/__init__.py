"""
This package contains implementations of recursive algorithms
for calculations on collections of books by author:

- Stack Recursion: Calculates the total value of books
  * Work on RETURN from recursive calls
  * Accumulates in the system call stack
  * Classic example of non-optimizable recursion

- Tail Recursion: Calculates the average weight of books
  * Work BEFORE recursive calls
  * Uses explicit accumulators
  * Optimizable (Tail Call Optimization)

Use:
    from controllers.recursion import (
        calcular_valor_total_recursivo,
        calcular_peso_promedio_recursivo
    )
    
    # Recursión de pila (valor total)
    valor = calcular_valor_total_recursivo(libros, "García Márquez")
    
    # Recursión de cola (peso promedio)
    peso = calcular_peso_promedio_recursivo(libros, "García Márquez")
"""

from .valor_total import (
    calcular_valor_total,
    contar_libros_autor,
    obtener_libros_autor,
    analizar_valor_por_autor,
    demostrar_recursion_pila
)

from .peso_promedio import (
    calcular_peso_promedio,
    calcular_estadisticas_peso,
    demostrar_recursion_cola,
)

__all__ = [
    # Recursión de Pila (Valor Total)
    'calcular_valor_total',
    'contar_libros_autor',
    'obtener_libros_autor',
    'analizar_valor_por_autor',
    'demostrar_recursion_pila',
    
    # Recursión de Cola (Peso Promedio)
    'calcular_peso_promedio',
    'calcular_estadisticas_peso',
    'demostrar_recursion_cola',
]