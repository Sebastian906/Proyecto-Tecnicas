"""
This module provides a menu-based console interface
for interacting with all system functionalities.
"""

from controllers.gestor_biblioteca import GestorBiblioteca
from controllers.adquisicion.lector_archivo import LectorArchivo
from models import Libro, Usuario, Estante
from controllers.ordenamiento.merge_sort import generar_reporte_global
from controllers.resolucion.fuerza_bruta import demostrar_exploracion_fuerza_bruta
from controllers.resolucion.backtracking import demostrar_backtracking
from controllers.recursion.valor_total import demostrar_recursion_pila
from controllers.recursion.peso_promedio import demostrar_recursion_cola
import os

# Instancia global del gestor
gestor = GestorBiblioteca()

def limpiar():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pauses until Enter is pressed."""
    input("\nPress Enter to continue...")

def menu_principal():
    """Displays the main menu."""
    while True:
        limpiar()
        print("    SISTEMA DE GESTIÓN DE BIBLIOTECAS")
        print("\n[1] Gestión de Libros")
        print("[2] Gestión de Usuarios")
        print("[3] Préstamos y Devoluciones")
        print("[4] Reservas")
        print("[5] Estantes")
        print("[6] Reportes")
        print("[7] Algoritmos (Demo)")
        print("[0] Salir")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": menu_libros()
        elif op == "2": menu_usuarios()
        elif op == "3": menu_prestamos()
        elif op == "4": menu_reservas()
        elif op == "5": menu_estantes()
        elif op == "6": menu_reportes()
        elif op == "7": menu_algoritmos()
        elif op == "0": 
            print("\n¡Hasta luego!")
            break

# Libros

def menu_libros():
    """Books management menu."""
    while True:
        limpiar()
        print("\n GESTIÓN DE LIBROS ")
        print("[1] Cargar desde archivo")
        print("[2] Agregar libro")
        print("[3] Buscar por ISBN")
        print("[4] Buscar por título")
        print("[5] Buscar por autor")
        print("[6] Listar todos")
        print("[7] Eliminar libro")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": cargar_libros()
        elif op == "2": agregar_libro()
        elif op == "3": buscar_isbn()
        elif op == "4": buscar_titulo()
        elif op == "5": buscar_autor()
        elif op == "6": listar_libros()
        elif op == "7": eliminar_libro()
        elif op == "0": break

def cargar_libros():
    """Load books from file."""
    print("\n CARGAR LIBROS ")
    ruta = input("Ruta del archivo: ").strip() or "data/libros.csv"
    
    try:
        libros = LectorArchivo.cargar_libros(ruta)
        agregados = sum(1 for libro in libros if gestor.agregar_libro(libro))
        print(f"\n {agregados}/{len(libros)} libros agregados")
    except Exception as e:
        print(f"\n Error: {e}")
    pausar()

def agregar_libro():
    """Add a book manually."""
    print("\n AGREGAR LIBRO ")
    try:
        libro = Libro(
            isbn=input("ISBN: "),
            titulo=input("Título: "),
            autor=input("Autor: "),
            peso=float(input("Peso (Kg): ")),
            valor=float(input("Valor (COP): ")),
            genero=input("Género: "),
            cantidad_disponible=int(input("Cantidad: ") or 1),
            cantidad_total=int(input("Total: ") or 1)
        )
        print("\n Agregado" if gestor.agregar_libro(libro) else "\n Ya existe")
    except Exception as e:
        print(f"\n Error: {e}")
    pausar()

def buscar_isbn():
    """Search for a book by ISBN."""
    print("\n BUSCAR POR ISBN ")
    libro = gestor.buscar_libro_por_isbn(input("ISBN: "))
    
    if libro:
        print(f"\n {libro.titulo} - {libro.autor}")
        print(f"  Peso: {libro.peso} Kg | Valor: ${libro.valor:,.0f}")
        print(f"  Disponibles: {libro.cantidad_disponible}/{libro.cantidad_total}")
    else:
        print("\n No encontrado")
    pausar()

def buscar_titulo():
    """Search for books by title."""
    print("\n BUSCAR POR TÍTULO ")
    libros = gestor.buscar_libros_por_titulo(input("Título: "))
    
    if libros:
        print(f"\n {len(libros)} libro(s):")
        for l in libros: print(f"  • {l.titulo} - {l.autor}")
    else:
        print("\n No encontrados")
    pausar()

def buscar_autor():
    """Search for books by author."""
    print("\n BUSCAR POR AUTOR ")
    libros = gestor.buscar_libros_por_autor(input("Autor: "))
    
    if libros:
        print(f"\n {len(libros)} libro(s):")
        for l in libros: print(f"  • {l.titulo}")
    else:
        print("\n No encontrados")
    pausar()

def listar_libros():
    """List all books."""
    print("\n TODOS LOS LIBROS ")
    libros = gestor.obtener_todos_los_libros()
    
    if libros:
        print(f"\nTotal: {len(libros)} libros\n")
        for i, l in enumerate(libros[:20], 1):  # Mostrar solo primeros 20
            print(f"{i}. {l.titulo} - {l.autor} | ${l.valor:,.0f}")
        if len(libros) > 20:
            print(f"\n... y {len(libros)-20} más")
    else:
        print("\n Sin libros ")
    pausar()

def eliminar_libro():
    """Delete a book."""
    print("\n ELIMINAR LIBRO ")
    print("Eliminado" if gestor.eliminar_libro(input("ISBN: ")) else "No encontrado")
    pausar()

# Usuarios

def menu_usuarios():
    """Users management menu."""
    while True:
        limpiar()
        print("\n GESTIÓN DE USUARIOS ")
        print("[1] Agregar usuario")
        print("[2] Buscar usuario")
        print("[3] Listar usuarios")
        print("[4] Ver historial")
        print("[5] Eliminar usuario")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": agregar_usuario()
        elif op == "2": buscar_usuario()
        elif op == "3": listar_usuarios()
        elif op == "4": ver_historial()
        elif op == "5": eliminar_usuario()
        elif op == "0": break

def agregar_usuario():
    """Add an user."""
    print("\n AGREGAR USUARIO ")
    try:
        usuario = Usuario(
            id=input("ID: "),
            nombre=input("Nombre: "),
            apellidos=input("Apellidos: "),
            direccion=input("Dirección: ")
        )
        print("\nAgregado" if gestor.agregar_usuario(usuario) else "\nYa existe")
    except Exception as e:
        print(f"\nError: {e}")
    pausar()

def buscar_usuario():
    """Search for a user."""
    print("\n BUSCAR USUARIO ")
    usuario = gestor.buscar_usuario(input("ID: "))
    
    if usuario:
        print(f"\n {usuario.nombre} {usuario.apellidos}")
        print(f"  Dirección: {usuario.direccion}")
    else:
        print("\n No encontrado")
    pausar()

def listar_usuarios():
    """List all users."""
    print("\n TODOS LOS USUARIOS ")
    usuarios = gestor.listar_usuarios()
    
    if usuarios:
        print(f"\nTotal: {len(usuarios)}\n")
        for u in usuarios:
            print(f"  • [{u.id}] {u.nombre} {u.apellidos}")
    else:
        print("\n Sin usuarios ")
    pausar()

def ver_historial():
    """Show loan history."""
    print("\n HISTORIAL ")
    usuario = gestor.buscar_usuario(input("ID del usuario: "))
    
    if usuario and usuario.historial_prestamos:
        prestamos = usuario.historial_prestamos.obtener_todos()
        if prestamos:
            print(f"\nPréstamos de {usuario.nombre}:")
            for p in prestamos:
                print(f"  • {p.id}: Libro {p.libro_isbn} - {p.estado}")
        else:
            print("\n Sin préstamos ")
    else:
        print("\n Usuario no encontrado ")
    pausar()

def eliminar_usuario():
    """Delete a user."""
    print("\n ELIMINAR USUARIO ")
    print("Eliminado" if gestor.eliminar_usuario(input("ID: ")) else "No encontrado")
    pausar()

# Préstamos

def menu_prestamos():
    """Loans management menu."""
    while True:
        limpiar()
        print("\n PRÉSTAMOS Y DEVOLUCIONES ")
        print("[1] Realizar préstamo")
        print("[2] Devolver libro")
        print("[3] Ver préstamos activos")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": realizar_prestamo()
        elif op == "2": devolver_libro()
        elif op == "3": ver_activos()
        elif op == "0": break

def realizar_prestamo():
    """Make a loan."""
    print("\n REALIZAR PRÉSTAMO ")
    exito, msg = gestor.realizar_prestamo(
        input("ID usuario: "),
        input("ISBN libro: "),
        int(input("Días (15): ") or 15)
    )
    print(f"\n{'Si' if exito else 'No'} {msg}")
    pausar()

def devolver_libro():
    """Return a book."""
    print("\n DEVOLVER LIBRO ")
    exito, msg = gestor.devolver_libro(input("ID usuario: "), input("ISBN libro: "))
    print(f"\n{'Si' if exito else 'No'} {msg}")
    pausar()

def ver_activos():
    """Shows active loans."""
    print("\n PRÉSTAMOS ACTIVOS ")
    total = 0
    for u in gestor.listar_usuarios():
        if u.historial_prestamos:
            activos = u.historial_prestamos.obtener_activos()
            if activos:
                print(f"\n{u.nombre} {u.apellidos}:")
                for p in activos:
                    print(f"  • {p.libro_isbn}")
                total += len(activos)
    print(f"\nTotal: {total}")
    pausar()

# Reservas

def menu_reservas():
    """Reservations management menu."""
    while True:
        limpiar()
        print("\n GESTIÓN DE RESERVAS ")
        print("[1] Crear reserva")
        print("[2] Cancelar reserva")
        print("[3] Ver reservas")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": crear_reserva()
        elif op == "2": cancelar_reserva()
        elif op == "3": ver_reservas()
        elif op == "0": break

def crear_reserva():
    """Create a reservation."""
    print("\n CREAR RESERVA ")
    exito, msg = gestor.crear_reserva(input("ID usuario: "), input("ISBN libro: "))
    print(f"\n{'Si' if exito else 'No'} {msg}")
    pausar()

def cancelar_reserva():
    """Cancel a reservation."""
    print("\n CANCELAR RESERVA ")
    exito, msg = gestor.cancelar_reserva(input("ID usuario: "), input("ISBN libro: "))
    print(f"\n{'Si' if exito else 'No'} {msg}")
    pausar()

def ver_reservas():
    """Show all reservations."""
    print("\n TODAS LAS RESERVAS ")
    total = 0
    for isbn, cola in gestor.colas_reservas.items():
        reservas = cola.obtener_todas()
        if reservas:
            print(f"\nLibro {isbn}: {len(reservas)} reservas")
            total += len(reservas)
    print(f"\nTotal: {total}")
    pausar()

# Estantes

def menu_estantes():
    """Shelves management menu."""
    while True:
        limpiar()
        print("\n GESTIÓN DE ESTANTES ")
        print("[1] Agregar estante")
        print("[2] Asignar libro")
        print("[3] Listar estantes")
        print("[4] Análisis peligroso (Fuerza Bruta)")
        print("[5] Optimización (Backtracking)")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": agregar_estante()
        elif op == "2": asignar_libro()
        elif op == "3": listar_estantes()
        elif op == "4": analisis_peligroso()
        elif op == "5": optimizacion()
        elif op == "0": break

def agregar_estante():
    """Add a shelf."""
    print("\nAGREGAR ESTANTE")
    try:
        estante = Estante(input("ID: "), int(input("Espacios: ")))
        print("\nAgregado" if gestor.agregar_estante(estante) else "\nYa existe")
    except Exception as e:
        print(f"\nError: {e}")
    pausar()

def asignar_libro():
    """Assign book to shelf."""
    print("\n ASIGNAR LIBRO")
    exito, msg = gestor.asignar_libro_a_estante(
        input("ISBN: "), 
        input("ID estante: ")
    )
    print(f"\n{'Si' if exito else 'No'} {msg}")
    pausar()

def listar_estantes():
    """List all shelves."""
    print("\n ESTANTES ")
    for e in gestor.listar_estantes():
        print(f"\nEstante {e.id}: {len(e.libros_asignados)}/{e.cantidad} libros")
        print(f"  Peso: {e.peso_actual:.2f}/{e.peso_maximo:.2f} Kg")
    pausar()

def analisis_peligroso():
    """Analyze dangerous combinations."""
    libros = gestor.obtener_todos_los_libros()
    if len(libros) < 4:
        print("\nSe necesitan al menos 4 libros")
    else:
        demostrar_exploracion_fuerza_bruta(libros, mostrar_primeras=10)
    pausar()

def optimizacion():
    """Optimize shelving."""
    libros = gestor.obtener_todos_los_libros()
    if libros:
        demostrar_backtracking(libros)
    else:
        print("\nSin libros")
    pausar()

# Reportes

def menu_reportes():
    """Reports and statistics menu."""
    while True:
        limpiar()
        print("\n REPORTES Y ESTADÍSTICAS ")
        print("[1] Estadísticas generales")
        print("[2] Reporte inventario (Merge Sort)")
        print("[3] Valor por autor (Recursión Pila)")
        print("[4] Peso por autor (Recursión Cola)")
        print("[0] Volver")
        
        op = input("\nOpción: ").strip()
        
        if op == "1": estadisticas()
        elif op == "2": reporte_inventario()
        elif op == "3": valor_autor()
        elif op == "4": peso_autor()
        elif op == "0": break

def estadisticas():
    """Show statistics."""
    stats = gestor.obtener_estadisticas()
    print(f"\nLibros: {stats['total_libros']}")
    print(f"Usuarios: {stats['total_usuarios']}")
    print(f"Préstamos activos: {stats['prestamos_activos']}")
    print(f"Reservas: {stats['total_reservas']}")
    print(f"Estantes: {stats['total_estantes']}")
    pausar()

def reporte_inventario():
    """Generate report."""
    libros = gestor.obtener_todos_los_libros()
    if libros:
        generar_reporte_global(libros, criterio='valor', orden='desc', 
                                formato='txt', ruta_archivo='reporte.txt')
        print("\nReporte en reports/reporte.txt")
    else:
        print("\nSin libros")
    pausar()

def valor_autor():
    """Calculate total value by author."""
    libros = gestor.obtener_todos_los_libros()
    if libros:
        demostrar_recursion_pila(libros, input("\nAutor: "))
    else:
        print("\nSin libros")
    pausar()

def peso_autor():
    """Calculate average weight per author."""
    libros = gestor.obtener_todos_los_libros()
    if libros:
        demostrar_recursion_cola(libros, input("\nAutor: "))
    else:
        print("\nSin libros")
    pausar()

# Algoritmos

def menu_algoritmos():
    """Demonstrations menu."""
    print("\n[Todas las demostraciones están en los menús específicos]")
    print("  • Estantes > Análisis peligroso (Fuerza Bruta)")
    print("  • Estantes > Optimización (Backtracking)")
    print("  • Reportes > Valor/Peso por autor (Recursión)")
    pausar()

def iniciar_cli():
    """Start the CLI."""
    limpiar()
    print("\n¡Bienvenido al Sistema de Gestión de Bibliotecas!")
    print("\nSugerencia: Cargue libros desde el menú [1]")
    pausar()
    menu_principal()