"""
This package contains implementations of sorting algorithms
adapted to work with Book objects:

- Insertion Sort: To maintain the inventory ordered by ISBN
- Merge Sort: To generate global reports ordered by any criteria
Use:
    from controllers.ordenamiento import ordenar_por_insercion, merge_sort
    
    # Insertion Sort
    ordenar_por_insercion(libros, criterio='isbn')
    
    # Merge Sort
    libros_ordenados = merge_sort(libros, criterio='valor', orden='desc')
"""

from .insercion import (
    ordenamiento_insercion,
    insertar_libro_ordenado,
    verificar_orden,
    contar_comparaciones_insercion
)

from .merge_sort import (
    merge_sort,
    generar_reporte_global
)

__all__ = [
    'ordenamiento_insercion',
    'insertar_libro_ordenado',
    'verificar_orden',
    'contar_comparaciones_insercion',
    'merge_sort',
    'generar_reporte_global'
]