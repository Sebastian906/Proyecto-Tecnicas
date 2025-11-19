"""
Este algoritmo se utiliza para generar Reportes Globales de inventario
ordenados por el atributo Valor (COP). Es eficiente para listas grandes
y garantiza un rendimiento O(n log n).

Complejidad Temporal: O(n log n) en todos los casos
Complejidad Espacial: O(n) - requiere espacio adicional para la mezcla
"""

import csv
import json
from datetime import datetime
import os

from models import libro

def merge_sort(lista_libros, criterio='valor', orden='asc'):
    """
    Ordena una lista de libros usando el algoritmo Merge Sort.

    Este algoritmo divide recursivamente la lista en mitades, 
    las ordena y luego las combina. Eficiente para listas grandes.
    
    Args:
        lista_libros (list): Lista de objetos Libro a ordenar.
        criterio (str, optional): Atributo por el cual ordenar.
            Opciones: 'isbn', 'titulo', 'autor', 'peso', 'valor'.
            Default: 'valor'.
        orden (str, optional): 'asc' para ascendente, 'desc' para descendente.
            Default: 'asc'.
    
    Returns:
        list: Nueva lista ordenada (no modifica la original).
    
    Example:
        >>> libros_ordenados = merge_sort(libros, criterio='valor', orden='desc')
        >>> # Reporte con libros más caros primero
    """
    # Caso base: lista vacía o con un solo elemento
    if len(lista_libros) <= 1:
        return lista_libros.copy()
    # Dividir la lista en dos mitades
    medio = len(lista_libros) // 2
    izquierda = lista_libros[:medio]
    derecha = lista_libros[medio:]
    # Ordenar recursivamente cada mitad
    izquierda_ordenada = merge_sort(izquierda, criterio, orden)
    derecha_ordenada = merge_sort(derecha, criterio, orden)
    # Combinar las dos mitades ordenadas
    return merge(izquierda_ordenada, derecha_ordenada, criterio, orden)

def merge(izquierda, derecha, criterio, orden):
    """
    Combina dos listas ordenadas en una sola lista ordenada.
    
    Args:
        izquierda (list): Primera sublista ordenada.
        derecha (list): Segunda sublista ordenada.
        criterio (str): Atributo por el cual están ordenadas.
        orden (str): 'asc' o 'desc'.
    
    Returns:
        list: Lista combinada y ordenada.
    """
    resultado = []
    i = j = 0
    # Mezclar mientras ambas listas tengan elementos
    while i < len(izquierda) and j < len(derecha):
        valor_izq = obtener_valor_criterio(izquierda[i], criterio)
        valor_der = obtener_valor_criterio(derecha[j], criterio)
        # Determinar qué elemento va primero según el orden
        if orden == 'asc':
            tomar_izquierda = valor_izq <= valor_der
        else:  # 'desc'
            tomar_izquierda = valor_izq >= valor_der
        
        if tomar_izquierda:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def obtener_valor_criterio(libro, criterio):
    """
    Obtiene el valor del atributo especificado de un libro.
    
    Args:
        libro (Libro): Objeto Libro.
        criterio (str): Nombre del atributo.
    
    Returns:
        any: Valor del atributo.
    """
    if not hasattr(libro, criterio):
        raise AttributeError(f"El libro no tiene el atributo '{criterio}'")
    return getattr(libro, criterio)

def generar_reporte_global(lista_libros, criterio='valor', orden='desc', formato='txt', ruta_archivo=None):
    """
    Genera un reporte global de inventario ordenado por un criterio.
    
    Este método utiliza Merge Sort para ordenar los libros y luego
    genera un reporte que puede guardarse en archivo.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        criterio (str, optional): Atributo por el cual ordenar. Default: 'valor'.
        orden (str, optional): 'asc' o 'desc'. Default: 'desc'.
        formato (str, optional): Formato del reporte: 'txt', 'csv', 'json'.
            Default: 'txt'.
        ruta_archivo (str, optional): Ruta donde guardar el reporte.
            Si es None, se genera automáticamente en la carpeta reports/.
    
    Returns:
        str|list: Reporte generado (formato depende del tipo).
    """
    # Crear carpeta reports/ si no existe y se va a guardar archivo
    reports = 'reports'
    if not os.path.exists(reports):
        os.makedirs(reports)
        print(f"Carpeta '{reports}/' creada")
    
    # Ordenar libros usando Merge Sort
    libros_ordenados = merge_sort(lista_libros, criterio, orden)
    
    # Generar ruta por defecto si no se especificó
    if ruta_archivo is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if formato == 'txt':
            ruta_archivo = os.path.join(reports, f'reporte_{criterio}_{timestamp}.txt')
        elif formato == 'csv':
            ruta_archivo = os.path.join(reports, f'reporte_{criterio}_{timestamp}.csv')
        elif formato == 'json':
            ruta_archivo = os.path.join(reports, f'reporte_{criterio}_{timestamp}.json')
    else:
        # Si se especificó ruta pero no incluye la carpeta reports/, agregarla
        if not ruta_archivo.startswith(reports):
            ruta_archivo = os.path.join(reports, os.path.basename(ruta_archivo))

    # Generar reporte según el formato
    if formato == 'txt':
        reporte = _generar_reporte_txt(libros_ordenados, criterio, orden)
    elif formato == 'csv':
        reporte = _generar_reporte_csv(libros_ordenados, ruta_archivo)
    elif formato == 'json':
        reporte = _generar_reporte_json(libros_ordenados, ruta_archivo)
    else:
        raise ValueError(f"Formato no soportado: {formato}")
    
    # Guardar en archivo si se especificó ruta
    if ruta_archivo and formato == 'txt':
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(reporte)
        print(f"✓ Reporte guardado en: {ruta_archivo}")
    return reporte

