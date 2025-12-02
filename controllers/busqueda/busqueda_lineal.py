"""
This algorithm is used to search for books by Title or Author in the
General Inventory (unordered list). . It sequentially traverses the entire
collection until it finds matches.
"""

def busqueda_lineal_por_isbn(lista_libros, isbn):
    """
    Search for a book by ISBN using linear search.
    
    Sequentially traverses the list until the searched ISBN is found.
    
    Args:
        lista_libros (list): List of Book objects (can be unordered).
        isbn (str): ISBN of the book to search for.
    
    Returns:
        tuple: (libro, índice) if found, (None, -1) if not found.
    """
    for indice, libro in enumerate(lista_libros):
        if libro.isbn == isbn:
            return libro, indice
    return None, -1

def busqueda_lineal_por_titulo(lista_libros, titulo, parcial=True):
    """
    Search for books by title using linear search.
    
    Can search for exact or partial matches (substring).
    
    Args:
        lista_libros (list): List of Book objects.
        titulo (str): Title or part of the title to search for.
        parcial (bool, optional): If True, searches for partial matches.
            Default: True.
    
    Returns:
        list: List of tuples (libro, índice) with found matches.
    """
    resultados = []
    titulo_busqueda = titulo.lower()
    for indice, libro in enumerate(lista_libros):
        titulo_libro = libro.titulo.lower()
        if parcial:
            # Búsqueda parcial (substring)
            if titulo_busqueda in titulo_libro:
                resultados.append((libro, indice))
        else:
            # Búsqueda exacta
            if titulo_busqueda == titulo_libro:
                resultados.append((libro, indice))
    return resultados

def busqueda_lineal_por_autor(lista_libros, autor, parcial=True):
    """
    Search for books by author using linear search.
    
    Can search for exact or partial matches (substring).
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Author or part of the author's name to search for.
        parcial (bool, optional): If True, searches for partial matches.
            Default: True.
    
    Returns:
        list: List of tuples (libro, índice) with found matches.
    """
    resultados = []
    autor_busqueda = autor.lower()
    for indice, libro in enumerate(lista_libros):
        autor_libro = libro.autor.lower()
        if parcial:
            # Búsqueda parcial (substring)
            if autor_busqueda in autor_libro:
                resultados.append((libro, indice))
        else:
            # Búsqueda exacta
            if autor_busqueda == autor_libro:
                resultados.append((libro, indice))
    return resultados

def busqueda_lineal_por_criterio(lista_libros, criterio, valor, parcial=False):
    """
    Generic linear search by any attribute of the book.
    
    Args:
        lista_libros (list): List of Book objects.
        criterio (str): Attribute to search by 
            ('isbn', 'titulo', 'autor', 'genero', etc.).
        valor: Value to search for (type depends on the attribute).
        parcial (bool, optional): Only applies to strings. Default: False.
    
    Returns:
        list: List of tuples (libro, índice) with found matches.
    """
    resultados = []
    for indice, libro in enumerate(lista_libros):
        if not hasattr(libro, criterio):
            continue
        valor_libro = getattr(libro, criterio)
        # Si es string y se busca parcialmente
        if isinstance(valor, str) and isinstance(valor_libro, str) and parcial:
            if valor.lower() in valor_libro.lower():
                resultados.append((libro, indice))
        else:
            # Comparación exacta
            if valor_libro == valor:
                resultados.append((libro, indice))
    return resultados

def busqueda_lineal_recursiva(lista_libros, isbn, indice=0):
    """
    Recursive linear search by ISBN.
    
    Recursive implementation of the linear search algorithm.
    Useful for academic demonstration.
    
    Args:
        lista_libros (list): List of Book objects.
        isbn (str): ISBN to search for.
        indice (int, optional): Current search index. Default: 0.
    
    Returns:
        tuple: (libro, indice) if found, (None, -1) if not found.
    """
    # Caso base: llegamos al final de la lista sin encontrar nada
    if indice >= len(lista_libros):
        return None, -1
    # Caso base: se encuentra la lista
    if lista_libros[indice].isbn == isbn:
        return lista_libros[indice], indice
    # Caso recursivo: seguir buscando
    return busqueda_lineal_recursiva(lista_libros, isbn, indice + 1)

def contar_comparaciones_lineal(lista_libros, isbn):
    """
    Count the number of comparisons performed during linear search.
    
    Useful for complexity analysis and algorithm demonstration.
    
    Args:
        lista_libros (list): List of Book objects.
        isbn (str): ISBN to search for.
    
    Returns:
        tuple: (libro, indice, comparaciones)
    """
    comparaciones = 0
    for indice, libro in enumerate(lista_libros):
        comparaciones += 1
        if libro.isbn == isbn:
            return libro, indice, comparaciones
    return None, -1, comparaciones

def busqueda_multiple(lista_libros, **criterios):
    """
    Search for books that meet multiple criteria simultaneously.
    
    Args:
        lista_libros (list): List of Book objects.
        **criterios: Key=value pairs to filter by.
    
    Returns:
        list: List of tuples (libro, indice) that meet all criteria.
    """
    resultados = []
    for indice, libro in enumerate(lista_libros):
        cumple_todos = True
        for atributo, valor in criterios.items():
            if not hasattr(libro, atributo):
                cumple_todos = False
                break
            valor_libro = getattr(libro, atributo)
            # Comparación parcial para strings
            if isinstance(valor, str) and isinstance(valor_libro, str):
                if valor.lower() not in valor_libro.lower():
                    cumple_todos = False
                    break
            else:
                if valor_libro != valor:
                    cumple_todos = False
                    break
        if cumple_todos:
            resultados.append((libro, indice))
    return resultados