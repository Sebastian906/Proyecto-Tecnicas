"""
This algorithm is used to generate Global Inventory Reports
ordered by the Value attribute (COP). It is efficient for large lists
and guarantees a performance of O(n log n).

Time Complexity: O(n log n) in all cases
Space Complexity: O(n) - requires additional space for merging
"""

import csv
import json
from datetime import datetime
import os

from models import libro

def merge_sort(lista_libros, criterio='valor', orden='asc'):
    """
    Sorts a list of books using the Merge Sort algorithm.

    This algorithm recursively divides the list into halves, 
    sorts them, and then merges them. Efficient for large lists.
    
    Args:
        lista_libros (list): List of Book objects to sort.
        criterio (str, optional): Attribute by which to sort.
            Options: 'isbn', 'title', 'author', 'weight', 'value'.
            Default: 'value'.
        orden (str, optional): 'asc' for ascending, 'desc' for descending.
            Default: 'asc'.
    
    Returns:
        list: New sorted list (does not modify the original).
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
    Combines two sorted lists into a single sorted list.
    
    Args:
        izquierda (list): First sorted sublist.
        derecha (list): Second sorted sublist.
        criterio (str): Attribute by which the lists are sorted.
        orden (str): 'asc' or 'desc'.
    
    Returns:
        list: Combined and sorted list.
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
    Obtains the value of the specified attribute from a book.
    
    Args:
        libro (Libro): Book object.
        criterio (str): Name of the attribute.
    
    Returns:
        any: Value of the attribute.
    """
    if not hasattr(libro, criterio):
        raise AttributeError(f"El libro no tiene el atributo '{criterio}'")
    return getattr(libro, criterio)

def generar_reporte_global(lista_libros, criterio='valor', orden='desc', formato='txt', ruta_archivo=None):
    """
    Generates a comprehensive inventory report sorted by a criterion.
    
    This method uses Merge Sort to sort the books and then
    generates a report that can be saved to a file.
    
    Args:
        lista_libros (list): List of Book objects.
        criterio (str, optional): Attribute by which to sort. Default: 'value'.
        orden (str, optional): 'asc' or 'desc'. Default: 'desc'.
        formato (str, optional): Report format: 'txt', 'csv', 'json'.
            Default: 'txt'.
        ruta_archivo (str, optional): Path to save the report.
            If None, it is automatically generated in the reports/ folder.
    
    Returns:
        str|list: Generated report (format depends on the type).
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
    Generates a plain text report.
    
    Args:
        libros_ordenados (list): Already sorted list of books.
        criterio (str): Sorting criterion used.
        orden (str): Applied order ('asc' or 'desc').
    
    Returns:
        str: Report formatted as text.
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
    Generates a report in CSV format.
    
    Args:
        libros_ordenados (list): Book list already sorted.
        ruta_archivo (str): Path to save the CSV file.
    
    Returns:
        list: List of dictionaries with the data.
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
    Generates a report in JSON format.
    
    Args:
        libros_ordenados (list): Already sorted list of books.
        ruta_archivo (str): Path to save the JSON file.
    
    Returns:
        list: List of dictionaries with the data.
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