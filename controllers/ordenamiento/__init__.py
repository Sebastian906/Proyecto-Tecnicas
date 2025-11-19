"""
Este paquete contiene implementaciones de algoritmos de ordenamiento
adaptados para trabajar con objetos Libro:

- Insertion Sort: Para mantener el inventario ordenado por ISBN
- Merge Sort: Para generar reportes globales ordenados por cualquier criterio

Uso:
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