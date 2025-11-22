"""
Este algoritmo se utiliza para buscar libros por ISBN en el Inventario
Ordenado. Es CRÍTICO para verificar reservas pendientes cuando se devuelve
un libro.

La lista DEBE estar ordenada por ISBN (ascendente) para que
este algoritmo funcione correctamente.
"""

def busqueda_binaria_por_isbn(lista_libros, isbn):
    """
    Buscar un libro por ISBN usando búsqueda binaria.

    Esta función es usada obligatoriamente para verificar si un libro
    devuelto tiene reservas pendientes en la cola de espera.

    Args:
        lista_libros (list): Lista de objetos Libro ordenada por ISBN.
        isbn (str): ISBN del libro a buscar.

    Returns:
        tuple: (libro, indice) si se encuentra, (None, -1) si no se encuentra.

    Raises: 
        ValueError: Si la lista no está ordenada por ISBN.
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
    Búsqueda binaria recursiva para encontrar un libro por ISBN.

    Implementa el mismo algoritmo que `busqueda_binaria_por_isbn` pero de forma recursiva.

    Args:
        lista_libros_ordenados (list): Lista ordenada por ISBN.
        isbn (str): ISBN a buscar.
        izquierda (int, optional): Índice izquierdo. Default: 0.
        derecha (int, optional): Índice derecho. Default: len-1.
    
    Returns:
        tuple: (libro, indice) si se encuentra, (None, -1) si no se encuentra.
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
    Búsqueda binaria por un atributo específico.

    La lista debe estar ordenada por el criterio dado

    Args:
        lista_ordenada (list): Lista ordenada de objetos.
        criterio (str): Atributo por el cual buscar.
        valor: Valor a buscar.
    
    Returns:
        tuple: (objeto, indice) si se encuentra, (None, -1) si no se encuentra.
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
    Encuentra la primera ocurrencia de un ISBN en una lista ordenada.
    
    Útil si hay libros duplicados (mismo ISBN) en el inventario.
    
    Args:
        lista_libros_ordenados (list): Lista ordenada por ISBN.
        isbn (str): ISBN a buscar.
    
    Returns:
        tuple: (libro, indice) de la primera ocurrencia, o (None, -1).
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
    Encuentra la última ocurrencia de un ISBN en una lista ordenada.
    
    Args:
        lista_libros_ordenados (list): Lista ordenada por ISBN.
        isbn (str): ISBN a buscar.
    
    Returns:
        tuple: (libro, indice) de la última ocurrencia, o (None, -1).
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
    Cuenta el número de comparaciones realizadas durante búsqueda binaria.
    
    Útil para análisis de complejidad y demostración del algoritmo.
    
    Args:
        lista_libros_ordenados (list): Lista ordenada por ISBN.
        isbn (str): ISBN a buscar.
    
    Returns:
        tuple: (libro, indice, comparaciones)
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
    Verifica si una lista está correctamente ordenada.
    
    Llamar a esta función antes de usar búsqueda binaria
    para evitar resultados incorrectos.
    
    Args:
        lista_libros (list): Lista de libros a verificar.
        criterio (str, optional): Atributo por el cual verificar. Default: 'isbn'.
    
    Returns:
        bool: True si está ordenada correctamente.
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
    Búsqueda binaria con validación automática del orden.
    
    Verifica que la lista esté ordenada antes de buscar.
    Más seguro pero con overhead adicional.
    
    Args:
        lista_libros (list): Lista de libros.
        isbn (str): ISBN a buscar.
    
    Returns:
        tuple: (libro, indice)
    
    Raises:
        ValueError: Si la lista no está ordenada por ISBN.
    """
    if not verificar_lista_ordenada(lista_libros, 'isbn'):
        raise ValueError("La lista no está ordenada por ISBN.")
    return busqueda_binaria_por_isbn(lista_libros, isbn)