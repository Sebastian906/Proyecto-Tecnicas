"""
Este algoritmo utiliza recursión de pila para calcular el valor total
de todos los libros de un autor específico. El trabajo se realiza al
"regresar" de las llamadas recursivas.
"""

def calcular_valor_total(lista_libros, autor, indice=0):
    """
    Calcula el valor total de todos los libros de un autor usando recursión de pila.
    
    Esta función demuestra la recursión de pila donde el cálculo se realiza
    al REGRESAR de las llamadas recursivas. El resultado se acumula en la pila
    de llamadas.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor a buscar.
        indice (int, optional): Índice actual en la lista. Default: 0.
    
    Returns:
        float: Valor total acumulado de los libros del autor.
    """
    # Caso base: llegamos al final de la lista
    if indice >= len(lista_libros):
        return 0.0
    libro_actual = lista_libros[indice]
    # Verificar si el libro es del autor buscado
    if autor.lower() in libro_actual.autor.lower():
        # Recursión: obtener el valor del resto de los libros
        valor_resto = calcular_valor_total(lista_libros, autor, indice + 1)
        # El trabajo se hace al regresar: Sumar el valor del libro actual con el resto
        return libro_actual.valor + valor_resto
    else:
        # Si no es del autor, solo continuar con el siguiente
        return calcular_valor_total(lista_libros, autor, indice + 1)

def calcular_valor_total_con_demostracion(lista_libros, autor, indice=0, nivel=0):
    """
    Versión que demuestra el proceso de recursión de pila en consola.
    
    Muestra cómo se construye la pila de llamadas y cómo se van
    acumulando los valores al regresar.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor a buscar.
        indice (int, optional): Índice actual. Default: 0.
        nivel (int, optional): Nivel de profundidad (para indentación). Default: 0.
    
    Returns:
        float: Valor total calculado.
    """
    margen = "  " * nivel
    # Caso base
    if indice >= len(lista_libros):
        print(f"{margen}[Caso base] Fin de la lista, retornando 0")
        return 0.0
    
    libro_actual = lista_libros[indice]
    
    if autor.lower() in libro_actual.autor.lower():
        print(f"{margen}→ [{nivel}] Libro: {libro_actual.titulo[:40]}")
        print(f"{margen}   Valor: ${libro_actual.valor:,.0f} | Llamando recursivamente...")
        # Llamada recursiva (bajando por la pila)
        valor_resto = calcular_valor_total_con_demostracion(
            lista_libros, autor, indice + 1, nivel + 1
        )
        # Trabajo al regresar (subiendo por la pila)
        valor_total = libro_actual.valor + valor_resto
        print(f"{margen}← [{nivel}] Regresando: ${libro_actual.valor:,.0f} + ${valor_resto:,.0f} = ${valor_total:,.0f}")
        return valor_total
    else:
        # No es del autor, seguir buscando
        return calcular_valor_total_con_demostracion(
            lista_libros, autor, indice + 1, nivel
        )

def contar_libros_autor(lista_libros, autor, indice=0):
    """
    Cuenta cuántos libros tiene un autor (auxiliar).
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor.
        indice (int, optional): Índice actual. Default: 0.
    
    Returns:
        int: Cantidad de libros del autor.
    """
    if indice >= len(lista_libros):
        return 0
    
    libro_actual = lista_libros[indice]
    
    if autor.lower() in libro_actual.autor.lower():
        return 1 + contar_libros_autor(lista_libros, autor, indice + 1)
    else:
        return contar_libros_autor(lista_libros, autor, indice + 1)

def obtener_libros_autor(lista_libros, autor, indice=0):
    """
    Obtiene todos los libros de un autor usando recursión de pila.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor.
        indice (int, optional): Índice actual. Default: 0.
    
    Returns:
        list: Lista de libros del autor.
    """
    if indice >= len(lista_libros):
        return []
    
    libro_actual = lista_libros[indice]
    libros_resto = obtener_libros_autor(lista_libros, autor, indice + 1)
    
    if autor.lower() in libro_actual.autor.lower():
        return [libro_actual] + libros_resto
    else:
        return libros_resto

def analizar_valor_por_autor(lista_libros, autor):
    """
    Análisis completo del valor de libros de un autor usando recursión.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor a analizar.
    
    Returns:
        dict: Diccionario con análisis completo.
    """
    # Calcular usando recursión de pila
    valor_total = calcular_valor_total(lista_libros, autor)
    cantidad_libros = contar_libros_autor(lista_libros, autor)
    libros_encontrados = obtener_libros_autor(lista_libros, autor)
    
    valor_promedio = valor_total / cantidad_libros if cantidad_libros > 0 else 0
    
    return {
        'autor': autor,
        'cantidad_libros': cantidad_libros,
        'valor_total': valor_total,
        'valor_promedio': valor_promedio,
        'libros': libros_encontrados
    }

def demostrar_recursion_pila(lista_libros, autor):
    """
    Demuestra visualmente el proceso de recursión de pila.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor.
    
    Returns:
        float: Valor total calculado.
    """
    print("Recursión de Pila - Cálculo de Valor Total")
    print(f"\nAutor buscado: {autor}")
    print(f"Total de libros en el inventario: {len(lista_libros)}")
    print("\nProceso de recursión (se muestra la pila de llamadas):")
    
    valor_total = calcular_valor_total_con_demostracion(lista_libros, autor)
    
    print(f"\nRESULTADO FINAL: ${valor_total:,.0f} COP")
    # Análisis adicional
    analisis = analizar_valor_por_autor(lista_libros, autor)
    print(f"\nEstadísticas:")
    print(f"  • Libros encontrados: {analisis['cantidad_libros']}")
    print(f"  • Valor total: ${analisis['valor_total']:,.0f} COP")
    print(f"  • Valor promedio por libro: ${analisis['valor_promedio']:,.0f} COP")
    print(f"\nLibros de {autor}:")
    for i, libro in enumerate(analisis['libros'], 1):
        print(f"  {i}. {libro.titulo} - ${libro.valor:,.0f} COP")
    print("EXPLICACIÓN:")
    print("  • Recursión de PILA: El cálculo se hace AL REGRESAR")
    print("  • Cada llamada espera el resultado de la siguiente")
    print("  • Se acumula en la pila de llamadas del sistema")
    print("  • No es tail-recursive (no optimizable por el compilador)")
    return valor_total