def _generar_reporte_txt(libros_ordenados, criterio, orden):
    """
    Genera un reporte en formato de texto plano.
    
    Args:
        libros_ordenados (list): Lista de libros ya ordenada.
        criterio (str): Criterio de ordenamiento usado.
        orden (str): Orden aplicado ('asc' o 'desc').
    
    Returns:
        str: Reporte formateado como texto.
    """
    lineas = []
    lineas.append("REPORTE GLOBAL DE INVENTARIO")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lineas.append(f"Ordenado por: {criterio.upper()} ({orden.upper()})")
    lineas.append(f"Total de libros: {len(libros_ordenados)}")
    lineas.append("")

    # Calcular totales
    valor_total = sum(libro.valor * libro.cantidad_total for libro in libros_ordenados)
    peso_total = sum(libro.peso * libro.cantidad_total for libro in libros_ordenados)

    lineas.append(f"Valor total del inventario: ${valor_total:,.2f} COP")
    lineas.append(f"Peso total del inventario: {peso_total:.2f} Kg")
    lineas.append(f"{'#':<4} {'ISBN':<20} {'Título':<30} {'Autor':<25} {'Valor (COP)':<15} {'Peso (Kg)':<10} {'Stock':<8}")
    lineas.append("-" * 80)

    # Listar libros
    for i, libro in enumerate(libros_ordenados, 1):
        lineas.append(
            f"{i:<4} "
            f"{libro.isbn:<20} "
            f"{libro.titulo[:28]:<30} "
            f"{libro.autor[:23]:<25} "
            f"${libro.valor:>13,.2f} "
            f"{libro.peso:>9.2f} "
            f"{libro.cantidad_disponible}/{libro.cantidad_total}"
        )
    lineas.append("FIN DEL REPORTE")
    return "\n".join(lineas)

def _generar_reporte_csv(libros_ordenados, ruta_archivo):
    """
    Genera un reporte en formato CSV.
    
    Args:
        libros_ordenados (list): Lista de libros ya ordenada.
        ruta_archivo (str): Ruta donde guardar el archivo CSV.
    
    Returns:
        list: Lista de diccionarios con los datos.
    """
    if not ruta_archivo:
        ruta_archivo = f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(ruta_archivo, 'w', encoding='utf-8', newline='') as f:
        campos = ['posicion', 'isbn', 'titulo', 'autor', 'peso', 'valor', 'genero', 'cantidad_disponible', 'cantidad_total']
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for i, libro in enumerate(libros_ordenados, 1):
            escritor.writerow({
                'posicion': i,
                'isbn': libro.isbn,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'peso': libro.peso,
                'valor': libro.valor,
                'genero': libro.genero,
                'cantidad_disponible': libro.cantidad_disponible,
                'cantidad_total': libro.cantidad_total
            })
    print(f"Reporte CSV guardado en: {ruta_archivo}")
    return [libro.__dict__ for libro in libros_ordenados]

def _generar_reporte_json(libros_ordenados, ruta_archivo):
    """
    Genera un reporte en formato JSON.
    
    Args:
        libros_ordenados (list): Lista de libros ya ordenada.
        ruta_archivo (str): Ruta donde guardar el archivo JSON.
    
    Returns:
        list: Lista de diccionarios con los datos.
    """
    if not ruta_archivo:
        ruta_archivo = f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    datos = {
        'fecha_generacion': datetime.now().isoformat(),
        'total_libros': len(libros_ordenados),
        'libros': [
            {
                'posicion': i,
                'isbn': libro.isbn,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'peso': libro.peso,
                'valor': libro.valor,
                'genero': libro.genero,
                'cantidad_disponible': libro.cantidad_disponible,
                'cantidad_total': libro.cantidad_total
            }
            for i, libro in enumerate(libros_ordenados, 1)
        ]
    }
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"Reporte JSON guardado en: {ruta_archivo}")
    return datos