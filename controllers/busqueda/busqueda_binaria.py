"""
This algorithm is used to search for books by ISBN in the Sorted Inventory.
It is CRITICAL for checking pending reservations when a book is returned.

The list MUST be sorted by ISBN (ascending) for
this algorithm to work correctly.
"""

def busqueda_binaria_por_isbn(lista_libros, isbn):
    """
    Search for a book by ISBN using binary search.

    This function is mandatory for checking if a returned book
    has pending reservations in the waiting queue.

    Args:
        lista_libros (list): List of Book objects sorted by ISBN.
        isbn (str): ISBN of the book to search for.

    Returns:
        tuple: (libro, índice) if found, (None, -1) if not found.
    Raises: 
        ValueError: If the list is not sorted by ISBN.
    """
    izquierda = 0
    derecha = len(lista_libros) - 1
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        isbn_medio = lista_libros[medio].isbn
        if isbn_medio == isbn:
            # Libros encontrados
            return lista_libros[medio], medio
        elif isbn_medio < isbn:
            # Buscar en la mitad izquierda
            izquierda = medio + 1
        else:
            # Buscar en la mitad derecha
            derecha = medio - 1
    # No encontrado
    return None, -1

def busqueda_binaria_recursiva(lista_libros, isbn, izquierda=0, derecha=None):
    """
    Recursive binary search to find a book by ISBN.

    Implements the same algorithm as `busqueda_binaria_por_isbn` but recursively.

    Args:
        lista_libros_ordenados (list): List sorted by ISBN.
        isbn (str): ISBN to search for.
        izquierda (int, optional): Left index. Default: 0.
        derecha (int, optional): Right index. Default: len-1.
    
    Returns:
        tuple: (libro, índice) if found, (None, -1) if not found.
    """
    if derecha is None:
        derecha = len(lista_libros) - 1
    # Caso base: no encontrado
    if izquierda > derecha:
        return None, -1
    medio = izquierda + (derecha - izquierda) // 2
    isbn_medio = lista_libros[medio].isbn
    # Caso base: encontrado
    if isbn_medio == isbn:
        return lista_libros[medio], medio
    # Casos recursivos
    elif isbn < isbn_medio:
        return busqueda_binaria_recursiva(lista_libros, isbn, izquierda, medio - 1)
    else:
        return busqueda_binaria_recursiva(lista_libros, isbn, medio + 1, derecha)
    
def busqueda_binaria_por_criterio(lista_ordenada, criterio, valor):
    """
    Binary search by a specific attribute.

    The list must be sorted by the given criterion.

    Args:
        lista_ordenada (list): Sorted list of objects.
        criterio (str): Attribute to search by.
        valor: Value to search for.
    
    Returns:
        tuple: (object, index) if found, (None, -1) if not found.
    """
    izquierda = 0
    derecha = len(lista_ordenada) - 1
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        valor_medio = getattr(lista_ordenada[medio], criterio)
        if valor_medio == valor:
            return lista_ordenada[medio], medio
        elif valor_medio < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None, -1

def encontrar_primera_ocurrencia(lista_libros, isbn):
    """
    Finds the first occurrence of an ISBN in a sorted list.
    
    Useful if there are duplicate books (same ISBN) in the inventory.
    
    Args:
        lista_libros_ordenados (list): List sorted by ISBN.
        isbn (str): ISBN to search for.
    
    Returns:
        tuple: (libro, índice) of the first occurrence, or (None, -1).
    """
    izquierda = 0
    derecha = len(lista_libros) - 1
    resultado = -1
    libro_encontrado = None
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        isbn_medio = lista_libros[medio].isbn
        if isbn_medio == isbn:
            resultado = medio
            libro_encontrado = lista_libros[medio]
            # Seguir buscando a la izquierda
            derecha = medio - 1 
        elif isbn_medio > isbn:
            derecha = medio - 1
        else:
            izquierda = medio + 1
    return libro_encontrado, resultado

def encontrar_ultima_ocurrencia(lista_libros, isbn):
    """
    Finds the last occurrence of an ISBN in a sorted list.
    
    Args:
        lista_libros_ordenados (list): List sorted by ISBN.
        isbn (str): ISBN to search for.
    
    Returns:
        tuple: (libro, índice) of the last occurrence, or (None, -1).
    """
    izquierda = 0
    derecha = len(lista_libros) - 1
    resultado = -1
    libro_encontrado = None
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        isbn_medio = lista_libros[medio].isbn
        if isbn_medio == isbn:
            resultado = medio
            libro_encontrado = lista_libros[medio]
            # Seguir buscando a la derecha
            izquierda = medio + 1 
        elif isbn_medio > isbn:
            derecha = medio - 1
        else:
            izquierda = medio + 1
    return libro_encontrado, resultado

def contar_comparaciones_binarias(lista_libros, isbn):
    """
    Counts the number of comparisons made during binary search.
    
    Useful for complexity analysis and algorithm demonstration.
    
    Args:
        lista_libros_ordenados (list): List sorted by ISBN.
        isbn (str): ISBN to search for.
    
    Returns:
        tuple: (libro, índice, comparaciones)
    """
    izquierda = 0
    derecha = len(lista_libros) - 1
    comparaciones = 0
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        comparaciones += 1
        isbn_medio = lista_libros[medio].isbn
        if isbn_medio == isbn:
            return lista_libros[medio], medio, comparaciones
        elif isbn < isbn_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1
    return None, -1, comparaciones

def verificar_lista_ordenada(lista_libros, criterio='isbn'):
    """
    Checks if a list is correctly sorted.
    
    Call this function before using binary search
    to avoid incorrect results.
    
    Args:
        lista_libros (list): List of books to check.
        criterio (str, optional): Attribute to check by. Default: 'isbn'.
    
    Returns:
        bool: True if correctly sorted.
    """
    if len(lista_libros) <= 1:
        return True
    for i in range(1, len(lista_libros)):
        valor_anterior = getattr(lista_libros[i - 1], criterio)
        valor_actual = getattr(lista_libros[i], criterio)
        if valor_anterior > valor_actual:
            return False
    return True

def busqueda_binaria_con_validacion(lista_libros, isbn):
    """
    Binary search with automatic order validation.
    
    Checks if the list is sorted before searching.
    Safer but with additional overhead.
    
    Args:
        lista_libros (list): List of books.
        isbn (str): ISBN to search for.
    
    Returns:
        tuple: (libro, índice)
    
    Raises:
        ValueError: If the list is not sorted by ISBN.
    """
    if not verificar_lista_ordenada(lista_libros, 'isbn'):
        raise ValueError("La lista no está ordenada por ISBN.")
    return busqueda_binaria_por_isbn(lista_libros, isbn)