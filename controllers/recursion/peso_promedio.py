"""
Este algoritmo utiliza recursión de cola (tail recursion) para calcular
el peso promedio de todos los libros de un autor. El trabajo se realiza
antes de la llamada recursiva, usando acumuladores.
"""

def calcular_peso_promedio(lista_libros, autor, indice=0, peso_acumulado=0.0, cantidad_libros=0):
    """
    Calcula el peso promedio de libros de un autor usando recursión de cola.
    
    Esta función demuestra la recursión de cola donde el cálculo se realiza
    antes de la llamada recursiva. Usa acumuladores para mantener el estado.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor a buscar.
        indice (int, optional): Índice actual en la lista. Default: 0.
        peso_acumulado (float, optional): Peso acumulado hasta ahora. Default: 0.0.
        cantidad_libros (int, optional): Cantidad de libros contados. Default: 0.
    
    Returns:
        float: Peso promedio de los libros del autor.
    """
    # Caso base: llegamos al final de la lista
    if indice >= len(lista_libros):
        # Calcular promedio final
        if cantidad_libros > 0:
            return peso_acumulado / cantidad_libros
        return 0.0
    libro_actual = lista_libros[indice]
    # Verificar si el libro es del autor buscado
    if autor.lower() in libro_actual.autor.lower():
        # Antes de la recursión: actualizar acumuladores
        nuevo_peso = peso_acumulado + libro_actual.peso
        nueva_cantidad = cantidad_libros + 1
        # Llamada recursiva de cola (última operación)
        return calcular_peso_promedio(
            lista_libros, autor, indice + 1, nuevo_peso, nueva_cantidad
        )
    else:
        # Si no es del autor, continuar sin actualizar acumuladores
        return calcular_peso_promedio(
            lista_libros, autor, indice + 1, peso_acumulado, cantidad_libros
        )

def calcular_peso_promedio_con_demostracion(lista_libros, autor, indice=0, peso_acumulado=0.0, cantidad_libros=0, nivel=0):
    """
    Versión que demuestra el proceso de recursión de cola en consola.
    
    Muestra cómo se van actualizando los acumuladores ANTES de cada
    llamada recursiva (característica clave de tail recursion).
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor a buscar.
        indice (int, optional): Índice actual. Default: 0.
        peso_acumulado (float, optional): Peso acumulado. Default: 0.0.
        cantidad_libros (int, optional): Cantidad contada. Default: 0.
        nivel (int, optional): Nivel de profundidad. Default: 0.
    
    Returns:
        float: Peso promedio calculado.
    """
    margen = "  " * nivel
    # Caso base
    if indice >= len(lista_libros):
        promedio = peso_acumulado / cantidad_libros if cantidad_libros > 0 else 0.0
        print(f"{margen}[Caso base] Fin de la lista")
        print(f"{margen}  Peso acumulado: {peso_acumulado:.2f} Kg")
        print(f"{margen}  Cantidad de libros: {cantidad_libros}")
        print(f"{margen}  Promedio final: {promedio:.2f} Kg")
        return promedio
    libro_actual = lista_libros[indice]

    if autor.lower() in libro_actual.autor.lower():
        # Actualizar acumuladores ANTES de la llamada recursiva
        nuevo_peso = peso_acumulado + libro_actual.peso
        nueva_cantidad = cantidad_libros + 1
        print(f"{margen}[{nivel}] Libro #{indice+1}: {libro_actual.titulo[:40]}")
        print(f"{margen}    Peso: {libro_actual.peso} Kg")
        print(f"{margen}    → Acumulando: {peso_acumulado:.2f} + {libro_actual.peso} = {nuevo_peso:.2f} Kg")
        print(f"{margen}    → Libros contados: {nueva_cantidad}")
        print(f"{margen}    → Llamada recursiva (TAIL CALL)...")
        # Llamada recursiva de cola (última operación)
        return calcular_peso_promedio_con_demostracion(
            lista_libros, autor, indice + 1, nuevo_peso, nueva_cantidad, nivel + 1
        )
    else:
        # No es del autor, continuar sin modificar acumuladores
        return calcular_peso_promedio_con_demostracion(
            lista_libros, autor, indice + 1, peso_acumulado, cantidad_libros, nivel
        )

