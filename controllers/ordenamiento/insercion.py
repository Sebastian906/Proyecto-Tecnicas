"""
This algorithm is used to keep the inventory sorted every time
a new book is added to the system, ensuring that the list is always 
ordered by ISBN in ascending order to allow binary search.

Time Complexity:
    - Best case: O(n) -> the list is already sorted
    - Average case: O(n²)
    - Worst case: O(n²)

Space Complexity: O(1) - in-place sorting
"""

def ordenamiento_insercion(lista_libros, criterio='isbn', orden='asc'):
    """
    Sorts a list of books using the insertion sort algorithm.

    This algorithm compares each element with the previous ones and inserts it
    in the correct position. It is efficient for small or nearly sorted lists.
    
    Args:
        lista_libros (list): List of Book objects to sort.
        criterio (str, optional): Attribute to sort by. 
            Options: 'isbn', 'titulo', 'autor', 'peso', 'valor'.
            Default: 'isbn'.
        orden (str, optional): 'asc' for ascending, 'desc' for descending.
            Default: 'asc'.
    
    Returns:
        list: The same sorted list (modified in-place).
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
    Inserts a new book into an already sorted list while maintaining order.
    
    This is an optimization of Insertion Sort to add a single element
    to a list that is already sorted. Used in the Ordered Inventory.
    
    Args:
        lista_ordenada (list): Already sorted list of books.
        libro_nuevo (Libro): Book to insert.
        criterio (str, optional): Attribute by which the list is sorted.
            Default: 'isbn'.
    
    Returns:
        int: Index where the book was inserted.
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
    Obtains the value of the specified attribute from a book.
    
    Args:
        libro (Libro): Book object.
        criterio (str): Name of the attribute.
    
    Returns:
        any: Value of the attribute (str, float, int).
    
    Raises:
        AttributeError: If the attribute does not exist in the Book object.
    """
    if not hasattr(libro, criterio):
        raise AttributeError(f"El libro no tiene el atributo '{criterio}'")
    return getattr(libro, criterio)

def verificar_orden(lista_libros, criterio='isbn', orden='asc'):
    """
    Verifies if a list of books is correctly ordered.

    Args:
        lista_libros (list): List of Book objects.
        criterio (str, optional): Attribute by which to verify. Default: 'isbn'.
        orden (str, optional): 'asc' or 'desc'. Default: 'asc'.
    
    Returns:
        bool: True if correctly ordered.
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
    Counts the number of comparisons made during Insertion Sort.
    
    Useful for complexity analysis and algorithm demonstration.
    
    Args:
        lista_libros (list): List of Book objects to sort.
        criterio (str, optional): Attribute by which to sort. Default: 'isbn'.
    
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