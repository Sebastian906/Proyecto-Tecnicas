"""
Interface built with tkinter for all system functionalities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from controllers.gestor_biblioteca import GestorBiblioteca
from controllers.adquisicion.lector_archivo import LectorArchivo
from models import Libro, Usuario, Estante


class BibliotecaGUI:
    """Main class for the graphical interface."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Bibliotecas")
        self.root.geometry("1000x700")
        
        # Gestor
        self.gestor = GestorBiblioteca()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Create the main structure of the interface."""
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.crear_interfaz_libros()
        self.crear_interfaz_usuarios()
        self.crear_interfaz_prestamos()
        self.crear_interfaz_reservas()
        self.crear_interfaz_estantes()
        self.crear_interfaz_reportes()
    
    #  Interfaz Libros
    
    def crear_interfaz_libros(self):
        """Create the book management tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Libros")
        
        # Frame superior: Botones
        frame_btns = ttk.Frame(tab)
        frame_btns.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(frame_btns, text="Cargar desde archivo", 
                    command=self.cargar_libros).pack(side='left', padx=2)
        ttk.Button(frame_btns, text="Agregar libro", 
                    command=self.agregar_libro).pack(side='left', padx=2)
        ttk.Button(frame_btns, text="Buscar ISBN", 
                    command=self.buscar_libro_isbn).pack(side='left', padx=2)
        ttk.Button(frame_btns, text="Actualizar lista", 
                    command=self.actualizar_lista_libros).pack(side='left', padx=2)
        
        # Frame de búsqueda
        frame_busqueda = ttk.LabelFrame(tab, text="Búsqueda")
        frame_busqueda.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_busqueda, text="Título:").pack(side='left', padx=2)
        self.entry_buscar_titulo = ttk.Entry(frame_busqueda, width=20)
        self.entry_buscar_titulo.pack(side='left', padx=2)
        ttk.Button(frame_busqueda, text="Buscar", 
                    command=self.buscar_por_titulo).pack(side='left', padx=2)
        
        ttk.Label(frame_busqueda, text="Autor:").pack(side='left', padx=2)
        self.entry_buscar_autor = ttk.Entry(frame_busqueda, width=20)
        self.entry_buscar_autor.pack(side='left', padx=2)
        ttk.Button(frame_busqueda, text="Buscar", 
                    command=self.buscar_por_autor).pack(side='left', padx=2)
        
        # Treeview
        frame_tree = ttk.Frame(tab)
        frame_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        cols = ('ISBN', 'Título', 'Autor', 'Peso', 'Valor', 'Disponibles')
        self.tree_libros = ttk.Treeview(frame_tree, columns=cols, show='headings', height=20)
        
        for col in cols:
            self.tree_libros.heading(col, text=col)
            self.tree_libros.column(col, width=120)
        
        scroll = ttk.Scrollbar(frame_tree, orient='vertical', command=self.tree_libros.yview)
        self.tree_libros.configure(yscrollcommand=scroll.set)
        
        self.tree_libros.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
    
    def cargar_libros(self):
        """Load books from file."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos JSON", "*.json")]
        )
        
        if ruta:
            try:
                libros = LectorArchivo.cargar_libros(ruta)
                agregados = sum(1 for libro in libros if self.gestor.agregar_libro(libro))
                messagebox.showinfo("Éxito", f"Se agregaron {agregados}/{len(libros)} libros")
                self.actualizar_lista_libros()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def agregar_libro(self):
        """Window to add a book."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Libro")
        ventana.geometry("400x350")
        
        campos = [
            ("ISBN:", "isbn"),
            ("Título:", "titulo"),
            ("Autor:", "autor"),
            ("Peso (Kg):", "peso"),
            ("Valor (COP):", "valor"),
            ("Género:", "genero"),
            ("Cantidad:", "cantidad")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(ventana, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(ventana, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                libro = Libro(
                    isbn=entries['isbn'].get(),
                    titulo=entries['titulo'].get(),
                    autor=entries['autor'].get(),
                    peso=float(entries['peso'].get()),
                    valor=float(entries['valor'].get()),
                    genero=entries['genero'].get(),
                    cantidad_disponible=int(entries['cantidad'].get() or 1),
                    cantidad_total=int(entries['cantidad'].get() or 1)
                )
                
                if self.gestor.agregar_libro(libro):
                    messagebox.showinfo("Éxito", "Libro agregado")
                    ventana.destroy()
                    self.actualizar_lista_libros()
                else:
                    messagebox.showerror("Error", "El libro ya existe")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=len(campos), column=0, columnspan=2, pady=10)
    
    def buscar_libro_isbn(self):
        """Search for a book by ISBN."""
        isbn = tk.simpledialog.askstring("Buscar", "Ingrese el ISBN:")
        if isbn:
            libro = self.gestor.buscar_libro_por_isbn(isbn)
            if libro:
                msg = f"Título: {libro.titulo}\nAutor: {libro.autor}\n"
                msg += f"Peso: {libro.peso} Kg\nValor: ${libro.valor:,.0f}\n"
                msg += f"Disponibles: {libro.cantidad_disponible}/{libro.cantidad_total}"
                messagebox.showinfo("Libro Encontrado", msg)
            else:
                messagebox.showwarning("No encontrado", "Libro no encontrado")
    
    def buscar_por_titulo(self):
        """Search for books by title."""
        titulo = self.entry_buscar_titulo.get()
        if titulo:
            libros = self.gestor.buscar_libros_por_titulo(titulo)
            self.mostrar_libros_en_tree(libros)
    
    def buscar_por_autor(self):
        """Search for books by author."""
        autor = self.entry_buscar_autor.get()
        if autor:
            libros = self.gestor.buscar_libros_por_autor(autor)
            self.mostrar_libros_en_tree(libros)
    
    def actualizar_lista_libros(self):
        """Update the list of books."""
        libros = self.gestor.obtener_todos_los_libros()
        self.mostrar_libros_en_tree(libros)
    
    def mostrar_libros_en_tree(self, libros):
        """Show books in the treeview."""
        # Limpiar
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        
        # Agregar
        for libro in libros:
            self.tree_libros.insert('', 'end', values=(
                libro.isbn,
                libro.titulo[:30],
                libro.autor[:25],
                f"{libro.peso:.2f}",
                f"${libro.valor:,.0f}",
                f"{libro.cantidad_disponible}/{libro.cantidad_total}"
            ))
    
    #  Interfaz Usuarios
    
    def crear_interfaz_usuarios(self):
        """Create the user tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Usuarios")
        
        # Botones
        frame_btns = ttk.Frame(tab)
        frame_btns.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(frame_btns, text="Agregar usuario", 
                    command=self.agregar_usuario).pack(side='left', padx=2)
        ttk.Button(frame_btns, text="Ver historial", 
                    command=self.ver_historial).pack(side='left', padx=2)
        ttk.Button(frame_btns, text="Actualizar lista", 
                    command=self.actualizar_lista_usuarios).pack(side='left', padx=2)
        
        # Treeview
        frame_tree = ttk.Frame(tab)
        frame_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        cols = ('ID', 'Nombre', 'Apellidos', 'Dirección')
        self.tree_usuarios = ttk.Treeview(frame_tree, columns=cols, show='headings', height=25)
        
        for col in cols:
            self.tree_usuarios.heading(col, text=col)
        
        scroll = ttk.Scrollbar(frame_tree, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scroll.set)
        
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
    
    def agregar_usuario(self):
        """Add user window."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Usuario")
        ventana.geometry("400x200")
        
        ttk.Label(ventana, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        entry_id = ttk.Entry(ventana)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Apellidos:").grid(row=2, column=0, padx=10, pady=5)
        entry_apellidos = ttk.Entry(ventana)
        entry_apellidos.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Dirección:").grid(row=3, column=0, padx=10, pady=5)
        entry_direccion = ttk.Entry(ventana)
        entry_direccion.grid(row=3, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                usuario = Usuario(
                    id=entry_id.get(),
                    nombre=entry_nombre.get(),
                    apellidos=entry_apellidos.get(),
                    direccion=entry_direccion.get()
                )
                
                if self.gestor.agregar_usuario(usuario):
                    messagebox.showinfo("Éxito", "Usuario agregado")
                    ventana.destroy()
                    self.actualizar_lista_usuarios()
                else:
                    messagebox.showerror("Error", "El usuario ya existe")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=10)
    
    def ver_historial(self):
        """Displays a user's history."""
        user_id = tk.simpledialog.askstring("Historial", "ID del usuario:")
        if user_id:
            usuario = self.gestor.buscar_usuario(user_id)
            if usuario and usuario.historial_prestamos:
                prestamos = usuario.historial_prestamos.obtener_todos()
                if prestamos:
                    msg = f"Historial de {usuario.nombre} {usuario.apellidos}:\n\n"
                    for p in prestamos:
                        msg += f"• {p.id}: Libro {p.libro_isbn} - {p.estado}\n"
                    messagebox.showinfo("Historial", msg)
                else:
                    messagebox.showinfo("Historial", "Sin préstamos")
            else:
                messagebox.showwarning("Error", "Usuario no encontrado")
    
    def actualizar_lista_usuarios(self):
        """Update the list of users."""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        for usuario in self.gestor.listar_usuarios():
            self.tree_usuarios.insert('', 'end', values=(
                usuario.id,
                usuario.nombre,
                usuario.apellidos,
                usuario.direccion
            ))
    
    #  Interfaz Préstamos
    
    def crear_interfaz_prestamos(self):
        """Create the loans tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Préstamos")
        
        # Frame de préstamo
        frame_prest = ttk.LabelFrame(tab, text="Realizar Préstamo")
        frame_prest.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_prest, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_prest_usuario = ttk.Entry(frame_prest)
        self.entry_prest_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_prest, text="ISBN Libro:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_prest_isbn = ttk.Entry(frame_prest)
        self.entry_prest_isbn.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame_prest, text="Prestar", 
                    command=self.realizar_prestamo).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Frame de devolución
        frame_dev = ttk.LabelFrame(tab, text="Devolver Libro")
        frame_dev.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_dev, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_dev_usuario = ttk.Entry(frame_dev)
        self.entry_dev_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_dev, text="ISBN Libro:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_dev_isbn = ttk.Entry(frame_dev)
        self.entry_dev_isbn.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame_dev, text="Devolver", 
                    command=self.devolver_libro).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Lista de activos
        ttk.Button(tab, text="Ver Préstamos Activos", 
                    command=self.ver_prestamos_activos).pack(pady=10)
    
    def realizar_prestamo(self):
        """Make a loan."""
        exito, msg = self.gestor.realizar_prestamo(
            self.entry_prest_usuario.get(),
            self.entry_prest_isbn.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.entry_prest_usuario.delete(0, 'end')
            self.entry_prest_isbn.delete(0, 'end')
        else:
            messagebox.showerror("Error", msg)
    
    def devolver_libro(self):
        """Return a book."""
        exito, msg = self.gestor.devolver_libro(
            self.entry_dev_usuario.get(),
            self.entry_dev_isbn.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.entry_dev_usuario.delete(0, 'end')
            self.entry_dev_isbn.delete(0, 'end')
        else:
            messagebox.showerror("Error", msg)
    
    def ver_prestamos_activos(self):
        """Show active loans."""
        msg = "PRÉSTAMOS ACTIVOS:\n\n"
        total = 0
        
        for u in self.gestor.listar_usuarios():
            if u.historial_prestamos:
                activos = u.historial_prestamos.obtener_activos()
                if activos:
                    msg += f"{u.nombre} {u.apellidos}:\n"
                    for p in activos:
                        msg += f"  • Libro {p.libro_isbn}\n"
                    total += len(activos)
        
        msg += f"\nTotal: {total}"
        messagebox.showinfo("Préstamos Activos", msg)
    
    #  Interfaz Reservas
    
    def crear_interfaz_reservas(self):
        """Create the bookings tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reservas")
        
        frame = ttk.LabelFrame(tab, text="Gestión de Reservas")
        frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_res_usuario = ttk.Entry(frame)
        self.entry_res_usuario.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="ISBN Libro:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_res_isbn = ttk.Entry(frame)
        self.entry_res_isbn.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Crear Reserva", 
                    command=self.crear_reserva).grid(row=2, column=0, pady=5)
        ttk.Button(frame, text="Cancelar Reserva", 
                    command=self.cancelar_reserva).grid(row=2, column=1, pady=5)
        
        ttk.Button(tab, text="Ver Todas las Reservas", 
                    command=self.ver_todas_reservas).pack(pady=10)
    
    def crear_reserva(self):
        """Create a booking."""
        exito, msg = self.gestor.crear_reserva(
            self.entry_res_usuario.get(),
            self.entry_res_isbn.get()
        )
        messagebox.showinfo("Resultado", msg) if exito else messagebox.showerror("Error", msg)
    
    def cancelar_reserva(self):
        """Cancel a booking."""
        exito, msg = self.gestor.cancelar_reserva(
            self.entry_res_usuario.get(),
            self.entry_res_isbn.get()
        )
        messagebox.showinfo("Resultado", msg) if exito else messagebox.showerror("Error", msg)
    
    def ver_todas_reservas(self):
        """Show all bookings."""
        msg = "RESERVAS:\n\n"
        total = 0
        
        for isbn, cola in self.gestor.colas_reservas.items():
            reservas = cola.obtener_todas()
            if reservas:
                msg += f"Libro {isbn}: {len(reservas)} reservas\n"
                total += len(reservas)
        
        msg += f"\nTotal: {total}"
        messagebox.showinfo("Reservas", msg)
    
    #  Interfaz Estantes
    
    def crear_interfaz_estantes(self):
        """Create the shelves tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Estantes")
        
        ttk.Button(tab, text="Agregar Estante", 
                    command=self.agregar_estante).pack(pady=5)
        ttk.Button(tab, text="Asignar Libro", 
                    command=self.asignar_libro).pack(pady=5)
        ttk.Button(tab, text="Listar Estantes", 
                    command=self.listar_estantes).pack(pady=5)
        ttk.Button(tab, text="Análisis Peligroso (Fuerza Bruta)", 
                    command=self.analisis_peligroso).pack(pady=5)
        ttk.Button(tab, text="Optimización (Backtracking)", 
                    command=self.optimizacion_estanteria).pack(pady=5)
    
    def agregar_estante(self):
        """Add a shelf."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Estante")
        
        ttk.Label(ventana, text="ID:").grid(row=0, column=0)
        entry_id = ttk.Entry(ventana)
        entry_id.grid(row=0, column=1)
        
        ttk.Label(ventana, text="Espacios:").grid(row=1, column=0)
        entry_esp = ttk.Entry(ventana)
        entry_esp.grid(row=1, column=1)
        
        def guardar():
            try:
                estante = Estante(entry_id.get(), int(entry_esp.get()))
                if self.gestor.agregar_estante(estante):
                    messagebox.showinfo("Éxito", "Estante agregado")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "Ya existe")
            except:
                messagebox.showerror("Error", "Datos inválidos")
        
        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=2, columnspan=2)
    
    def asignar_libro(self):
        """Assign a book to a shelf."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Asignar Libro a Estante")
        
        ttk.Label(ventana, text="ISBN:").grid(row=0, column=0)
        entry_isbn = ttk.Entry(ventana)
        entry_isbn.grid(row=0, column=1)
        
        ttk.Label(ventana, text="ID Estante:").grid(row=1, column=0)
        entry_estante = ttk.Entry(ventana)
        entry_estante.grid(row=1, column=1)
        
        def guardar():
            try:
                exito, msg = self.gestor.asignar_libro_a_estante(
                    entry_isbn.get(), 
                    entry_estante.get()
                )
                if exito:
                    messagebox.showinfo("Éxito", msg)
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
        
        ttk.Button(ventana, text="Asignar", command=guardar).grid(row=2, columnspan=2)
    
    def listar_estantes(self):
        """List all shelves."""
        msg = "ESTANTES:\n\n"
        for e in self.gestor.listar_estantes():
            msg += f"Estante {e.id}:\n"
            msg += f"  Libros: {len(e.libros_asignados)}/{e.cantidad}\n"
            msg += f"  Peso: {e.peso_actual:.2f}/{e.peso_maximo:.2f} Kg\n\n"
        messagebox.showinfo("Estantes", msg)
    
    def analisis_peligroso(self):
        """Brute force analysis."""
        libros = self.gestor.obtener_todos_los_libros()
        
        if len(libros) < 4:
            messagebox.showwarning("Advertencia", "Se necesitan al menos 4 libros para el análisis")
            return
        
        from controllers.resolucion.fuerza_bruta import encontrar_combinaciones
        
        combinaciones_peligrosas = encontrar_combinaciones(libros, num_libros=4, peso_maximo=8.0)
        
        if not combinaciones_peligrosas:
            messagebox.showinfo("Resultado", "No se encontraron combinaciones peligrosas (peso > 8 Kg)")
            return
        
        # Mostrar resultados en ventana emergente
        msg = "ANÁLISIS DE FUERZA BRUTA - COMBINACIONES PELIGROSAS\n"
        msg += f"Total de combinaciones peligrosas encontradas: {len(combinaciones_peligrosas)}\n\n"
        msg += "Mostrando primeras 10 combinaciones:\n"
        
        for i, (libros_combo, peso_total, exceso) in enumerate(combinaciones_peligrosas[:10], 1):
            msg += f"\n[{i}] Peso: {peso_total:.2f} Kg (Excede por {exceso:.2f} Kg)\n"
            for j, libro in enumerate(libros_combo, 1):
                msg += f"    {j}. {libro.titulo[:40]}\n"
                msg += f"       Peso: {libro.peso} Kg | Valor: ${libro.valor:,.0f}\n"
        
        if len(combinaciones_peligrosas) > 10:
            msg += f"\n... y {len(combinaciones_peligrosas) - 10} combinaciones más"
        
        messagebox.showinfo("Fuerza Bruta", msg)
    
    def optimizacion_estanteria(self):
        """Optimization with backtracking."""
        libros = self.gestor.obtener_todos_los_libros()
        
        if not libros:
            messagebox.showwarning("Advertencia", "No hay libros disponibles")
            return
        
        from controllers.resolucion.backtracking import optimizar_estanteria
        
        mejor = optimizar_estanteria(libros, peso_maximo=8.0, mostrar_exploracion=False)
        
        if not mejor.libros:
            messagebox.showinfo("Resultado", "No se encontró una combinación válida")
            return
        
        # Mostrar resultados en ventana emergente
        msg = "BACKTRACKING - SOLUCIÓN ÓPTIMA DE ESTANTERÍA\n"
        msg += f"Número de libros: {len(mejor.libros)}\n"
        msg += f"Peso total: {mejor.peso_total:.2f} Kg / 8.0 Kg\n"
        msg += f"Valor total: ${mejor.valor_total:,.0f} COP\n"
        msg += f"Espacio disponible: {8.0 - mejor.peso_total:.2f} Kg\n"
        msg += "\nLibros seleccionados:\n"
        
        for i, libro in enumerate(mejor.libros, 1):
            msg += f"\n{i}. {libro.titulo}\n"
            msg += f"   ISBN: {libro.isbn}\n"
            msg += f"   Peso: {libro.peso} Kg | Valor: ${libro.valor:,.0f}\n"
        
        messagebox.showinfo("Backtracking", msg)
    
    #  Interfaz Reportes
    
    def crear_interfaz_reportes(self):
        """Create the reports tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reportes")
        
        ttk.Button(tab, text="Estadísticas Generales", 
                    command=self.mostrar_estadisticas).pack(pady=10)
        ttk.Button(tab, text="Generar Reporte Inventario", 
                    command=self.generar_reporte).pack(pady=10)
        ttk.Button(tab, text="Valor por Autor (Recursión Pila)", 
                    command=self.valor_por_autor).pack(pady=10)
        ttk.Button(tab, text="Peso por Autor (Recursión Cola)", 
                    command=self.peso_por_autor).pack(pady=10)
        ttk.Button(tab, text="Menor Valor de Libros",
                    command=self.valor_menor).pack(pady=10)
    
    def mostrar_estadisticas(self):
        """Shows general statistics."""
        stats = self.gestor.obtener_estadisticas()
        msg = f"ESTADÍSTICAS:\n\n"
        msg += f"Libros: {stats['total_libros']}\n"
        msg += f"Usuarios: {stats['total_usuarios']}\n"
        msg += f"Préstamos activos: {stats['prestamos_activos']}\n"
        msg += f"Reservas: {stats['total_reservas']}\n"
        msg += f"Estantes: {stats['total_estantes']}"
        messagebox.showinfo("Estadísticas", msg)
    
    def generar_reporte(self):
        """Generate inventory report."""
        from controllers.ordenamiento.merge_sort import generar_reporte_global
        libros = self.gestor.obtener_todos_los_libros()
        
        if libros:
            generar_reporte_global(libros, criterio='valor', orden='desc',
                                    formato='txt', ruta_archivo='reporte_gui.txt')
            messagebox.showinfo("Éxito", "Reporte en reports/reporte_gui.txt")
        else:
            messagebox.showwarning("Advertencia", "Sin libros")
    
    def valor_por_autor(self):
        """Calculate total value of books by author using stack recursion."""
        libros = self.gestor.obtener_todos_los_libros()
        
        if not libros:
            messagebox.showwarning("Advertencia", "No hay libros disponibles")
            return
        
        # Pedir el nombre del autor
        from tkinter import simpledialog
        autor = simpledialog.askstring("Valor por Autor", "Ingrese el nombre del autor:")
        
        if not autor:
            return
        
        from controllers.recursion.valor_total import analizar_valor_por_autor
        
        analisis = analizar_valor_por_autor(libros, autor)
        
        if analisis['cantidad_libros'] == 0:
            messagebox.showinfo("Resultado", f"No se encontraron libros del autor: {autor}")
            return
        
        # Mostrar resultados en ventana emergente
        msg = f"ANÁLISIS DE VALOR - RECURSIÓN DE PILA\n"
        msg += f"Autor: {analisis['autor']}\n\n"
        msg += f"Cantidad de libros: {analisis['cantidad_libros']}\n"
        msg += f"Valor total: ${analisis['valor_total']:,.0f} COP\n"
        msg += f"Valor promedio: ${analisis['valor_promedio']:,.0f} COP\n\n"
        msg += f"Libros de {autor}:\n"
        
        for i, libro in enumerate(analisis['libros'], 1):
            msg += f"\n{i}. {libro.titulo}\n"
            msg += f"   ISBN: {libro.isbn}\n"
            msg += f"   Valor: ${libro.valor:,.0f} COP\n"
        
        msg += f"\n\nEXPLICACIÓN (Recursión de Pila):\n"
        msg += f"• El cálculo se realiza AL REGRESAR de las llamadas recursivas\n"
        msg += f"• Los resultados se acumulan en la pila de llamadas del sistema\n"
        msg += f"• No es tail-recursive (no optimizable por el compilador)"
        
        messagebox.showinfo("Valor por Autor", msg)
    
    def peso_por_autor(self):
        """Calculate average book weight per author using tail recursion."""
        libros = self.gestor.obtener_todos_los_libros()
        
        if not libros:
            messagebox.showwarning("Advertencia", "No hay libros disponibles")
            return
        
        # Pedir el nombre del autor
        from tkinter import simpledialog
        autor = simpledialog.askstring("Peso por Autor", "Ingrese el nombre del autor:")
        
        if not autor:
            return
        
        from controllers.recursion.peso_promedio import calcular_estadisticas_peso
        
        stats = calcular_estadisticas_peso(libros, autor)
        
        if stats['cantidad_libros'] == 0:
            messagebox.showinfo("Resultado", f"No se encontraron libros del autor: {autor}")
            return
        
        # Mostrar resultados en ventana emergente
        msg = f"ANÁLISIS DE PESO - RECURSIÓN DE COLA\n"
        msg += f"Autor: {stats['autor']}\n\n"
        msg += f"Cantidad de libros: {stats['cantidad_libros']}\n"
        msg += f"Peso total: {stats['peso_total']:.2f} Kg\n"
        msg += f"Peso promedio: {stats['peso_promedio']:.2f} Kg\n"
        msg += f"Peso mínimo: {stats['peso_minimo']:.2f} Kg\n"
        msg += f"Peso máximo: {stats['peso_maximo']:.2f} Kg\n"
        msg += f"\nEXPLICACIÓN (Recursión de Cola):\n"
        msg += f"• El cálculo se realiza ANTES de la llamada recursiva\n"
        msg += f"• Utiliza acumuladores para mantener el estado\n"
        msg += f"• La llamada recursiva es lo ÚLTIMO que se ejecuta\n"
        msg += f"• Puede ser optimizada (Tail Call Optimization)\n"
        msg += f"• No acumula innecesariamente en la pila de llamadas"
        
        messagebox.showinfo("Peso por Autor", msg)

    def valor_menor(self):
        libros = self.gestor.obtener_todos_los_libros()
        
        if not libros:
            messagebox.showwarning("Advertencia", "No hay libros disponibles")
            return
        
        from controllers.recursion.valor_total import calcular_valor_menor
        
        try:
            analisis = calcular_valor_menor(libros)

            # Verificar que la respuesta no sea None
            if analisis is None:
                messagebox.showerror("Error", "Error al procesar los libros")
                return
            
            libro = analisis['libro']
            valor_menor = analisis['valor_menor']
            
            # Mostrar resultados en ventana emergente
            msg = f"Valor Menor de Libro - RECURSIÓN DE PILA\n"
            msg += f"Total de libros analizados: {len(libros)}\n"
            msg += f"Valor menor encontrado: ${valor_menor:,.0f} COP\n\n"
            msg += f"Libro con menor valor:\n"

            libro = analisis['libro']
            msg += f"   Título: {libro.titulo}\n"
            msg += f"   ISBN: {libro.isbn}\n"
            msg += f"   Autor: {libro.autor}\n"
            msg += f"   Valor: ${libro.valor:,.0f} COP\n"
            messagebox.showinfo("Valor Menor", msg)
        except KeyError as e:
            messagebox.showerror("Error de Clave", f"Clave no encontrada: {e}\nVerifica la estructura del diccionario")
        except AttributeError as e:
            messagebox.showerror("Error de Atributo", f"El libro no tiene el atributo: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")

def iniciar_interfaz_grafica():
    """Start the graphical interface."""
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz_grafica()