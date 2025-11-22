"""
Este paquete contiene implementaciones de algoritmos recursivos
para cálculos sobre colecciones de libros por autor:

- Recursión de Pila: Calcula el valor total de libros
  * Trabajo al REGRESAR de las llamadas recursivas
  * Acumula en la pila de llamadas del sistema
  * Ejemplo clásico de recursión no optimizable

- Recursión de Cola: Calcula el peso promedio de libros
  * Trabajo ANTES de las llamadas recursivas
  * Usa acumuladores explícitos
  * Optimizable (Tail Call Optimization)

Uso:
    from controllers.recursion import (
        calcular_valor_total_recursivo,
        calcular_peso_promedio_recursivo
    )
    
    # Recursión de pila (valor total)
    valor = calcular_valor_total_recursivo(libros, "García Márquez")
    
    # Recursión de cola (peso promedio)
    peso = calcular_peso_promedio_recursivo(libros, "García Márquez")
"""

from .valor_total import (
    calcular_valor_total,
    contar_libros_autor,
    obtener_libros_autor,
    analizar_valor_por_autor,
    demostrar_recursion_pila
)

from .peso_promedio import (
    calcular_peso_promedio,
    calcular_estadisticas_peso,
    demostrar_recursion_cola,
)

__all__ = [
    # Recursión de Pila (Valor Total)
    'calcular_valor_total',
    'contar_libros_autor',
    'obtener_libros_autor',
    'analizar_valor_por_autor',
    'demostrar_recursion_pila',
    
    # Recursión de Cola (Peso Promedio)
    'calcular_peso_promedio',
    'calcular_estadisticas_peso',
    'demostrar_recursion_cola',
]