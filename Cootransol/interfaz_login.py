import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from sistema_cootransol import Administrador, Despachador  # Importar las clases del sistema
from DataBase import agregar_conductor, agregar_vehiculo, eliminar_vehiculo_db, eliminar_conductor_db  # Importar funciones para base de datos
import sqlite3
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# Ventana de inicio de sesión
import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - COOTRANSOL")

        # Centrando la ventana
        self.center_window(350, 350)

        # Cargar y mostrar la imagen
        image = Image.open("D:\Asus\Escritorio\Cootransol\Cootransol\logo.jpg")  # Cambia esto a la ruta de tu imagen
        image = image.resize((200, 100))  # Ajusta el tamaño de la imagen si es necesario
        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(root, image=photo)
        label_image.image = photo  # Esto es necesario para que la imagen no sea eliminada por el recolector de basura
        label_image.pack(pady=10)

        # Etiquetas y entradas para el usuario y la contraseña
        self.label_user = tk.Label(root, text="Usuario")
        self.label_user.pack(pady=5)

        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5, padx=20, fill="x")

        self.label_pass = tk.Label(root, text="Contraseña")
        self.label_pass.pack(pady=5)

        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5, padx=20, fill="x")

        # Botón de inicio de sesión
        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack(pady=20)

    def center_window(self, width=300, height=200):
        """Centrar la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (width/2))
        y_cordinate = int((screen_height/2) - (height/2))
        self.root.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # Suponemos que el administrador tiene el usuario 'admin' y el despachador tiene 'despachador'
        if username == "admin" and password == "1234":
            messagebox.showinfo("Login exitoso", "Bienvenido Administrador")
            self.root.destroy()  # Cerrar la ventana de login
            admin = Administrador(username, password, "admin")
            AdminWindow(admin)  # Abrir la ventana de administración pasando el objeto 'admin'
        elif username == "despachador" and password == "1234":
            messagebox.showinfo("Login exitoso", "Bienvenido Despachador")
            self.root.destroy()  # Cerrar la ventana de login
            despachador = Despachador(username, password, "despachador")
            DespachadorWindow(despachador)  # Abrir la ventana del despachador pasando el objeto 'despachador'
        else:
            messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")

# Ventana para el Administrador
class AdminWindow:
    def __init__(self, admin):
        self.admin = admin
        self.admin_root = tk.Tk()
        self.admin_root.title("Sistema de Gestión de Transporte - COOTRANSOL")
        self.admin_root.state('zoomed')  # Ajusta los valores de ancho y alto según tu preferencia
        self.admin_root.bind("<Escape>", lambda event: self.admin_root.attributes("-fullscreen", False))

        # Crear Notebook (pestañas)
        self.tab_control = ttk.Notebook(self.admin_root)

        # Pestaña de Datos del Conductor
        self.tab_conductor = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_conductor, text="Datos del Conductor")

        # Pestaña de Datos del Vehículo
        self.tab_vehiculo = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_vehiculo, text="Datos del Vehículo")

        # Pestaña de Gestión de Pagos
        self.tab_pagos = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_pagos, text="Gestión de Pagos")

        # Empaquetar las pestañas
        self.tab_control.pack(expand=1, fill="both")

        # Configuración de cada pestaña
        self.setup_conductor_tab()
        self.setup_vehiculo_tab()
        self.setup_pago_tab()

        # Vincular el evento para ajustar el tamaño al cambiar de pestaña
        self.tab_control.bind("<<NotebookTabChanged>>", self.ajustar_tamano_pestana)

        self.admin_root.mainloop()
   
    def ajustar_tamano_pestana(self, event):
        # Obtiene la pestaña seleccionada
        tab_id = event.widget.select()
        frame_activo = event.widget.nametowidget(tab_id)

        # Ajusta el tamaño de la ventana principal según el tamaño del contenido de la pestaña activa
        frame_activo.update_idletasks()  # Asegura que el contenido esté actualizado
        ancho = max(frame_activo.winfo_width(), 1600)  # Valor mínimo de ancho
        alto = max(frame_activo.winfo_height(), 1200)  # Valor mínimo de alto

        self.admin_root.geometry(f"{ancho}x{alto}")  # Ajusta el tamaño de la ventana principal
   
    def setup_conductor_tab(self):
        # Configurar la distribución de las filas y columnas para expandirse
        self.tab_conductor.rowconfigure(1, weight=1)  # Tabla de conductores
        self.tab_conductor.columnconfigure(1, weight=1)  # Columna central
        
        # Campo de búsqueda por identificación
        label_busqueda = tk.Label(self.tab_conductor, text="Buscar por Identificación:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_conductor = tk.Entry(self.tab_conductor)
        self.entry_busqueda_conductor.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_conductor, text="Buscar", command=self.filtrar_conductor)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Tabla para mostrar conductores
        self.tree_conductores = ttk.Treeview(self.tab_conductor, columns=("Identificacion", "Nombre", "Licencia"), show="headings")
        self.tree_conductores.heading("Identificacion", text="Identificacion")
        self.tree_conductores.heading("Nombre", text="Nombre")
        self.tree_conductores.heading("Licencia", text="Vigencia Licencia")
        self.tree_conductores.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Scrollbars para la tabla
        scrollbar_y = ttk.Scrollbar(self.tab_conductor, orient="vertical", command=self.tree_conductores.yview)
        self.tree_conductores.configure(yscroll=scrollbar_y.set)
        scrollbar_y.grid(row=1, column=3, sticky="ns")
        
        # Botón para agregar conductor
        btn_agregar_conductor = tk.Button(self.tab_conductor, text="Agregar Conductor", command=self.abrir_agregar_conductor)
        btn_agregar_conductor.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        # Botón para eliminar conductor
        self.btn_eliminar_conductor = tk.Button(self.tab_conductor, text="Eliminar Conductor", command=self.eliminar_conductor)
        self.btn_eliminar_conductor.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

        # Botón para editar conductor
        self.btn_editar_conductor = tk.Button(self.tab_conductor, text="Editar Conductor", command=self.editar_conductor)
        self.btn_editar_conductor.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        self.cargar_conductores()
   
    def setup_vehiculo_tab(self):
        # Configurar la distribución de las filas y columnas para expandirse
        self.tab_vehiculo.rowconfigure(1, weight=1)  # Tabla de vehículos
        self.tab_vehiculo.columnconfigure(1, weight=1)  # Columna central

        # Campo de búsqueda por placa
        label_busqueda = tk.Label(self.tab_vehiculo, text="Buscar por Placa:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_vehiculo = tk.Entry(self.tab_vehiculo)
        self.entry_busqueda_vehiculo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_vehiculo, text="Buscar", command=self.filtrar_vehiculo)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Tabla para mostrar vehículos
        self.tree_vehiculos = ttk.Treeview(self.tab_vehiculo, columns=("Nro", "Placa", "Estado", "Modelo", "SOAT", "Tarjeta", "Póliza", "Tecno"), show="headings")
        self.tree_vehiculos.heading("Nro", text="Nro")
        self.tree_vehiculos.heading("Placa", text="Placa")
        self.tree_vehiculos.heading("Estado", text="Estado")
        self.tree_vehiculos.heading("Modelo", text="Mod.")
        self.tree_vehiculos.heading("SOAT", text="SOAT")
        self.tree_vehiculos.heading("Tarjeta", text="Tarj. Op.")
        self.tree_vehiculos.heading("Póliza", text="Póliza")
        self.tree_vehiculos.heading("Tecno", text="Tecno")

        # Configurar columnas de la tabla
        self.tree_vehiculos.column("Nro", width=50, anchor="center")
        self.tree_vehiculos.column("Placa", width=80, anchor="center")
        self.tree_vehiculos.column("Estado", width=80, anchor="center")
        self.tree_vehiculos.column("Modelo", width=60, anchor="center")
        self.tree_vehiculos.column("SOAT", width=90, anchor="center")
        self.tree_vehiculos.column("Tarjeta", width=90, anchor="center")
        self.tree_vehiculos.column("Póliza", width=90, anchor="center")
        self.tree_vehiculos.column("Tecno", width=90, anchor="center")

        self.tree_vehiculos.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configurar barras de desplazamiento vertical y horizontal
        scrollbar_y = ttk.Scrollbar(self.tab_vehiculo, orient="vertical", command=self.tree_vehiculos.yview)
        scrollbar_y.grid(row=1, column=3, sticky="ns")
        scrollbar_x = ttk.Scrollbar(self.tab_vehiculo, orient="horizontal", command=self.tree_vehiculos.xview)
        scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.tree_vehiculos.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Botón para agregar vehículo
        btn_agregar_vehiculo = tk.Button(self.tab_vehiculo, text="Agregar Vehículo", command=self.abrir_agregar_vehiculo)
        btn_agregar_vehiculo.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

        # Botón para eliminar vehículo
        self.btn_eliminar_vehiculo = tk.Button(self.tab_vehiculo, text="Eliminar Vehículo", command=self.eliminar_vehiculo)
        self.btn_eliminar_vehiculo.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        # Botón para editar vehículo
        self.btn_editar_vehiculo = tk.Button(self.tab_vehiculo, text="Editar Vehículo", command=self.editar_vehiculo)
        self.btn_editar_vehiculo.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Cargar información de los vehículos ya existentes
        self.cargar_vehiculos()
   
    def setup_pago_tab(self):

        # Crear una tabla para mostrar los movimientos registrados
        self.tree_pagos = ttk.Treeview(self.tab_pagos, columns=("idMovimiento", "fecha", "vueltas", "montoPago", "rutaAsignada", "placaVehiculo", "horaInicio", "horaFin","pagoConfirmadoDesp", "pagado"), show='headings')
        
        # Definir los encabezados de las columnas
        self.tree_pagos.heading("idMovimiento", text="ID Movimiento")
        self.tree_pagos.heading("fecha", text="Fecha")
        self.tree_pagos.heading("vueltas", text="Vueltas")
        self.tree_pagos.heading("montoPago", text="Monto Pago")
        self.tree_pagos.heading("rutaAsignada", text="Ruta Asignada")
        self.tree_pagos.heading("placaVehiculo", text="Placa Vehículo")
        self.tree_pagos.heading("horaInicio", text="Hora Inicio")
        self.tree_pagos.heading("horaFin", text="Hora Fin")
        self.tree_pagos.heading("pagoConfirmadoDesp", text="PCD")
        self.tree_pagos.heading("pagado", text="Pagado")

        # Definir el ancho de las columnas
        for col in ("idMovimiento", "fecha", "vueltas", "montoPago", "rutaAsignada", "placaVehiculo", "horaInicio", "horaFin", "pagado"):
            self.tree_pagos.column(col, width=100)

        # Ubicar la tabla en la pestaña de pagos
        self.tree_pagos.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para marcar pago como realizado
        btn_pagar = tk.Button(self.tab_pagos, text="Marcar Pago Realizado", command=self.marcar_pago)
        btn_pagar.pack(side="left", padx=5, pady=10)

        # Botón para editar movimiento
        btn_editar_movimiento = tk.Button(self.tab_pagos, text="Editar Movimiento", command=self.editar_movimiento)
        btn_editar_movimiento.pack(side="left", padx=5, pady=10)

        # Botón para eliminar movimiento
        btn_eliminar_movimiento = tk.Button(self.tab_pagos, text="Eliminar Movimiento", command=self.eliminar_movimiento)
        btn_eliminar_movimiento.pack(side="left", padx=5, pady=10)

        # Cargar movimientos registrados al iniciar la pestaña de pagos
        self.cargar_movimientos()

    def obtener_numeros_internos(self):
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno FROM Vehiculos")
        numeros_internos = cursor.fetchall()
        conexion.close()
        return [str(nro[0]) for nro in numeros_internos]

    def obtener_placa_por_nro_interno(self, nro_interno):
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT placa FROM Vehiculos WHERE nro_interno = ?", (nro_interno,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado[0] if resultado else "No disponible"

    def editar_movimiento(self):
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un movimiento para editar.")
            return

        # Obtener los datos actuales del movimiento seleccionado
        id_movimiento = self.tree_pagos.item(selected_item, "values")[0]
        fecha_actual = self.tree_pagos.item(selected_item, "values")[1]
        vueltas_actual = self.tree_pagos.item(selected_item, "values")[2]
        monto_actual = self.tree_pagos.item(selected_item, "values")[3]
        ruta_actual = self.tree_pagos.item(selected_item, "values")[4]
        nro_interno_actual = self.tree_pagos.item(selected_item, "values")[5]
        hora_inicio_actual = self.tree_pagos.item(selected_item, "values")[6]
        hora_fin_actual = self.tree_pagos.item(selected_item, "values")[7]

        editar_window = tk.Toplevel(self.admin_root)
        editar_window.title("Editar Movimiento")

        # Entrada para Fecha
        tk.Label(editar_window, text="Fecha:").grid(row=0, column=0, padx=10, pady=5)
        self.fecha_var = tk.StringVar(value=fecha_actual)
        date_entry = DateEntry(editar_window, textvariable=self.fecha_var, date_pattern='dd-mm-yyyy')
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Entrada para Vueltas
        tk.Label(editar_window, text="Vueltas:").grid(row=1, column=0, padx=10, pady=5)
        entry_vueltas = tk.Entry(editar_window)
        entry_vueltas.grid(row=1, column=1, padx=10, pady=5)
        entry_vueltas.insert(0, vueltas_actual)

        # Entrada para Ruta Asignada
        tk.Label(editar_window, text="Ruta Asignada:").grid(row=2, column=0, padx=10, pady=5)
        self.ruta_var = tk.StringVar(value=ruta_actual)
        dropdown_ruta = ttk.Combobox(editar_window, textvariable=self.ruta_var, state="readonly")
        dropdown_ruta["values"] = ["La sirena", "Los chorros", "La estrella", "La cruz", "El jordán",
                                "El mortiñal", "Siloé", "Las palomas", "Nápoles", "Cuatro Esquinas", "Menga"]
        dropdown_ruta.grid(row=2, column=1, padx=10, pady=5)

        # Entrada para Hora de Inicio
        tk.Label(editar_window, text="Hora de Inicio:").grid(row=3, column=0, padx=10, pady=5)
        self.hora_inicio_var = tk.StringVar(value=hora_inicio_actual)
        hora_inicio_picker = ttk.Combobox(editar_window, textvariable=self.hora_inicio_var, state="readonly")
        hora_inicio_picker["values"] = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        hora_inicio_picker.grid(row=3, column=1, padx=10, pady=5)

        # Entrada para Hora de Fin
        tk.Label(editar_window, text="Hora de Fin:").grid(row=4, column=0, padx=10, pady=5)
        self.hora_fin_var = tk.StringVar(value=hora_fin_actual)
        hora_fin_picker = ttk.Combobox(editar_window, textvariable=self.hora_fin_var, state="readonly")
        hora_fin_picker["values"] = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        hora_fin_picker.grid(row=4, column=1, padx=10, pady=5)

        # Entrada para Número Interno (no editable pero mostrará la placa asociada)
        tk.Label(editar_window, text="Número Interno:").grid(row=5, column=0, padx=10, pady=5)
        self.nro_interno_var = tk.StringVar(value=nro_interno_actual)
        nro_interno_dropdown = ttk.Combobox(editar_window, textvariable=self.nro_interno_var, state="readonly")
        nro_interno_dropdown["values"] = self.obtener_numeros_internos()
        nro_interno_dropdown.grid(row=5, column=1, padx=10, pady=5)
        nro_interno_dropdown.bind("<<ComboboxSelected>>", self.actualizar_placa_vehiculo)

        # Mostrar Placa del Vehículo (asociada al Número Interno)
        tk.Label(editar_window, text="Placa del Vehículo:").grid(row=6, column=0, padx=10, pady=5)
        self.placa_var = tk.StringVar(value=self.obtener_placa_por_nro_interno(nro_interno_actual))
        entry_placa = tk.Entry(editar_window, textvariable=self.placa_var, state="readonly")
        entry_placa.grid(row=6, column=1, padx=10, pady=5)

        def guardar_cambios():
            nueva_fecha = self.fecha_var.get()
            nuevas_vueltas = entry_vueltas.get().strip()
            nueva_ruta = self.ruta_var.get().strip()
            nueva_hora_inicio = self.hora_inicio_var.get().strip()
            nueva_hora_fin = self.hora_fin_var.get().strip()

            if not (nueva_fecha and nuevas_vueltas and nueva_ruta and nueva_hora_inicio and nueva_hora_fin):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            # Aquí se debe actualizar el movimiento en la base de datos con los nuevos valores
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute('''UPDATE Movimientos SET fecha = ?, vueltas = ?, rutaAsignada = ?, 
                            horaInicio = ?, horaFin = ? WHERE idMovimiento = ?''',
                        (nueva_fecha, nuevas_vueltas, nueva_ruta, nueva_hora_inicio, nueva_hora_fin, id_movimiento))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Movimiento actualizado correctamente.")
            self.cargar_movimientos()
            editar_window.destroy()

        btn_guardar = tk.Button(editar_window, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=7, column=0, columnspan=2, pady=10)

    def actualizar_placa_vehiculo(self, event=None):
        nro_interno = self.nro_interno_var.get()  # Obtiene el valor seleccionado
        nueva_placa = self.obtener_placa_por_nro_interno(nro_interno)
        self.placa_var.set(nueva_placa)
    def eliminar_movimiento(self):
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un movimiento para eliminar.")
            return

        id_movimiento = self.tree_pagos.item(selected_item, "values")[0]

        # Confirm before deleting
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el movimiento con ID {id_movimiento}?")
        if respuesta:
            # Connect to the database and delete the movement
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Movimientos WHERE idMovimiento = ?", (id_movimiento,))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Movimiento eliminado correctamente.")
            self.cargar_movimientos()
        # Método para cargar los movimientos desde la base de datos
    def cargar_movimientos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tree_pagos.get_children():
            self.tree_pagos.delete(row)

        # Conectar a la base de datos y cargar todos los movimientos con la placa asociada
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT m.idMovimiento, m.fecha, m.vueltas, m.montoPago, m.rutaAsignada, 
                v.placa, m.horaInicio, m.horaFin, m.pagoConfirmadoDesp, m.pagado
            FROM Movimientos m
            LEFT JOIN Vehiculos v ON nro_Interno = v.nro_interno
        ''')
        movimientos = cursor.fetchall()
        conexion.close()

        # Insertar los datos de cada movimiento en la tabla
        for movimiento in movimientos:
            self.tree_pagos.insert("", "end", values=movimiento)
    # Método para marcar un pago como realizado
    def marcar_pago(self):
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un movimiento para marcar como pagado.")
            return

        id_movimiento = self.tree_pagos.item(selected_item, "values")[0]

        # Conectar a la base de datos y marcar el movimiento como pagado
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE Movimientos SET pagado = 'Sí' WHERE idMovimiento = ?", (id_movimiento,))
        conexion.commit()
        conexion.close()

        # Actualizar la tabla de movimientos
        self.cargar_movimientos()
        messagebox.showinfo("Éxito", "Pago marcado como realizado.")
    
    def eliminar_conductor(self):
        # Obtener el conductor seleccionado
        selected_item = self.tree_conductores.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un conductor para eliminar.")
            return

        identificacion = self.tree_conductores.item(selected_item, "values")[0]

        # Confirmación antes de eliminar
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al conductor con ID {identificacion}?")
        if respuesta:
            # Llamada a la función de la base de datos para eliminar
            eliminar_conductor_db(identificacion)
            messagebox.showinfo("Éxito", "Conductor eliminado correctamente.")
            self.cargar_conductores()

    def editar_conductor(self):
        selected_item = self.tree_conductores.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un conductor para editar.")
            return

        identificacion = self.tree_conductores.item(selected_item, "values")[0]
        nombre_actual = self.tree_conductores.item(selected_item, "values")[1]
        vigencia_actual = self.tree_conductores.item(selected_item, "values")[2]

        editar_window = tk.Toplevel(self.admin_root)
        editar_window.title("Editar Conductor")

        tk.Label(editar_window, text="Identificación:").grid(row=0, column=0, padx=10, pady=5)
        entry_id = tk.Entry(editar_window)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        entry_id.insert(0, identificacion)

        tk.Label(editar_window, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(editar_window)
        entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        entry_nombre.insert(0, nombre_actual)

        tk.Label(editar_window, text="Vigencia Licencia:").grid(row=2, column=0, padx=10, pady=5)
        # Usar DateEntry para seleccionar la fecha de vigencia de la licencia
        entry_vigencia = DateEntry(editar_window, date_pattern='dd-mm-yyyy')
        entry_vigencia.grid(row=2, column=1, padx=10, pady=5)
        entry_vigencia.set_date(vigencia_actual)  # Establecer la fecha actual

        def guardar_cambios():
            nuevo_id = entry_id.get().strip()
            nuevo_nombre = entry_nombre.get().strip()
            nueva_vigencia = entry_vigencia.get().strip()

            if not nuevo_id or not nuevo_nombre or not nueva_vigencia:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE Conductores SET identificacion = ?, nombre = ?, vigencia_licencia = ? WHERE identificacion = ?",
                        (nuevo_id, nuevo_nombre, nueva_vigencia, identificacion))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Conductor editado correctamente.")
            self.cargar_conductores()
            editar_window.destroy()

        tk.Button(editar_window, text="Guardar Cambios", command=guardar_cambios).grid(row=3, column=0, columnspan=2, pady=10)

    def eliminar_vehiculo(self):
        selected_item = self.tree_vehiculos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un vehículo para eliminar.")
            return

        placa = self.tree_vehiculos.item(selected_item, "values")[1]

        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el vehículo con placa {placa}?")
        if respuesta:
            eliminar_vehiculo_db(placa)
            messagebox.showinfo("Éxito", "Vehículo eliminado correctamente.")
            self.cargar_vehiculos()

    def editar_vehiculo(self):
        selected_item = self.tree_vehiculos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un vehículo para editar.")
            return

        # Obtener los datos actuales del vehículo seleccionado
        nro_interno = self.tree_vehiculos.item(selected_item, "values")[0]
        placa_actual = self.tree_vehiculos.item(selected_item, "values")[1]
        estado_actual = self.tree_vehiculos.item(selected_item, "values")[2]
        modelo_actual = self.tree_vehiculos.item(selected_item, "values")[3]
        soat_actual = self.tree_vehiculos.item(selected_item, "values")[4]
        tarjeta_actual = self.tree_vehiculos.item(selected_item, "values")[5]
        poliza_actual = self.tree_vehiculos.item(selected_item, "values")[6]
        tecno_actual = self.tree_vehiculos.item(selected_item, "values")[7]

        editar_window = tk.Toplevel(self.admin_root)
        editar_window.title("Editar Vehículo")

        tk.Label(editar_window, text="Número Interno:").grid(row=0, column=0, padx=10, pady=5)
        entry_nro_interno = tk.Entry(editar_window)
        entry_nro_interno.grid(row=0, column=1, padx=10, pady=5)
        entry_nro_interno.insert(0, nro_interno)

        tk.Label(editar_window, text="Placa:").grid(row=1, column=0, padx=10, pady=5)
        entry_placa = tk.Entry(editar_window)
        entry_placa.grid(row=1, column=1, padx=10, pady=5)
        entry_placa.insert(0, placa_actual)

        tk.Label(editar_window, text="Estado:").grid(row=2, column=0, padx=10, pady=5)
        entry_estado = tk.Entry(editar_window)
        entry_estado.grid(row=2, column=1, padx=10, pady=5)
        entry_estado.insert(0, estado_actual)

        tk.Label(editar_window, text="Modelo:").grid(row=3, column=0, padx=10, pady=5)
        entry_modelo = tk.Entry(editar_window)
        entry_modelo.grid(row=3, column=1, padx=10, pady=5)
        entry_modelo.insert(0, modelo_actual)

        tk.Label(editar_window, text="Vigencia SOAT:").grid(row=4, column=0, padx=10, pady=5)
        entry_soat = DateEntry(editar_window, date_pattern='dd-mm-yyyy')
        entry_soat.grid(row=4, column=1, padx=10, pady=5)
        entry_soat.set_date(soat_actual)  # Asume que el formato de fecha está en 'dd-mm-yyyy'

        tk.Label(editar_window, text="Vigencia Tarjeta:").grid(row=5, column=0, padx=10, pady=5)
        entry_tarjeta = DateEntry(editar_window, date_pattern='dd-mm-yyyy')
        entry_tarjeta.grid(row=5, column=1, padx=10, pady=5)
        entry_tarjeta.set_date(tarjeta_actual)

        tk.Label(editar_window, text="Vigencia Póliza:").grid(row=6, column=0, padx=10, pady=5)
        entry_poliza = DateEntry(editar_window, date_pattern='dd-mm-yyyy')
        entry_poliza.grid(row=6, column=1, padx=10, pady=5)
        entry_poliza.set_date(poliza_actual)

        tk.Label(editar_window, text="Vigencia Tecnomecánica:").grid(row=7, column=0, padx=10, pady=5)
        entry_tecno = DateEntry(editar_window, date_pattern='dd-mm-yyyy')
        entry_tecno.grid(row=7, column=1, padx=10, pady=5)
        entry_tecno.set_date(tecno_actual)

        # Dropdown para seleccionar un conductor disponible
        tk.Label(editar_window, text="Asignar Conductor:").grid(row=8, column=0, padx=10, pady=5)
        self.conductor_var = tk.StringVar()
        self.dropdown_conductor = ttk.Combobox(editar_window, textvariable=self.conductor_var, state="readonly")
        self.dropdown_conductor.grid(row=8, column=1, padx=10, pady=5)

        # Cargar conductores disponibles (excluyendo aquellos que ya tienen un vehículo asignado)
        conductores_disponibles = self.obtener_conductores_disponibles(nro_interno)
        self.dropdown_conductor["values"] = conductores_disponibles

        def guardar_cambios():
            nuevo_nro_interno = entry_nro_interno.get().strip()
            nueva_placa = entry_placa.get().strip()
            nuevo_estado = entry_estado.get().strip()
            nuevo_modelo = entry_modelo.get().strip()
            nueva_vigencia_soat = entry_soat.get()  # Obtener la fecha seleccionada
            nueva_vigencia_tarjeta = entry_tarjeta.get()  # Obtener la fecha seleccionada
            nueva_vigencia_poliza = entry_poliza.get()  # Obtener la fecha seleccionada
            nueva_vigencia_tecno = entry_tecno.get()  # Obtener la fecha seleccionada
            conductor_seleccionado = self.conductor_var.get()

            # Validar que todos los campos estén completos
            if not (nuevo_nro_interno and nueva_placa and nuevo_estado and nuevo_modelo and 
                    nueva_vigencia_soat and nueva_vigencia_tarjeta and nueva_vigencia_poliza and 
                    nueva_vigencia_tecno and conductor_seleccionado):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            # Separar el ID del conductor seleccionado
            id_conductor = conductor_seleccionado.split(" - ")[0]

            # Conectar a la base de datos y actualizar los datos del vehículo
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute('''
                UPDATE Vehiculos 
                SET nro_interno = ?, placa = ?, estado = ?, modelo = ?, 
                    vigencia_soat = ?, vigencia_tarjeta = ?, vigencia_poliza = ?, 
                    vigencia_tecnomecanica = ?, idConductor = ?
                WHERE nro_interno = ?
            ''', (
                nuevo_nro_interno, nueva_placa, nuevo_estado, nuevo_modelo, 
                nueva_vigencia_soat, nueva_vigencia_tarjeta, nueva_vigencia_poliza, 
                nueva_vigencia_tecno, id_conductor, nro_interno
            ))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Vehículo editado correctamente.")
            self.cargar_vehiculos()
            editar_window.destroy()

        # Botón para guardar cambios
        btn_guardar = tk.Button(editar_window, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=10, column=0, columnspan=2, pady=10)

    def filtrar_conductor(self):
        # Lógica para filtrar los conductores en la base de datos y mostrar resultados en la tabla
        identificacion = self.entry_busqueda_conductor.get().strip()
        
        #Verificación de campo vacio
        if not identificacion:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una identificación para buscar.")
            return        # Conectar a la base de datos y buscar el conductor por identificación

        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT identificacion, nombre, vigencia_licencia FROM Conductores WHERE identificacion = ?", (identificacion,))
        conductor = cursor.fetchone()
        conexion.close()

         # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_conductores.get_children():
            self.tree_conductores.delete(row)

        # Mostrar el conductor encontrado o mensaje si no existe
        if conductor:
            self.tree_conductores.insert("", "end", values=conductor)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un conductor con esa identificación.")

    def filtrar_vehiculo(self):
        # Obtener el valor de la placa desde el campo de búsqueda
        placa = self.entry_busqueda_vehiculo.get().strip()

        # Validación de campo vacío
        if not placa:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una placa para buscar.")
            return

        # Conectar a la base de datos y buscar el vehículo por placa
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos WHERE placa = ?", (placa,))
        vehiculos = cursor.fetchall()
        conexion.close()

        # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Mostrar los vehículos encontrados o mensaje si no existe
        if vehiculos:
            for vehiculo in vehiculos:
                self.tree_vehiculos.insert("", "end", values=vehiculo)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un vehículo con esa placa.")

    def abrir_agregar_conductor(self):
        agregar_window = tk.Toplevel(self.admin_root)
        agregar_window.title("Agregar Conductor")

        label_id = tk.Label(agregar_window, text="Identificación:")
        label_id.grid(row=0, column=0, padx=10, pady=10)
        entry_id = tk.Entry(agregar_window)
        entry_id.grid(row=0, column=1, padx=10, pady=10)

        label_nombre = tk.Label(agregar_window, text="Nombre:")
        label_nombre.grid(row=1, column=0, padx=10, pady=10)
        entry_nombre = tk.Entry(agregar_window)
        entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        label_licencia = tk.Label(agregar_window, text="Vigencia Licencia:")
        label_licencia.grid(row=2, column=0, padx=10, pady=10)
        
        # Usar DateEntry para seleccionar la fecha de vigencia de la licencia
        entry_licencia = DateEntry(agregar_window, date_pattern='dd-mm-yyyy')
        entry_licencia.grid(row=2, column=1, padx=10, pady=10)

        def agregar_conductor_callback():
            identificacion = entry_id.get().strip()
            nombre = entry_nombre.get().strip()
            licencia = entry_licencia.get().strip()

            # Validación de campos
            if not identificacion or not nombre or not licencia:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            # Llamada a la función de agregar conductor con identificación
            agregar_conductor(identificacion, nombre, licencia)
            messagebox.showinfo("Éxito", "Conductor agregado correctamente")
            self.cargar_conductores()
            agregar_window.destroy()

        btn_guardar = tk.Button(agregar_window, text="Guardar", command=agregar_conductor_callback)
        btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)
   
    def asignar_conductor_vehiculo(self):
        # Crear ventana para la asignación
        asignar_window = tk.Toplevel(self.admin_root)
        asignar_window.title("Asignar Conductor a Vehículo")

        # Campo para seleccionar el ID del vehículo
        label_vehiculo = tk.Label(asignar_window, text="ID Vehículo:")
        label_vehiculo.grid(row=0, column=0, padx=10, pady=10)
        entry_vehiculo = tk.Entry(asignar_window)
        entry_vehiculo.grid(row=0, column=1, padx=10, pady=10)

        # Campo para seleccionar la identificación del conductor
        label_conductor = tk.Label(asignar_window, text="Identificación del Conductor:")
        label_conductor.grid(row=1, column=0, padx=10, pady=10)
        entry_conductor = tk.Entry(asignar_window)
        entry_conductor.grid(row=1, column=1, padx=10, pady=10)

        def asignar_callback():
            id_vehiculo = entry_vehiculo.get().strip()
            id_conductor = entry_conductor.get().strip()

            # Validación de campos vacíos
            if not id_vehiculo or not id_conductor:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            # Actualizar la base de datos para asignar el conductor al vehículo
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE Vehiculos SET idConductor = ? WHERE idVehiculo = ?", (id_conductor, id_vehiculo))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Conductor asignado al vehículo correctamente")
            asignar_window.destroy()

        btn_guardar = tk.Button(asignar_window, text="Asignar", command=asignar_callback)
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=10)
    
    def cargar_conductores(self):
    # Limpiar la tabla antes de agregar nuevos datos
        for row in self.tree_conductores.get_children():
            self.tree_conductores.delete(row)

        # Conectar a la base de datos y obtener todos los conductores
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT identificacion, nombre, vigencia_licencia FROM Conductores")
        conductores = cursor.fetchall()
        conexion.close()

    # Insertar cada conductor en la tabla
        for conductor in conductores:
            self.tree_conductores.insert("", "end", values=conductor)

    def cargar_vehiculos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Conectar a la base de datos y cargar todos los vehículos
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos")
        vehiculos = cursor.fetchall()
        conexion.close()

        # Insertar los datos de cada vehículo en la tabla
        for vehiculo in vehiculos:
            self.tree_vehiculos.insert("", "end", values=vehiculo)

    def buscar_vehiculo(self):
        # Obtener el valor de la placa desde el campo de búsqueda
        placa = self.entry_busqueda_vehiculo.get().strip()

        # Validación de campo vacío
        if not placa:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una placa para buscar.")
            return

        # Conectar a la base de datos y buscar el vehículo por placa
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos WHERE placa = ?", (placa,))
        vehiculo = cursor.fetchone()
        conexion.close()

        # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Mostrar el vehículo encontrado o mensaje si no existe
        if vehiculo:
            self.tree_vehiculos.insert("", "end", values=vehiculo)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un vehículo con esa placa.")

    def abrir_agregar_vehiculo(self):
        # Ventana para agregar un nuevo vehículo
        agregar_window = tk.Toplevel(self.admin_root)
        agregar_window.title("Agregar Vehículo")

        # Definir etiquetas y entradas para cada atributo del vehículo
        labels = ["Número interno", "Placa", "Estado", "Modelo"]
        entries = {}

        # Crear entradas para los campos básicos
        for i, label_text in enumerate(labels):
            label = tk.Label(agregar_window, text=label_text + ":")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(agregar_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label_text] = entry

        # Crear DateEntry para fechas de vigencia
        fecha_labels = ["Vigencia SOAT", "Vigencia Tarjeta", "Vigencia Póliza", "Vigencia Tecnomecánica"]
        date_entries = {}

        for j, fecha_label in enumerate(fecha_labels):
            label = tk.Label(agregar_window, text=fecha_label + ":")
            label.grid(row=len(labels) + j, column=0, padx=10, pady=5)
            date_entry = DateEntry(agregar_window, date_pattern='dd-mm-yyyy')
            date_entry.grid(row=len(labels) + j, column=1, padx=10, pady=5)
            date_entries[fecha_label] = date_entry

        # Dropdown para seleccionar el conductor disponible
        label_conductor = tk.Label(agregar_window, text="Asignar Conductor:")
        label_conductor.grid(row=len(labels) + len(fecha_labels), column=0, padx=10, pady=5)

        # Variable y dropdown para conductores disponibles
        self.conductor_var = tk.StringVar()
        self.dropdown_conductor = ttk.Combobox(agregar_window, textvariable=self.conductor_var, state="readonly")
        self.dropdown_conductor.grid(row=len(labels) + len(fecha_labels), column=1, padx=10, pady=5)

        # Cargar conductores disponibles con formato adecuado
        conductores_disponibles = self.obtener_conductores_disponibles()
        self.dropdown_conductor["values"] = conductores_disponibles

        def agregar_vehiculo_callback():
            # Obtener los valores de entrada
            datos_vehiculo = {key: entry.get().strip() for key, entry in entries.items()}
            conductor_seleccionado = self.conductor_var.get()

            # Validación de campos vacíos
            if any(value == "" for value in datos_vehiculo.values()) or not conductor_seleccionado:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            # Obtener fechas de las entradas de calendario
            for fecha_label, date_entry in date_entries.items():
                datos_vehiculo[fecha_label] = date_entry.get_date().strftime('%d-%m-%Y')

            # Separar el ID del conductor seleccionado
            id_conductor = conductor_seleccionado.split(" - ")[0]

            # Verificar si el conductor ya tiene un vehículo asignado
            if not self.verificar_conductor_disponible(id_conductor):
                messagebox.showerror("Error", "El conductor ya tiene un vehículo asignado.")
                return

            # Convertir el valor de "Número interno" a entero
            try:
                datos_vehiculo["Número interno"] = int(datos_vehiculo["Número interno"])
            except ValueError:
                messagebox.showerror("Error", "El Número interno debe ser un número entero.")
                return

            # Llamada a la función de agregar vehículo con el conductor asignado
            agregar_vehiculo(
                nro_interno=datos_vehiculo["Número interno"],  
                placa=datos_vehiculo["Placa"],
                estado=datos_vehiculo["Estado"],
                modelo=datos_vehiculo["Modelo"],
                vigencia_soat=datos_vehiculo["Vigencia SOAT"],
                vigencia_tarjeta=datos_vehiculo["Vigencia Tarjeta"],
                vigencia_poliza=datos_vehiculo["Vigencia Póliza"],
                vigencia_tecnomecanica=datos_vehiculo["Vigencia Tecnomecánica"],
                id_conductor=id_conductor
            )
            
            messagebox.showinfo("Éxito", "Vehículo agregado correctamente y conductor asignado.")

            # Actualizar la tabla con los datos más recientes
            self.cargar_vehiculos()
            agregar_window.destroy()

        # Botón para guardar el vehículo
        btn_guardar = tk.Button(agregar_window, text="Guardar", command=agregar_vehiculo_callback)
        btn_guardar.grid(row=len(labels) + len(fecha_labels) + 1, column=0, columnspan=2, pady=10)
   
    def obtener_conductores_disponibles(self, nro_interno=None):
        try:
            # Confirma la ruta de la base de datos
            db_path = "D:/Asus/Escritorio/Cootransol/Cootransol/cootransol.db"
            print(f"Usando la base de datos en: {db_path}")

            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            # Modificar la consulta para filtrar conductores si es necesario
            if nro_interno is not None:
                print("Filtrando conductores, excluyendo el asignado al vehículo actual...")
                cursor.execute("""
                    SELECT identificacion, nombre 
                    FROM Conductores 
                    WHERE identificacion NOT IN (
                        SELECT idConductor FROM Vehiculos WHERE idConductor IS NOT NULL AND nro_interno != ?
                    )
                """, (nro_interno,))
            else:
                print("Obteniendo todos los conductores disponibles...")
                cursor.execute("""
                    SELECT identificacion, nombre 
                    FROM Conductores 
                    WHERE identificacion NOT IN (
                        SELECT idConductor FROM Vehiculos WHERE idConductor IS NOT NULL
                    )
                """)
            
            conductores = cursor.fetchall()
            print("Conductores disponibles:", conductores)

            conexion.close()

            # Formatear para visualización en la lista desplegable
            return [f"{identificacion} - {nombre}" for identificacion, nombre in conductores]

        except sqlite3.OperationalError as e:
            print("Error en consulta SQL:", e)
            return []

    def verificar_conductor_disponible(self, id_conductor):
        """Verifica si el conductor está disponible (sin vehículo asignado)."""
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Vehiculos WHERE idConductor = ?", (id_conductor,))
        resultado = cursor.fetchone()[0]
        conexion.close()

        # Si el resultado es 0, el conductor está disponible
        return resultado == 0
# Ventana para el Despachador
class DespachadorWindow:
    def __init__(self, despachador):
        self.despachador = despachador
        self.despachador_root = tk.Tk()
        self.despachador_root.title("Sistema de Gestión de Transporte - COOTRANSOL")
        self.despachador_root.state('zoomed')
        # Crear Notebook (pestañas)
        self.tab_control = ttk.Notebook(self.despachador_root)

        # Pestaña de Datos del Conductor
        self.tab_conductor = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_conductor, text="Datos del Conductor")

        # Pestaña de Datos del Vehículo
        self.tab_vehiculo = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_vehiculo, text="Datos del Vehículo")

        # Pestaña de Gestión de Pagos
        self.tab_pagos = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_pagos, text="Gestión de Pagos")

        # Empaquetar las pestañas
        self.tab_control.pack(expand=1, fill="both")

        # Configuración de cada pestaña
        self.setup_conductor_tab()
        self.setup_vehiculo_tab()
        self.setup_pago_tab()

        self.despachador_root.mainloop()

    def setup_conductor_tab(self):
        # Configuración del layout general
        self.tab_conductor.columnconfigure(1, weight=1)
        self.tab_conductor.rowconfigure(1, weight=1)

        # Campo de búsqueda por identificación
        label_busqueda = tk.Label(self.tab_conductor, text="Buscar por Identificación:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_conductor = tk.Entry(self.tab_conductor)
        self.entry_busqueda_conductor.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_conductor, text="Buscar", command=self.buscar_conductor)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Tabla para mostrar conductores
        self.tree_conductores = ttk.Treeview(self.tab_conductor, columns=("Identificacion", "Nombre", "Licencia"), show="headings")
        self.tree_conductores.heading("Identificacion", text="Identificacion")
        self.tree_conductores.heading("Nombre", text="Nombre")
        self.tree_conductores.heading("Licencia", text="Vigencia Licencia")
        self.tree_conductores.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configurar barras de desplazamiento
        scrollbar_y = ttk.Scrollbar(self.tab_conductor, orient="vertical", command=self.tree_conductores.yview)
        scrollbar_y.grid(row=1, column=3, sticky="ns")
        scrollbar_x = ttk.Scrollbar(self.tab_conductor, orient="horizontal", command=self.tree_conductores.xview)
        scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        self.tree_conductores.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Cargar info de los conductores ya existentes
        self.cargar_conductores()

    def buscar_conductor(self):
        # Obtener el valor de la identificación desde el campo de búsqueda
        identificacion = self.entry_busqueda.get().strip()

        # Validación de campo vacío
        if not identificacion:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una identificación para buscar.")
            return

        # Conectar a la base de datos y buscar el conductor por identificación
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT identificacion, nombre, vigencia_licencia FROM Conductores WHERE identificacion = ?", (identificacion,))
        conductor = cursor.fetchone()
        conexion.close()

        # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_conductores.get_children():
            self.tree_conductores.delete(row)

        # Mostrar el conductor encontrado o mensaje si no existe
        if conductor:
            self.tree_conductores.insert("", "end", values=conductor)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un conductor con esa identificación.")
   
    def cargar_conductores(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tree_conductores.get_children():
            self.tree_conductores.delete(row)

        # Conectar a la base de datos y cargar todos los conductores
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT identificacion, nombre, vigencia_licencia FROM Conductores")
        conductores = cursor.fetchall()
        conexion.close()

        # Insertar los datos de cada conductor en la tabla
        for conductor in conductores:
            self.tree_conductores.insert("", "end", values=conductor)
    
    def setup_vehiculo_tab(self):
        # Configuración del layout general
        self.tab_vehiculo.columnconfigure(1, weight=1)
        self.tab_vehiculo.rowconfigure(1, weight=1)

        # Campo de búsqueda por placa
        label_busqueda = tk.Label(self.tab_vehiculo, text="Buscar por Placa:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_busqueda_vehiculo = tk.Entry(self.tab_vehiculo)
        self.entry_busqueda_vehiculo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Expansión horizontal para la entrada de búsqueda
        self.tab_vehiculo.columnconfigure(1, weight=1)

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_vehiculo, text="Buscar", command=self.filtrar_vehiculo)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar vehículos
        self.tree_vehiculos = ttk.Treeview(self.tab_vehiculo, columns=("Nro", "Placa", "Estado", "Modelo", "SOAT", "Tarjeta", "Póliza", "Tecno"), show="headings")
        
        # Configurar encabezados de la tabla con nombres más compactos
        self.tree_vehiculos.heading("Nro", text="Nro")
        self.tree_vehiculos.heading("Placa", text="Placa")
        self.tree_vehiculos.heading("Estado", text="Estado")
        self.tree_vehiculos.heading("Modelo", text="Mod.")
        self.tree_vehiculos.heading("SOAT", text="SOAT")
        self.tree_vehiculos.heading("Tarjeta", text="Tarj. Op.")
        self.tree_vehiculos.heading("Póliza", text="Póliza")
        self.tree_vehiculos.heading("Tecno", text="Tecno")

        # Configurar columnas de la tabla con un ancho más reducido
        self.tree_vehiculos.column("Nro", width=50, anchor="center")
        self.tree_vehiculos.column("Placa", width=80, anchor="center")
        self.tree_vehiculos.column("Estado", width=80, anchor="center")
        self.tree_vehiculos.column("Modelo", width=60, anchor="center")
        self.tree_vehiculos.column("SOAT", width=90, anchor="center")
        self.tree_vehiculos.column("Tarjeta", width=90, anchor="center")
        self.tree_vehiculos.column("Póliza", width=90, anchor="center")
        self.tree_vehiculos.column("Tecno", width=90, anchor="center")

        self.tree_vehiculos.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configurar barras de desplazamiento vertical y horizontal
        scrollbar_y = ttk.Scrollbar(self.tab_vehiculo, orient="vertical", command=self.tree_vehiculos.yview)
        scrollbar_y.grid(row=1, column=3, sticky="ns")
        scrollbar_x = ttk.Scrollbar(self.tab_vehiculo, orient="horizontal", command=self.tree_vehiculos.xview)
        scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        self.tree_vehiculos.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Cargar info de los vehículos ya existentes
        self.cargar_vehiculos()
    def cargar_vehiculos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Conectar a la base de datos y cargar todos los vehículos
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos")
        vehiculos = cursor.fetchall()
        conexion.close()

        # Insertar los datos de cada vehículo en la tabla
        for vehiculo in vehiculos:
            self.tree_vehiculos.insert("", "end", values=vehiculo) 

    def buscar_vehiculo(self):
        # Obtener el valor de la placa desde el campo de búsqueda
        placa = self.entry_busqueda_vehiculo.get().strip()

        # Validación de campo vacío
        if not placa:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una placa para buscar.")
            return

        # Conectar a la base de datos y buscar el vehículo por placa
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos WHERE placa = ?", (placa,))
        vehiculo = cursor.fetchone()
        conexion.close()

        # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Mostrar el vehículo encontrado o mensaje si no existe
        if vehiculo:
            self.tree_vehiculos.insert("", "end", values=vehiculo)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un vehículo con esa placa.")

    def filtrar_vehiculo(self):
        # Obtener el valor de la placa desde el campo de búsqueda
        placa = self.entry_busqueda_vehiculo.get().strip()

        # Validación de campo vacío
        if not placa:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese una placa para buscar.")
            return

        # Conectar a la base de datos y buscar el vehículo por placa
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno, placa, estado, modelo, vigencia_soat, vigencia_tarjeta, vigencia_poliza, vigencia_tecnomecanica FROM Vehiculos WHERE placa = ?", (placa,))
        vehiculos = cursor.fetchall()
        conexion.close()

        # Limpiar la tabla antes de mostrar el resultado de la búsqueda
        for row in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(row)

        # Mostrar los vehículos encontrados o mensaje si no existe
        if vehiculos:
            for vehiculo in vehiculos:
                self.tree_vehiculos.insert("", "end", values=vehiculo)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un vehículo con esa placa.")

    def setup_pago_tab(self):

        # Crear una tabla para mostrar los movimientos registrados
        self.tree_pagos = ttk.Treeview(
        self.tab_pagos, 
        columns=("idMovimiento", "fecha", "vueltas", "montoPago", "rutaAsignada", 
                "placaVehiculo", "horaInicio", "horaFin", "pagoConfirmadoDesp", "pagado"), 
        show='headings'
    )
      
        # Definir los encabezados de las columnas
        self.tree_pagos.heading("idMovimiento", text="ID Movimiento")
        self.tree_pagos.heading("fecha", text="Fecha")
        self.tree_pagos.heading("vueltas", text="Vueltas")
        self.tree_pagos.heading("montoPago", text="Monto Pago")
        self.tree_pagos.heading("rutaAsignada", text="Ruta Asignada")
        self.tree_pagos.heading("placaVehiculo", text="Placa Vehículo")
        self.tree_pagos.heading("horaInicio", text="Hora Inicio")
        self.tree_pagos.heading("horaFin", text="Hora Fin")
        self.tree_pagos.heading("pagoConfirmadoDesp", text="PCD")
        self.tree_pagos.heading("pagado", text="Pagado")

        # Definir el ancho de las columnas
        for col in ("idMovimiento", "fecha", "vueltas", "montoPago", "rutaAsignada", 
            "placaVehiculo", "horaInicio", "horaFin", "pagoConfirmadoDesp", "pagado"):
            self.tree_pagos.column(col, width=100)


        # Ubicar la tabla en la pestaña de pagos
        self.tree_pagos.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para marcar pago por despachador como realizado 
        btn_pagar = tk.Button(self.tab_pagos, text="Marcar Pago Realizado (Despachador)", command=self.confirmar_pago_despachador)
        btn_pagar.pack(side="left", padx=5)

        # Botón para agregar un nuevo movimiento
        btn_agregar_movimiento = tk.Button(self.tab_pagos, text="Agregar Movimiento", command=self.agregar_movimiento)
        btn_agregar_movimiento.pack(side="left", padx=5)

        # Cargar movimientos registrados al iniciar la pestaña de pagos
        self.cargar_movimientos()
    
    def confirmar_pago_despachador(self):
        selected_item = self.tree_pagos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un movimiento para confirmar el pago.")
            return

        id_movimiento = self.tree_pagos.item(selected_item, "values")[0]

        # Conectar a la base de datos y actualizar el estado de confirmación del pago
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE Movimientos SET pagoConfirmadoDesp = 'Sí' WHERE idMovimiento = ?", (id_movimiento,))
        conexion.commit()
        conexion.close()

        # Actualizar la tabla de movimientos
        self.cargar_movimientos()
        messagebox.showinfo("Éxito", "Pago confirmado por el despachador.")
    # Método para cargar los movimientos desde la base de datos
    def cargar_movimientos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tree_pagos.get_children():
            self.tree_pagos.delete(row)

        # Conectar a la base de datos y cargar todos los movimientos
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT idMovimiento, fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, horaInicio, horaFin, pagoConfirmadoDesp, pagado FROM Movimientos")
        movimientos = cursor.fetchall()
        conexion.close()

        # Insertar los datos de cada movimiento en la tabla
        for movimiento in movimientos:
            self.tree_pagos.insert("", "end", values=movimiento)

    def agregar_movimiento(self):
        agregar_window = tk.Toplevel(self.despachador_root)
        agregar_window.title("Agregar Nuevo Movimiento")

        tk.Label(agregar_window, text="Número Interno:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nro_interno_var = tk.StringVar()
        dropdown_nro_interno = ttk.Combobox(agregar_window, textvariable=self.nro_interno_var)
        dropdown_nro_interno.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Cargar números internos en la lista desplegable
        numeros_internos = self.obtener_numeros_internos()
        dropdown_nro_interno["values"] = numeros_internos
        dropdown_nro_interno.bind("<<ComboboxSelected>>", self.actualizar_placa_vehiculo)

        tk.Label(agregar_window, text="Placa del Vehículo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.placa_var = tk.StringVar()
        entry_placa = tk.Entry(agregar_window, textvariable=self.placa_var, state="readonly")
        entry_placa.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(agregar_window, text="Fecha del Movimiento:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fecha_var = tk.StringVar()
        date_entry = DateEntry(agregar_window, textvariable=self.fecha_var, date_pattern='dd-mm-yyyy')
        date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(agregar_window, text="Vueltas:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_vueltas = tk.Entry(agregar_window)
        entry_vueltas.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(agregar_window, text="Ruta Asignada:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ruta_var = tk.StringVar()
        dropdown_ruta = ttk.Combobox(agregar_window, textvariable=self.ruta_var, state="readonly")
        dropdown_ruta["values"] = [
            "La sirena", "Los chorros", "La estrella", "La cruz", 
            "El jordán", "El mortiñal", "Siloé", "Las palomas", 
            "Nápoles", "Cuatro Esquinas", "Menga"
        ]
        dropdown_ruta.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(agregar_window, text="Hora de Inicio:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        horas = [f"{h:02}" for h in range(24)]  # Lista de horas 00-23
        minutos = [f"{m:02}" for m in range(60)]  # Lista de minutos 00-59

        self.hora_inicio_var = tk.StringVar()
        self.minuto_inicio_var = tk.StringVar()

        dropdown_hora_inicio = ttk.Combobox(agregar_window, textvariable=self.hora_inicio_var, values=horas, state="readonly", width=3)
        dropdown_hora_inicio.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        dropdown_minuto_inicio = ttk.Combobox(agregar_window, textvariable=self.minuto_inicio_var, values=minutos, state="readonly", width=3)
        dropdown_minuto_inicio.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        tk.Label(agregar_window, text="Hora de Fin:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.hora_fin_var = tk.StringVar()
        self.minuto_fin_var = tk.StringVar()

        dropdown_hora_fin = ttk.Combobox(agregar_window, textvariable=self.hora_fin_var, values=horas, state="readonly", width=3)
        dropdown_hora_fin.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        dropdown_minuto_fin = ttk.Combobox(agregar_window, textvariable=self.minuto_fin_var, values=minutos, state="readonly", width=3)
        dropdown_minuto_fin.grid(row=6, column=2, padx=5, pady=5, sticky="w")

        def guardar_movimiento():
            nro_interno = self.nro_interno_var.get().strip()
            # Validación para asegurarse de que el número interno esté seleccionado
            if not nro_interno:
                messagebox.showwarning("Advertencia", "Debe seleccionar un número interno válido.")
                return
            fecha = self.fecha_var.get().strip()
            vueltas = entry_vueltas.get().strip()
            ruta_asignada = self.ruta_var.get().strip()
            if not ruta_asignada:
                messagebox.showwarning("Advertencia", "Debe seleccionar una ruta válida.")
                return
            hora_inicio = self.hora_inicio_var.get().strip()
            hora_fin = self.hora_fin_var.get().strip()

            # Validar campos vacíos
            if not (nro_interno and fecha and vueltas and ruta_asignada and hora_inicio and hora_fin):
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            try:
                vueltas = float(vueltas)
            except ValueError:
                messagebox.showwarning("Error de Valor", "La cantidad de vueltas debe ser un número.")
                return

            # Conectar a la base de datos para verificar el último movimiento del vehículo
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT pagado FROM Movimientos 
                WHERE numeroInternoVehiculo = ? 
                ORDER BY idMovimiento DESC 
                LIMIT 1
            ''', (nro_interno,))
            ultimo_movimiento = cursor.fetchone()

            if ultimo_movimiento and ultimo_movimiento[0] != "Sí":
                messagebox.showwarning("Restricción", "No se puede agregar un nuevo movimiento hasta que el movimiento anterior esté marcado como pagado.")
                conexion.close()
                return

            # Calcular el monto del pago basado en la cantidad de vueltas
            if vueltas <= 1:
                monto_pago = 54000
            else:
                monto_pago = 94000

            # Insertar el nuevo movimiento en la base de datos
            cursor.execute('''
                INSERT INTO Movimientos (fecha, vueltas, montoPago, rutaAsignada, placaVehiculo, numeroInternoVehiculo, horaInicio, horaFin, pagado)
                VALUES (?, ?, ?, ?, NULL, ?, ?, ?, 'No')
            ''', (fecha, vueltas, monto_pago, ruta_asignada, nro_interno, hora_inicio, hora_fin))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Nuevo movimiento agregado.")
            self.cargar_movimientos()  # Para actualizar la tabla en la interfaz
            agregar_window.destroy()
        btn_guardar = tk.Button(agregar_window, text="Guardar Movimiento", command=guardar_movimiento)
        btn_guardar.grid(row=7, column=0, columnspan=2, pady=10)

    def obtener_numeros_internos(self):
        conexion = sqlite3.connect("cootransol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_interno FROM Vehiculos")
        numeros_internos = cursor.fetchall()
        conexion.close()
        return [str(nro[0]) for nro in numeros_internos]

    def actualizar_placa_vehiculo(self, event):
        nro_interno = self.nro_interno_var.get()
        if nro_interno:
            conexion = sqlite3.connect("cootransol.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT placa FROM Vehiculos WHERE nro_interno = ?", (nro_interno,))
            resultado = cursor.fetchone()
            conexion.close()
            if resultado:
                self.placa_var.set(resultado[0])
            else:
                self.placa_var.set("No encontrado")
# Inicializar la ventana de inicio de sesión
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

