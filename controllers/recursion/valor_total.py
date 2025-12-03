"""
This algorithm uses stack recursion to calculate the total value
of all books by a specific author. The work is done when "returning"
from the recursive calls.
"""

def calcular_valor_total(lista_libros, autor, indice=0):
    """
    Calculates the total value of all books by an author using stack recursion.
    
    This function demonstrates stack recursion where the calculation is done
    when RETURNING from recursive calls. The result accumulates in the call stack.
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author to search for.
        indice (int, optional): Current index in the list. Default: 0.
    
    Returns:
        float: Total accumulated value of the author's books.
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

def calcular_valor_menor(libros: list, indice: int = 0, menor_actual: dict = None):
    # Caso base: llegamos al final de la lista
    if not libros:
        return None
    # Primera llamada: Inicializar
    if menor_actual is None:
        menor_actual = {
            'libro': libros[0],
            'valor_menor': libros[0].valor
        }

    # Caso base: Llegamos al final
    if indice >= len(libros):
        return menor_actual
    
    # Obtener el libro actual
    libro_actual = libros[indice]

    # Si el valor actual es menor que el mínimo registrado
    if libro_actual.valor < menor_actual['valor_menor']:
        menor_actual['libro'] = libro_actual
        menor_actual['valor_menor'] = libro_actual.valor

    # Llamada recursiva
    return calcular_valor_menor(libros, indice + 1, menor_actual)

def calcular_valor_total_con_demostracion(lista_libros, autor, indice=0, nivel=0):
    """
    Version that demonstrates the stack recursion process in the console.
    
    Shows how the call stack is built and how values accumulate when returning.
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author to search for.
        indice (int, optional): Current index. Default: 0.
        nivel (int, optional): Depth level (for indentation). Default: 0.
    
    Returns:
        float: Calculated total value.
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
    Counts how many books an author has (helper).
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author.
        indice (int, optional): Current index. Default: 0.
    
    Returns:
        int: Number of books by the author.
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
    Obtains all books by an author using stack recursion.
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author.
        indice (int, optional): Current index. Default: 0.
    
    Returns:
        list: List of books by the author.
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
    Complete analysis of the value of books by an author using recursion.
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author to analyze.
    
    Returns:
        dict: Dictionary with complete analysis.
    """
    # Calcular usando recursión de pila
    valor_total = calcular_valor_total(lista_libros, autor)
    cantidad_libros = contar_libros_autor(lista_libros, autor)
    libros_encontrados = obtener_libros_autor(lista_libros, autor)
    
    resultado_menor = calcular_valor_menor(lista_libros)

    valor_promedio = valor_total / cantidad_libros if cantidad_libros > 0 else 0
    
    return {
        'autor': autor,
        'cantidad_libros': cantidad_libros,
        'valor_total': valor_total,
        'valor_promedio': valor_promedio,
        'libros': libros_encontrados,
        'valor_menor': resultado_menor['valor_menor'] if resultado_menor else 0,
        'libro_menor': resultado_menor['libro'] if resultado_menor else None,
    }

def demostrar_recursion_pila(lista_libros, autor):
    """
    Visually demonstrate the stack recursion process.
    
    Args:
        lista_libros (list): List of Book objects.
        autor (str): Name of the author.
    
    Returns:
        float: Calculated total value.
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