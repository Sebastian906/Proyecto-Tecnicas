"""
Este algoritmo encuentra todas las combinaciones posibles que 
superan el umbral de riesgo de 8 Kg. (estantería deficiente).
"""

from itertools import combinations

def encontrar_combinaciones(lista_libros, num_libros=4, peso_maximo=8.0):
    """
    Encuentra todas las combinaciones de libros que exceden el peso máximo.
    
    Este algoritmo de fuerza bruta explora TODAS las combinaciones posibles
    de 'num_libros' libros y retorna aquellas cuyo peso total supera el
    umbral de riesgo (8 Kg).
    
    Args:
        lista_libros (list): Lista de objetos Libro disponibles.
        num_libros (int, optional): Cantidad de libros por combinación. Default: 4.
        peso_maximo (float, optional): Peso máximo permitido en Kg. Default: 8.0.
    
    Returns:
        list: Lista de tuplas, cada una contiene:
            - (libros_tuple, peso_total, exceso)
            donde libros_tuple es una tupla de 4 libros.
    """
    combinaciones_peligrosas = []
    total_combinaciones = 0
    
    # Generar todas las combinaciones posibles de 'num_libros' libros
    print(f"\nExplorando todas las combinaciones de {num_libros} libros...")
    for combinacion in combinations(lista_libros, num_libros):
        total_combinaciones += 1
    
        # Calcular peso total de esta combinación
        peso_total = sum(libro.peso for libro in combinacion)
    
        # Si excede el límite, es peligrosa
        if peso_total > peso_maximo:
            exceso = peso_total - peso_maximo
            combinaciones_peligrosas.append((combinacion, peso_total, exceso))
    print(f"Exploración completada: {total_combinaciones} combinaciones analizadas")
    print(f"Combinaciones peligrosas encontradas: {len(combinaciones_peligrosas)}")
    
    return combinaciones_peligrosas

def demostrar_exploracion_fuerza_bruta(lista_libros, num_libros=4, peso_maximo=8.0, mostrar_primeras=15):
    """
    Demuestra paso a paso la exploración exhaustiva de fuerza bruta.
    
    Imprime en consola el proceso de exploración para fines educativos.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        num_libros (int, optional): Cantidad de libros. Default: 4.
        peso_maximo (float, optional): Peso máximo en Kg. Default: 8.0.
        mostrar_primeras (int, optional): Cuántas combinaciones mostrar. Default: 15.
    
    Returns:
        list: Lista de combinaciones peligrosas encontradas.
    """
    print("Exploración Exhaustiva - Fuerza Bruta")
    print(f"\nParámetros:")
    print(f"  • Total de libros: {len(lista_libros)}")
    print(f"  • Libros por combinación: {num_libros}")
    print(f"  • Peso máximo permitido: {peso_maximo} Kg")
    print(f"  • Umbral de riesgo: > {peso_maximo} Kg")
    
    from math import comb
    total_posibles = comb(len(lista_libros), num_libros)
    print(f"  • Total de combinaciones a explorar: {total_posibles:,}")
    print(f"\nExplorando TODAS las combinaciones...\n")

    combinaciones_peligrosas = []
    combinacion_num = 0
    peligrosas_encontradas = 0
    
    for combinacion in combinations(lista_libros, num_libros):
        combinacion_num += 1
        peso_total = sum(libro.peso for libro in combinacion)

        # Mostrar solo las primeras N combinaciones
        if combinacion_num <= mostrar_primeras:
            isbns = [libro.isbn[-4:] for libro in combinacion]
            estado = "PELIGROSA" if peso_total > peso_maximo else "Segura"
            print(f"  [{combinacion_num:3d}] ISBNs: {isbns} | Peso: {peso_total:5.2f} Kg | {estado}")
        elif combinacion_num == mostrar_primeras + 1:
            print(f"  ... (explorando {total_posibles - mostrar_primeras:,} combinaciones más) ...")
        
        # Registrar si es peligrosa
        if peso_total > peso_maximo:
            exceso = peso_total - peso_maximo
            combinaciones_peligrosas.append((combinacion, peso_total, exceso))
            peligrosas_encontradas += 1

    print(f"RESULTADO DE LA EXPLORACIÓN:")
    print(f"  • Combinaciones exploradas: {combinacion_num:,}")
    print(f"  • Combinaciones PELIGROSAS encontradas: {peligrosas_encontradas}")
    print(f"  • Porcentaje peligrosas: {(peligrosas_encontradas/combinacion_num*100):.2f}%")

    return combinaciones_peligrosas