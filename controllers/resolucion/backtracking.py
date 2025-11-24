"""
Este algoritmo encuentra la combinación de libros que maximiza 
el valor total sin exceder el peso máximo de 8 Kg.
"""

class SolucionEstanteria:
    """
    Clase para almacenar una solución de estantería.
    
    Attributes:
        libros (list): Lista de libros en la solución.
        peso_total (float): Peso total de los libros.
        valor_total (float): Valor total de los libros.
    """
    def __init__(self, libros=None, peso_total=0.0, valor_total=0.0):
        self.libros = libros if libros else []
        self.peso_total = peso_total
        self.valor_total = valor_total
    
    def agregar_libro(self, libro):
        """Agrega un libro a la solución."""
        self.libros.append(libro)
        self.peso_total += libro.peso
        self.valor_total += libro.valor

    def quitar_libro(self, libro):
        """Quita un libro de la solución por backtracking."""
        if self.libros:
            libro = self.libros.pop()
            self.peso_total -= libro.peso
            self.valor_total -= libro.valor
            return libro
        return None
    
    def copia(self):
        """Crea una copia de la solución actual."""
        return SolucionEstanteria(
            libros=self.libros.copy(),
            peso_total=self.peso_total,
            valor_total=self.valor_total
        )
    
    def __str__(self):
        return f"Solución: {len(self.libros)} libros | Peso: {self.peso_total:.2f} Kg | Valor: ${self.valor_total:,.0f}"

def optimizar_estanteria(lista_libros, peso_maximo=8.0, mostrar_exploracion=False, limite_output=50):
    """
    Encuentra la combinación óptima de libros que maximiza el valor total
    sin exceder el peso máximo usando backtracking.
    
    Explora recursivamente dos opciones para cada libro: incluirlo o no incluirlo.
    Mantiene la mejor solución encontrada y retorna al finalizar la exploración.
    
    Args:
        lista_libros (list): Lista de objetos Libro disponibles.
        peso_maximo (float, optional): Peso máximo en Kg. Default: 8.0.
        mostrar_exploracion (bool, optional): Si True, imprime la exploración.
            Default: False.
        limite_output (int, optional): Máximo de líneas de exploración a mostrar.
            Default: 50.
    
    Returns:
        SolucionEstanteria: La mejor solución encontrada.
    """
    mejor_solucion = SolucionEstanteria()
    solucion_actual = SolucionEstanteria()
    nodos_explorados = [0]  # Usar lista para mantener referencia
    lineas_impresas = [0]

    def backtrack(indice):
        """
        Función recursiva de backtracking.
        
        Explora dos ramas para cada libro:
        1. Incluir el libro si cabe en el peso máximo
        2. No incluir el libro (siempre se explora)
        
        Args:
            indice (int): Índice del libro actual a considerar.
        """
        nonlocal mejor_solucion
        nodos_explorados[0] += 1
        
        # Caso base: hemos considerado todos los libros
        if indice == len(lista_libros):
            if solucion_actual.valor_total > mejor_solucion.valor_total:
                mejor_solucion = solucion_actual.copia()
                if mostrar_exploracion and lineas_impresas[0] < limite_output:
                    print(f"  → Mejor: {len(mejor_solucion.libros)} libros, ${mejor_solucion.valor_total:,.0f}")
                    lineas_impresas[0] += 1
            return
        
        libro_actual = lista_libros[indice]
        
        # Opción 1: Incluir el libro si cabe en el peso máximo
        if solucion_actual.peso_total + libro_actual.peso <= peso_maximo:
            solucion_actual.agregar_libro(libro_actual)
            backtrack(indice + 1)
            solucion_actual.quitar_libro(libro_actual)
        
        # Opción 2: No incluir el libro actual (siempre se explora)
        backtrack(indice + 1)
    
    # Iniciar backtracking
    print(f"\nBuscando combinación óptima con backtracking...")
    backtrack(0)
    print(f"Exploración completada: {nodos_explorados[0]} nodos explorados")
    print(f"Solución óptima encontrada: {len(mejor_solucion.libros)} libros")
    return mejor_solucion

def demostrar_backtracking(lista_libros, peso_maximo=8.0):
    """
    Demuestra paso a paso el proceso de backtracking para optimización de estantería.
    
    Ejecuta el algoritmo de backtracking que explora recursivamente todas
    las combinaciones de libros para encontrar aquella que maximiza el
    valor total sin exceder el peso máximo.
    
    Args:
        lista_libros (list): Lista de objetos Libro.
        peso_maximo (float, optional): Peso máximo en Kg. Default: 8.0.
    
    Returns:
        SolucionEstanteria: La mejor solución encontrada.
    """
    print("Backtracking - Optimización de Estantería")
    print(f"\nParámetros:")
    print(f"  • Total de libros disponibles: {len(lista_libros)}")
    print(f"  • Peso máximo del estante: {peso_maximo} Kg")
    print(f"  • Objetivo: Maximizar valor total (COP)")
    print(f"  • Método: Backtracking (exploración recursiva)\n")
    
    mejor = optimizar_estanteria(lista_libros, peso_maximo, mostrar_exploracion=True)
    
    print(f"\nSOLUCIÓN ÓPTIMA ENCONTRADA:")
    print(f"  • Número de libros: {len(mejor.libros)}")
    print(f"  • Peso total: {mejor.peso_total:.2f} Kg / {peso_maximo} Kg")
    print(f"  • Valor total: ${mejor.valor_total:,.0f} COP")
    print(f"  • Espacio disponible: {peso_maximo - mejor.peso_total:.2f} Kg")
    
    if mejor.libros:
        print(f"\nLibros seleccionados:")
        for i, libro in enumerate(mejor.libros, 1):
            print(f"  {i}. {libro.titulo}")
            print(f"     ISBN: {libro.isbn} | Peso: {libro.peso} Kg | Valor: ${libro.valor:,.0f}")
    
    return mejor