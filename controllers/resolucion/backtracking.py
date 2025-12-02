"""
This algorithm finds the combination of books that maximizes the total 
value without exceeding the maximum weight of 8 kg.
"""

class SolucionEstanteria:
    """
    Class to store a shelving solution.
    
    Attributes:
        libros (list): List of books in the solution.
        peso_total (float): Total weight of the books.
        valor_total (float): Total value of the books.
    """
    def __init__(self, libros=None, peso_total=0.0, valor_total=0.0):
        self.libros = libros if libros else []
        self.peso_total = peso_total
        self.valor_total = valor_total
    
    def agregar_libro(self, libro):
        """Adds a book to the solution."""
        self.libros.append(libro)
        self.peso_total += libro.peso
        self.valor_total += libro.valor

    def quitar_libro(self, libro):
        """Removes a book from the solution using backtracking."""
        if self.libros:
            libro = self.libros.pop()
            self.peso_total -= libro.peso
            self.valor_total -= libro.valor
            return libro
        return None
    
    def copia(self):
        """Creates a copy of the current solution."""
        return SolucionEstanteria(
            libros=self.libros.copy(),
            peso_total=self.peso_total,
            valor_total=self.valor_total
        )
    
    def __str__(self):
        return f"Solución: {len(self.libros)} libros | Peso: {self.peso_total:.2f} Kg | Valor: ${self.valor_total:,.0f}"

def optimizar_estanteria(lista_libros, peso_maximo=8.0, mostrar_exploracion=False, limite_output=50):
    """
    Finds the optimal combination of books that maximizes the total value
    without exceeding the maximum weight using backtracking.
    
    Recursively explores two options for each book: include it or not include it.
    Maintains the best solution found and returns it after exploration.
    Args:
        lista_libros (list): List of available Book objects.
        peso_maximo (float, optional): Maximum weight in Kg. Default: 8.0.
        mostrar_exploracion (bool, optional): If True, prints the exploration.
            Default: False.
        limite_output (int, optional): Maximum number of exploration lines to show.
            Default: 50.
    
    Returns:
        SolucionEstanteria: The best solution found.
    """
    mejor_solucion = SolucionEstanteria()
    solucion_actual = SolucionEstanteria()
    nodos_explorados = [0]  # Usar lista para mantener referencia
    lineas_impresas = [0]

    def backtrack(indice):
        """
        Recursive backtracking function.
        
        Explores two branches for each book:
        1. Include the book if it fits within the maximum weight
        2. Do not include the book (always explored)
        
        Args:
            indice (int): Index of the current book to consider.
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
    Demonstrates step-by-step the backtracking process for shelf optimization.
    
    Executes the backtracking algorithm that recursively explores all
    combinations of books to find the one that maximizes the
    total value without exceeding the maximum weight.
    
    Args:
        lista_libros (list): List of Book objects.
        peso_maximo (float, optional): Maximum weight in Kg. Default: 8.0.
    
    Returns:
        SolucionEstanteria: The best solution found.
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