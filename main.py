"""
Library Management System (LMS)

Main entry point of the system.

This system implements:
- Inventory management (general and ordered)
- Data structures (Stack and Queue)
- Sorting algorithms (Insertion Sort, Merge Sort)
- Search algorithms (Linear, Binary)
- Resolution algorithms (Brute Force, Backtracking)
- Recursion (Stack and Queue)

Use:
    python main.py [--cli|--gui]
    
    --cli: Start command line interface (default)
    --gui: Start graphical interface
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Función principal del sistema."""
    print("Sistema de Gestión de Bibliotecas")
    print()
    
    # Determinar modo de ejecución
    modo = "--cli"  # Modo por defecto
    
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
    
    if modo == "--gui":
        # Iniciar interfaz gráfica
        print("Iniciando interfaz gráfica...")
        try:
            from views.gui.interfaz import iniciar_interfaz_grafica
            iniciar_interfaz_grafica()
        except ImportError as e:
            print(f"Error al cargar la interfaz gráfica: {e}")
            print("Asegúrate de tener tkinter instalado.")
            print("Cambiando a modo CLI...")
            from views.cli.comandos import iniciar_cli
            iniciar_cli()
    else:
        # Iniciar interfaz de línea de comandos
        print("Iniciando interfaz de línea de comandos...")
        from views.cli.comandos import iniciar_cli
        iniciar_cli()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSistema terminado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)