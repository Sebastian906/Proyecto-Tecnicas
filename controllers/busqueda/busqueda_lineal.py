"""
Este algoritmo se utiliza para buscar libros por Título o Autor en el
Inventario General (lista desordenada). Recorre secuencialmente toda
la colección hasta encontrar coincidencias.
"""

def busqueda_lineal_por_isbn(lista_libros, isbn):
    """
    Busca un libro por ISBN usando búsqueda lineal.
    
    Recorre secuencialmente la lista hasta encontrar el ISBN buscado.
    
    Args:
        lista_libros (list): Lista de objetos Libro (puede estar desordenada).
        isbn (str): ISBN del libro a buscar.
    
    Returns:
        tuple: (libro, indice) si se encuentra, (None, -1) si no se encuentra.
    """
    for indice, libro in enumerate(lista_libros):
        if libro.isbn == isbn:
            return libro, indice
    return None, -1

def busqueda_lineal_por_titulo(lista_libros, titulo, parcial=True):
    """
    Busca libros por título usando búsqueda lineal.
    
    Puede buscar coincidencias exactas o parciales (substring).
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        titulo (str): Título o parte del título a buscar.
        parcial (bool, optional): Si True, busca coincidencias parciales.
            Default: True.
    
    Returns:
        list: Lista de tuplas (libro, indice) con coincidencias encontradas.
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
    Busca libros por autor usando búsqueda lineal.
    
    Puede buscar coincidencias exactas o parciales (substring).
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Autor o parte del nombre del autor a buscar.
        parcial (bool, optional): Si True, busca coincidencias parciales.
            Default: True.
    
    Returns:
        list: Lista de tuplas (libro, indice) con coincidencias encontradas.
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
    Búsqueda lineal genérica por cualquier atributo del libro.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        criterio (str): Atributo por el cual buscar 
            ('isbn', 'titulo', 'autor', 'genero', etc.).
        valor: Valor a buscar (tipo depende del atributo).
        parcial (bool, optional): Solo aplica para strings. Default: False.
    
    Returns:
        list: Lista de tuplas (libro, indice) con coincidencias.
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
    Búsqueda lineal recursiva por ISBN.
    
    Implementación recursiva del algoritmo de búsqueda lineal.
    Útil para demostración académica.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        isbn (str): ISBN a buscar.
        indice (int, optional): Índice actual de búsqueda. Default: 0.
    
    Returns:
        tuple: (libro, indice) si se encuentra, (None, -1) si no se encuentra.
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
    Cuenta el número de comparaciones realizadas durante búsqueda lineal.
    
    Útil para análisis de complejidad y demostración del algoritmo.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        isbn (str): ISBN a buscar.
    
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
    Busca libros que cumplan múltiples criterios simultáneamente.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        **criterios: Pares clave=valor para filtrar.
    
    Returns:
        list: Lista de tuplas (libro, indice) que cumplen todos los criterios.
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