def calcular_estadisticas_peso(lista_libros, autor):
    """
    Calcula estadísticas completas del peso usando recursión de cola.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor.
    
    Returns:
        dict: Diccionario con estadísticas completas.
    """
    # Funciones auxiliares con recursión de cola
    def calcular_peso_total(libros, indice=0, acumulado=0.0):
        if indice >= len(libros):
            return acumulado
        libro = libros[indice]
        if autor.lower() in libro.autor.lower():
            return calcular_peso_total(libros, indice + 1, acumulado + libro.peso)
        return calcular_peso_total(libros, indice + 1, acumulado)
    
    def contar_libros(libros, indice=0, contador=0):
        if indice >= len(libros):
            return contador
        libro = libros[indice]
        if autor.lower() in libro.autor.lower():
            return contar_libros(libros, indice + 1, contador + 1)
        return contar_libros(libros, indice + 1, contador)
    
    def calcular_peso_minimo(libros, indice=0, minimo=float('inf')):
        if indice >= len(libros):
            return minimo if minimo != float('inf') else 0.0
        libro = libros[indice]
        if autor.lower() in libro.autor.lower():
            nuevo_minimo = min(minimo, libro.peso)
            return calcular_peso_minimo(libros, indice + 1, nuevo_minimo)
        return calcular_peso_minimo(libros, indice + 1, minimo)
    
    def calcular_peso_maximo(libros, indice=0, maximo=0.0):
        if indice >= len(libros):
            return maximo
        libro = libros[indice]
        if autor.lower() in libro.autor.lower():
            nuevo_maximo = max(maximo, libro.peso)
            return calcular_peso_maximo(libros, indice + 1, nuevo_maximo)
        return calcular_peso_maximo(libros, indice + 1, maximo)
    # Calcular todas las estadísticas
    peso_total = calcular_peso_total(lista_libros)
    cantidad = contar_libros(lista_libros)
    peso_promedio = peso_total / cantidad if cantidad > 0 else 0.0
    peso_minimo = calcular_peso_minimo(lista_libros)
    peso_maximo = calcular_peso_maximo(lista_libros)
    return {
        'autor': autor,
        'cantidad_libros': cantidad,
        'peso_total': peso_total,
        'peso_promedio': peso_promedio,
        'peso_minimo': peso_minimo,
        'peso_maximo': peso_maximo
    }

def demostrar_recursion_cola(lista_libros, autor):
    """
    Demuestra visualmente el proceso de recursión de cola.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        autor (str): Nombre del autor.
    
    Returns:
        float: Peso promedio calculado.
    """
    print("Recursión de Cola - Cálculo de Peso Promedio")
    print(f"\nAutor buscado: {autor}")
    print(f"Total de libros en el inventario: {len(lista_libros)}")
    print("\nProceso de recursión de cola (con acumuladores):")
    peso_promedio = calcular_peso_promedio_con_demostracion(lista_libros, autor)
    print(f"\nRESULTADO FINAL: {peso_promedio:.2f} Kg")
    # Estadísticas adicionales
    stats = calcular_estadisticas_peso(lista_libros, autor)
    print(f"\nEstadísticas completas de {autor}:")
    print(f"  • Libros encontrados: {stats['cantidad_libros']}")
    print(f"  • Peso total: {stats['peso_total']:.2f} Kg")
    print(f"  • Peso promedio: {stats['peso_promedio']:.2f} Kg")
    print(f"  • Peso mínimo: {stats['peso_minimo']:.2f} Kg")
    print(f"  • Peso máximo: {stats['peso_maximo']:.2f} Kg")
    print("EXPLICACIÓN:")
    print("  • Recursión de COLA: El cálculo se hace ANTES de llamar")
    print("  • Usa acumuladores para mantener el estado")
    print("  • La llamada recursiva es lo ÚLTIMO que se ejecuta")
    print("  • Puede ser optimizada (Tail Call Optimization)")
    print("  • No acumula en la pila de llamadas")
    return peso_promedio

