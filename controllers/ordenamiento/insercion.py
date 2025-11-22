"""
Este algoritmo se utiliza para mantener el Inventario Ordenado cada vez
que se agrega un nuevo libro al sistema, asegurando que la lista siempre 
esté ordenada por ISBN de forma ascendente para permitir búsqueda binaria.

Complejidad Temporal:
    - Mejor caso: O(n) -> la lista ya está ordenada
    - Caso promedio: O(n²)
    - Peor caso: O(n²)

Complejidad Espacial: O(1) - ordenamiento in-place
"""

def ordenamiento_insercion(lista_libros, criterio='isbn', orden='asc'):
    """
    Ordena una lista de libros utilizando el algoritmo de ordenamiento por inserción.

    Este algoritmo compara cada elemento con los anteriores y lo inserta
    en la posición correcta. Es eficiente para listas pequeñas o casi ordenadas.
    
    Args:
        lista_libros (list): Lista de objetos Libro a ordenar.
        criterio (str, optional): Atributo por el cual ordenar. 
            Opciones: 'isbn', 'titulo', 'autor', 'peso', 'valor'.
            Default: 'isbn'.
        orden (str, optional): 'asc' para ascendente, 'desc' para descendente.
            Default: 'asc'.
    
    Returns:
        list: La misma lista ordenada (modificada in-place).
    """
    n = len(lista_libros)

    # Iterar sobre el segundo elemento
    for i in range(1, n):
        libro_actual = lista_libros[i]
        valor_actual = obtener_valor_criterio(libro_actual, criterio)
        # Posición donde se va a insertar el libro actual
        j = i - 1
        # Mover elementos mayores una posición adelante
        while j >= 0:
            valor_comparacion = obtener_valor_criterio(lista_libros[j], criterio)
            # Determinar si se debe mover según el orden
            if orden == 'asc':
                debe_mover = valor_comparacion > valor_actual
            else: # desc
                debe_mover = valor_comparacion < valor_actual
            if debe_mover:
                lista_libros[j + 1] = lista_libros[j]
                j -= 1
            else:
                break

        # Insertar el libro actual en su posición correcta
        lista_libros[j + 1] = libro_actual
    return lista_libros

def insertar_libro_ordenado(lista_ordenada, libro_nuevo, criterio='isbn'):
    """
    Inserta un nuevo libro en una lista ya ordenada manteniendo el orden.
    
    Esta es una optimización del Insertion Sort para agregar un solo elemento
    a una lista que ya está ordenada. Usado en el Inventario Ordenado.
    
    Args:
        lista_ordenada (list): Lista de libros ya ordenada.
        libro_nuevo (Libro): Libro a insertar.
        criterio (str, optional): Atributo por el cual está ordenada la lista.
            Default: 'isbn'.
    
    Returns:
        int: Índice donde se insertó el libro.
    """
    valor_nuevo = obtener_valor_criterio(libro_nuevo, criterio)
    # Agregar al final
    lista_ordenada.append(libro_nuevo)
    # Encontrar la posición correcta y mover hacia atrás
    i = len(lista_ordenada) - 1
    while i > 0 and obtener_valor_criterio(lista_ordenada[i - 1], criterio) > valor_nuevo:
        # Intercambiar con el elemento anterior
        lista_ordenada[i], lista_ordenada[i - 1] = lista_ordenada[i - 1], lista_ordenada[i] 
        i -= 1
    return i

def obtener_valor_criterio(libro, criterio):
    """
    Obtiene el valor del atributo especificado de un libro.
    
    Args:
        libro (Libro): Objeto Libro.
        criterio (str): Nombre del atributo.
    
    Returns:
        any: Valor del atributo (str, float, int).
    
    Raises:
        AttributeError: Si el criterio no existe en el objeto Libro.
    """
    if not hasattr(libro, criterio):
        raise AttributeError(f"El libro no tiene el atributo '{criterio}'")
    return getattr(libro, criterio)

def verificar_orden(lista_libros, criterio='isbn', orden='asc'):
    """
    Verifica si una lista de libros está ordenada correctamente.

    Args:
        lista_libros (list): Lista de objetos Libro.
        criterio (str, optional): Atributo por el cual verificar. Default: 'isbn'.
        orden (str, optional): 'asc' o 'desc'. Default: 'asc'.
    
    Returns:
        bool: True si está ordenada correctamente.
    """
    if len(lista_libros) <= 1:
        return True
    
    for i in range(1, len(lista_libros)):
        valor_anterior = obtener_valor_criterio(lista_libros[i - 1], criterio)
        valor_actual = obtener_valor_criterio(lista_libros[i], criterio)

        if orden == 'asc':
            if valor_anterior > valor_actual:
                return False
        else: # desc
            if valor_anterior < valor_actual:
                return False
    return True

def contar_comparaciones_insercion(lista_libros, criterio='isbn'):
    """
    Cuenta el número de comparaciones realizadas durante Insertion Sort.
    
    Útil para análisis de complejidad y demostración del algoritmo.
    
    Args:
        lista_libros (list): Lista de objetos Libro a ordenar.
        criterio (str, optional): Atributo por el cual ordenar. Default: 'isbn'.
    
    Returns:
        tuple: (lista_ordenada, num_comparaciones, num_movimientos)
    """
    n = len(lista_libros)
    comparaciones = 0
    movimientos = 0
    for i in range(1, n):
        libro_actual = lista_libros[i]
        valor_actual = obtener_valor_criterio(libro_actual, criterio)
        j = i - 1
        while j >= 0:
            comparaciones += 1
            valor_comparacion = obtener_valor_criterio(lista_libros[j], criterio)
            if valor_comparacion > valor_actual:
                lista_libros[j + 1] = lista_libros[j]
                movimientos += 1
                j -= 1
            else:
                break
        lista_libros[j + 1] = libro_actual
        if j + 1 != i:
            movimientos += 1
    return lista_libros, comparaciones, movimientos