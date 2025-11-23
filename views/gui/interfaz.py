"""
Interfaz construida con tkinter para todas las funcionalidades del sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from controllers.gestor_biblioteca import GestorBiblioteca
from controllers.adquisicion.lector_archivo import LectorArchivo
from models import Libro, Usuario, Estante


class BibliotecaGUI:
    """Clase principal de la interfaz gráfica."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Bibliotecas")
        self.root.geometry("1000x700")
        
        # Gestor
        self.gestor = GestorBiblioteca()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la estructura principal de la interfaz."""
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
        """Crea la pestaña de gestión de libros."""
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
        """Carga libros desde archivo."""
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
        """Ventana para agregar un libro."""
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
        """Busca un libro por ISBN."""
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
        """Busca libros por título."""
        titulo = self.entry_buscar_titulo.get()
        if titulo:
            libros = self.gestor.buscar_libros_por_titulo(titulo)
            self.mostrar_libros_en_tree(libros)
    
    def buscar_por_autor(self):
        """Busca libros por autor."""
        autor = self.entry_buscar_autor.get()
        if autor:
            libros = self.gestor.buscar_libros_por_autor(autor)
            self.mostrar_libros_en_tree(libros)
    
    def actualizar_lista_libros(self):
        """Actualiza la lista de libros."""
        libros = self.gestor.obtener_todos_los_libros()
        self.mostrar_libros_en_tree(libros)
    
    def mostrar_libros_en_tree(self, libros):
        """Muestra libros en el treeview."""
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
        """Crea la pestaña de usuarios."""
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
        """Ventana para agregar usuario."""
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
        """Muestra el historial de un usuario."""
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
        """Actualiza la lista de usuarios."""
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
        """Crea la pestaña de préstamos."""
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
        """Realiza un préstamo."""
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
        """Devuelve un libro."""
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
        """Muestra préstamos activos."""
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
        """Crea la pestaña de reservas."""
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
        """Crea una reserva."""
        exito, msg = self.gestor.crear_reserva(
            self.entry_res_usuario.get(),
            self.entry_res_isbn.get()
        )
        messagebox.showinfo("Resultado", msg) if exito else messagebox.showerror("Error", msg)
    
    def cancelar_reserva(self):
        """Cancela una reserva."""
        exito, msg = self.gestor.cancelar_reserva(
            self.entry_res_usuario.get(),
            self.entry_res_isbn.get()
        )
        messagebox.showinfo("Resultado", msg) if exito else messagebox.showerror("Error", msg)
    
    def ver_todas_reservas(self):
        """Muestra todas las reservas."""
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
        """Crea la pestaña de estantes."""
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
        """Agrega un estante."""
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
        """Asigna un libro a un estante."""
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
        """Lista todos los estantes."""
        msg = "ESTANTES:\n\n"
        for e in self.gestor.listar_estantes():
            msg += f"Estante {e.id}:\n"
            msg += f"  Libros: {len(e.libros_asignados)}/{e.cantidad}\n"
            msg += f"  Peso: {e.peso_actual:.2f}/{e.peso_maximo:.2f} Kg\n\n"
        messagebox.showinfo("Estantes", msg)
    
    def analisis_peligroso(self):
        """Análisis de fuerza bruta."""
        messagebox.showinfo("Info", "Análisis ejecutándose en consola...")
    
    def optimizacion_estanteria(self):
        """Optimización con backtracking."""
        messagebox.showinfo("Info", "Optimización ejecutándose en consola...")
    
    #  Interfaz Reportes
    
    def crear_interfaz_reportes(self):
        """Crea la pestaña de reportes."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reportes")
        
        ttk.Button(tab, text="Estadísticas Generales", 
                    command=self.mostrar_estadisticas).pack(pady=10)
        ttk.Button(tab, text="Generar Reporte Inventario", 
                    command=self.generar_reporte).pack(pady=10)
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales."""
        stats = self.gestor.obtener_estadisticas()
        msg = f"ESTADÍSTICAS:\n\n"
        msg += f"Libros: {stats['total_libros']}\n"
        msg += f"Usuarios: {stats['total_usuarios']}\n"
        msg += f"Préstamos activos: {stats['prestamos_activos']}\n"
        msg += f"Reservas: {stats['total_reservas']}\n"
        msg += f"Estantes: {stats['total_estantes']}"
        messagebox.showinfo("Estadísticas", msg)
    
    def generar_reporte(self):
        """Genera reporte de inventario."""
        from controllers.ordenamiento.merge_sort import generar_reporte_global
        libros = self.gestor.obtener_todos_los_libros()
        
        if libros:
            generar_reporte_global(libros, criterio='valor', orden='desc',
                                    formato='txt', ruta_archivo='reporte_gui.txt')
            messagebox.showinfo("Éxito", "Reporte en reports/reporte_gui.txt")
        else:
            messagebox.showwarning("Advertencia", "Sin libros")

def iniciar_interfaz_grafica():
    """Inicia la interfaz gráfica."""
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz_grafica()