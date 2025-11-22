"""
Este paquete contiene implementaciones de algoritmos de búsqueda
adaptados para trabajar con objetos Libro:

- Búsqueda Lineal: Para inventario general

- Búsqueda Binaria: Para inventario ordenado 

Uso:
    from controllers.busqueda import (
        busqueda_lineal_por_titulo,
        busqueda_binaria_por_isbn
    )
    
    # Búsqueda lineal en inventario general
    resultados = busqueda_lineal_por_titulo(libros, "Quijote")
    
    # Búsqueda binaria en inventario ordenado 
    libro, indice = busqueda_binaria_por_isbn(inventario_ordenado, isbn)
"""

from .busqueda_lineal import (
    busqueda_lineal_por_isbn,
    busqueda_lineal_por_titulo,
    busqueda_lineal_por_autor,
    busqueda_lineal_por_criterio,
    busqueda_lineal_recursiva,
    busqueda_multiple,
    contar_comparaciones_lineal
)

from .busqueda_binaria import (
    busqueda_binaria_por_isbn,
    busqueda_binaria_recursiva,
    busqueda_binaria_por_criterio,
    encontrar_primera_ocurrencia,
    encontrar_ultima_ocurrencia,
    verificar_lista_ordenada,
    contar_comparaciones_binarias
)

__all__ = [
    # Búsqueda Lineal
    'busqueda_lineal_por_isbn',
    'busqueda_lineal_por_titulo',
    'busqueda_lineal_por_autor',
    'busqueda_lineal_por_criterio',
    'busqueda_lineal_recursiva',
    'busqueda_multiple',
    'contar_comparaciones_lineal',
    
    # Búsqueda Binaria
    'busqueda_binaria_por_isbn',
    'busqueda_binaria_recursiva',
    'busqueda_binaria_por_criterio',
    'encontrar_primera_ocurrencia',
    'encontrar_ultima_ocurrencia',
    'verificar_lista_ordenada',
    'contar_comparaciones_binarias'
]