import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from sistema_cootransol import Administrador, Despachador  # Importar las clases del sistema
from DataBase import agregar_conductor, agregar_vehiculo, eliminar_vehiculo_db, eliminar_conductor_db  # Importar funciones para base de datos
import sqlite3
# Ventana de inicio de sesión
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - COOTRANSOL")

        # Etiquetas y entradas para el usuario y la contraseña
        self.label_user = tk.Label(root, text="Usuario")
        self.label_user.pack(pady=5)

        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        self.label_pass = tk.Label(root, text="Contraseña")
        self.label_pass.pack(pady=5)

        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        # Botón de inicio de sesión
        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack(pady=20)

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # Suponemos que el administrador tiene el usuario 'admin' y el despachador tiene 'despachador'
        if username == "admin" and password == "adminpass":
            messagebox.showinfo("Login exitoso", "Bienvenido Administrador")
            self.root.destroy()  # Cerrar la ventana de login
            admin = Administrador(username, password, "admin")
            AdminWindow(admin)  # Abrir la ventana de administración pasando el objeto 'admin'
        elif username == "despachador" and password == "despachadorpass":
            messagebox.showinfo("Login exitoso", "Bienvenido Despachador")
            self.root.destroy()  # Cerrar la ventana de login
            despachador = Despachador(username, password, "despachador")
            DespachadorWindow(despachador)  # Abrir la ventana del despachador pasando el objeto 'despachador'
        else:
            messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")
# Función para cargar todos los conductores en la tabla de la interfaz
# Ventana para el Administrador
class AdminWindow:
    def __init__(self, admin):
        self.admin = admin
        self.admin_root = tk.Tk()
        self.admin_root.title("Sistema de Gestión de Transporte - COOTRANSOL")

        # Crear Notebook (pestañas)
        self.tab_control = ttk.Notebook(self.admin_root)

        # Pestaña de Datos del Conductor
        self.tab_conductor = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_conductor, text="Datos del Conductor")

        # Pestaña de Datos del Vehículo
        self.tab_vehiculo = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_vehiculo, text="Datos del Vehículo")

        # Empaquetar las pestañas
        self.tab_control.pack(expand=1, fill="both")

        # Configuración de cada pestaña
        self.setup_conductor_tab()
        self.setup_vehiculo_tab()

        self.admin_root.mainloop()

    def setup_conductor_tab(self):
        # Campo de búsqueda por identificación
        label_busqueda = tk.Label(self.tab_conductor, text="Buscar por Identificación:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_conductor = tk.Entry(self.tab_conductor)
        self.entry_busqueda_conductor.grid(row=0, column=1, padx=10, pady=10)

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_conductor, text="Buscar", command=self.filtrar_conductor)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar conductores
        self.tree_conductores = ttk.Treeview(self.tab_conductor, columns=("Identificacion", "Nombre", "Licencia"), show="headings")
        self.tree_conductores.heading("Identificacion", text="Identificacion")
        self.tree_conductores.heading("Nombre", text="Nombre")
        self.tree_conductores.heading("Licencia", text="Vigencia Licencia")
        self.tree_conductores.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Botón para agregar conductor
        btn_agregar_conductor = tk.Button(self.tab_conductor, text="Agregar Conductor", command=self.abrir_agregar_conductor)
        btn_agregar_conductor.grid(row=2, column=0, columnspan=3, pady=10)

        # Botón para eliminar conductor
        self.btn_eliminar_conductor = tk.Button(self.tab_conductor, text="Eliminar Conductor", command=self.eliminar_conductor)
        self.btn_eliminar_conductor.grid(row=3, column=0, columnspan=3, pady=10)

        # Botón para editar conductor
        self.btn_editar_conductor = tk.Button(self.tab_conductor, text="Editar Conductor", command=self.editar_conductor)
        self.btn_editar_conductor.grid(row=4, column=0, columnspan=3, pady=10)

        self.cargar_conductores()
    def setup_vehiculo_tab(self):
        # Campo de búsqueda por placa
        label_busqueda = tk.Label(self.tab_vehiculo, text="Buscar por Placa:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_busqueda_vehiculo = tk.Entry(self.tab_vehiculo)
        self.entry_busqueda_vehiculo.grid(row=0, column=1, padx=10, pady=10)

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_vehiculo, text="Buscar", command=self.filtrar_vehiculo)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar vehículos
        self.tree_vehiculos = ttk.Treeview(self.tab_vehiculo, columns=("Nro", "Placa", "Estado", "Modelo", "SOAT", "Tarjeta", "Póliza", "Tecno"), show="headings", height=8)
        
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

        # Botón para agregar vehículo
        btn_agregar_vehiculo = tk.Button(self.tab_vehiculo, text="Agregar Vehículo", command=self.abrir_agregar_vehiculo)
        btn_agregar_vehiculo.grid(row=3, column=0, columnspan=3, pady=10)

        # Botón para eliminar vehículo
        self.btn_eliminar_vehiculo = tk.Button(self.tab_vehiculo, text="Eliminar Vehículo", command=self.eliminar_vehiculo)
        self.btn_eliminar_vehiculo.grid(row=4, column=0, columnspan=3, pady=10)

        # Botón para editar vehículo
        self.btn_editar_vehiculo = tk.Button(self.tab_vehiculo, text="Editar Vehículo", command=self.editar_vehiculo)
        self.btn_editar_vehiculo.grid(row=5, column=0, columnspan=3, pady=10)

        #Cargar info de los vehículos ya existentes
        self.cargar_vehiculos()
    
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
        entry_vigencia = tk.Entry(editar_window)
        entry_vigencia.grid(row=2, column=1, padx=10, pady=5)
        entry_vigencia.insert(0, vigencia_actual)

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

        # Retrieve current vehicle data from the table
        nro_interno = self.tree_vehiculos.item(selected_item, "values")[0]
        placa = self.tree_vehiculos.item(selected_item, "values")[1]
        estado_actual = self.tree_vehiculos.item(selected_item, "values")[2]
        modelo_actual = self.tree_vehiculos.item(selected_item, "values")[3]
        soat_actual = self.tree_vehiculos.item(selected_item, "values")[4]
        tarjeta_actual = self.tree_vehiculos.item(selected_item, "values")[5]
        poliza_actual = self.tree_vehiculos.item(selected_item, "values")[6]
        tecno_actual = self.tree_vehiculos.item(selected_item, "values")[7]

        editar_window = tk.Toplevel(self.admin_root)
        editar_window.title("Editar Vehículo")

        # Add fields for vehicle data
        tk.Label(editar_window, text="Número Interno:").grid(row=0, column=0, padx=10, pady=5)
        entry_nro_interno = tk.Entry(editar_window)
        entry_nro_interno.grid(row=0, column=1, padx=10, pady=5)
        entry_nro_interno.insert(0, nro_interno)

        tk.Label(editar_window, text="Placa:").grid(row=1, column=0, padx=10, pady=5)
        entry_placa = tk.Entry(editar_window)
        entry_placa.grid(row=1, column=1, padx=10, pady=5)
        entry_placa.insert(0, placa)

        tk.Label(editar_window, text="Estado:").grid(row=2, column=0, padx=10, pady=5)
        entry_estado = tk.Entry(editar_window)
        entry_estado.grid(row=2, column=1, padx=10, pady=5)
        entry_estado.insert(0, estado_actual)

        tk.Label(editar_window, text="Modelo:").grid(row=3, column=0, padx=10, pady=5)
        entry_modelo = tk.Entry(editar_window)
        entry_modelo.grid(row=3, column=1, padx=10, pady=5)
        entry_modelo.insert(0, modelo_actual)

        tk.Label(editar_window, text="Vigencia SOAT:").grid(row=4, column=0, padx=10, pady=5)
        entry_soat = tk.Entry(editar_window)
        entry_soat.grid(row=4, column=1, padx=10, pady=5)
        entry_soat.insert(0, soat_actual)

        tk.Label(editar_window, text="Vigencia Tarjeta:").grid(row=5, column=0, padx=10, pady=5)
        entry_tarjeta = tk.Entry(editar_window)
        entry_tarjeta.grid(row=5, column=1, padx=10, pady=5)
        entry_tarjeta.insert(0, tarjeta_actual)

        tk.Label(editar_window, text="Vigencia Póliza:").grid(row=6, column=0, padx=10, pady=5)
        entry_poliza = tk.Entry(editar_window)
        entry_poliza.grid(row=6, column=1, padx=10, pady=5)
        entry_poliza.insert(0, poliza_actual)

        tk.Label(editar_window, text="Vigencia Tecnomecánica:").grid(row=7, column=0, padx=10, pady=5)
        entry_tecno = tk.Entry(editar_window)
        entry_tecno.grid(row=7, column=1, padx=10, pady=5)
        entry_tecno.insert(0, tecno_actual)

        # Dropdown for selecting an available driver
        tk.Label(editar_window, text="Asignar Conductor:").grid(row=8, column=0, padx=10, pady=5)
        self.conductor_var = tk.StringVar()
        self.dropdown_conductor = ttk.Combobox(editar_window, textvariable=self.conductor_var, state="readonly")
        self.dropdown_conductor.grid(row=8, column=1, padx=10, pady=5)

        # Load available drivers (excluding already assigned ones)
        conductores_disponibles = self.obtener_conductores_disponibles(nro_interno)  # Pass current assigned driver ID to filter correctly
        self.dropdown_conductor["values"] = conductores_disponibles

        def guardar_cambios():
            # Gather updated data
            datos_actualizados = {
                "nro_interno": entry_nro_interno.get().strip(),
                "placa": entry_placa.get().strip(),
                "estado": entry_estado.get().strip(),
                "modelo": entry_modelo.get().strip(),
                "vigencia_soat": entry_soat.get().strip(),
                "vigencia_tarjeta": entry_tarjeta.get().strip(),
                "vigencia_poliza": entry_poliza.get().strip(),
                "vigencia_tecno": entry_tecno.get().strip()
            }
            conductor_seleccionado = self.conductor_var.get()

            # Validate fields
            if any(value == "" for value in datos_actualizados.values()) or not conductor_seleccionado:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

            # Extract the selected driver's ID
            id_conductor = conductor_seleccionado.split(" - ")[0]

            # Save changes (you should implement or update the method to save changes)
            self.guardar_cambios_vehiculo(datos_actualizados, id_conductor)
            messagebox.showinfo("Éxito", "Vehículo editado correctamente.")
            editar_window.destroy()

        btn_guardar = tk.Button(editar_window, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.grid(row=9, column=0, columnspan=2, pady=10)

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
        # Lógica para filtrar los vehículos en la base de datos y mostrar resultados en la tabla
        placa = self.entry_busqueda_vehiculo.get()
        # Aquí llamaremos a una función para buscar en la base de datos y actualizar la tabla `tree_vehiculos`
        # Ejemplo: self.tree_vehiculos.insert('', 'end', values=(placa, estado, modelo))

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
        entry_licencia = tk.Entry(agregar_window)
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
        labels = ["Número interno", "Placa", "Estado", "Modelo", "Vigencia SOAT", "Vigencia Tarjeta", "Vigencia Póliza", "Vigencia Tecnomecánica"]
        entries = {}

        # Crear entradas dinámicas
        for i, label_text in enumerate(labels):
            label = tk.Label(agregar_window, text=label_text + ":")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(agregar_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label_text] = entry

        # Dropdown para seleccionar el conductor disponible
        label_conductor = tk.Label(agregar_window, text="Asignar Conductor:")
        label_conductor.grid(row=len(labels), column=0, padx=10, pady=5)

        # Variable y dropdown para conductores disponibles
        self.conductor_var = tk.StringVar()
        self.dropdown_conductor = ttk.Combobox(agregar_window, textvariable=self.conductor_var, state="readonly")
        self.dropdown_conductor.grid(row=len(labels), column=1, padx=10, pady=5)

        # Cargar conductores disponibles con formato adecuado
        conductores_disponibles = self.obtener_conductores_disponibles()
        self.dropdown_conductor["values"] = conductores_disponibles
        #self.dropdown_conductor["values"] = [f"{conductor[0]} - {conductor[1]}" for conductor in conductores_disponibles]

        def agregar_vehiculo_callback():
            # Obtener los valores de entrada
            datos_vehiculo = {key: entry.get().strip() for key, entry in entries.items()}
            conductor_seleccionado = self.conductor_var.get()

            # Validación de campos vacíos
            if any(value == "" for value in datos_vehiculo.values()) or not conductor_seleccionado:
                messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
                return

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
        btn_guardar.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)
   
    def obtener_conductores_disponibles(self):
        try:
            # Confirma la ruta de la base de datos
            db_path = "D:/Asus/Escritorio/Psergio/cootransol.db"
            print(f"Usando la base de datos en: {db_path}")

            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            # Prueba de consulta para verificar la columna `idConductor`
            print("Ejecutando consulta para verificar conductores disponibles...")
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
        self.tab_control.add(self.tab_pagos, text="Gestionar Pagos")

        # Pestaña de Asignar Rutas
        self.tab_rutas = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_rutas, text="Asignar Ruta")

        # Empaquetar las pestañas
        self.tab_control.pack(expand=1, fill="both")

        # Configuración de cada pestaña
        self.setup_conductor_tab()
        self.setup_vehiculo_tab()
        self.setup_pagos_tab()
        self.setup_rutas_tab()

        self.despachador_root.mainloop()

    def setup_conductor_tab(self):
        # Campo de búsqueda por identificación
        label_busqueda = tk.Label(self.tab_conductor, text="Buscar por Identificación:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_conductor = tk.Entry(self.tab_conductor)
        self.entry_busqueda_conductor.grid(row=0, column=1, padx=10, pady=10)

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_conductor, text="Buscar", command=self.buscar_conductor)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar conductores
        self.tree_conductores = ttk.Treeview(self.tab_conductor, columns=("Identificacion", "Nombre", "Licencia"), show="headings")
        self.tree_conductores.heading("Identificacion", text="Identificacion")
        self.tree_conductores.heading("Nombre", text="Nombre")
        self.tree_conductores.heading("Licencia", text="Vigencia Licencia")
        self.tree_conductores.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

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
       def setup_conductor_tab(self):
        # Campo de búsqueda por identificación
        label_busqueda = tk.Label(self.tab_conductor, text="Buscar por Identificación:")
        label_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_conductor = tk.Entry(self.tab_conductor)
        self.entry_busqueda_conductor.grid(row=0, column=1, padx=10, pady=10)

        # Botón de búsqueda
        btn_buscar = tk.Button(self.tab_conductor, text="Buscar", command=self.filtrar_conductor)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar conductores
        self.tree_conductores = ttk.Treeview(self.tab_conductor, columns=("Identificacion", "Nombre", "Licencia"), show="headings")
        self.tree_conductores.heading("Identificacion", text="Identificacion")
        self.tree_conductores.heading("Nombre", text="Nombre")
        self.tree_conductores.heading("Licencia", text="Vigencia Licencia")
        self.tree_conductores.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.cargar_conductores()

    def setup_pagos_tab(self):
        # Etiquetas y campos de entrada para los pagos
        label_id_conductor = tk.Label(self.tab_pagos, text="ID del Conductor:")
        label_id_conductor.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_id_conductor_pago = tk.Entry(self.tab_pagos)
        self.entry_id_conductor_pago.grid(row=0, column=1, padx=10, pady=10)

        label_monto_pago = tk.Label(self.tab_pagos, text="Monto del Pago:")
        label_monto_pago.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_monto_pago = tk.Entry(self.tab_pagos)
        self.entry_monto_pago.grid(row=1, column=1, padx=10, pady=10)

        # Botón para gestionar el pago
        self.btn_gestionar_pago = tk.Button(self.tab_pagos, text="Gestionar Pago", bg="green", fg="white", command=self.gestionar_pago)
        self.btn_gestionar_pago.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    def setup_rutas_tab(self):
        # Etiquetas y campos de entrada para asignar rutas
        label_id_conductor = tk.Label(self.tab_rutas, text="ID del Conductor:")
        label_id_conductor.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_id_conductor_ruta = tk.Entry(self.tab_rutas)
        self.entry_id_conductor_ruta.grid(row=0, column=1, padx=10, pady=10)

        label_ruta = tk.Label(self.tab_rutas, text="Ruta a Asignar:")
        label_ruta.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_ruta = tk.Entry(self.tab_rutas)
        self.entry_ruta.grid(row=1, column=1, padx=10, pady=10)

        # Botón para asignar ruta
        self.btn_asignar_ruta = tk.Button(self.tab_rutas, text="Asignar Ruta", bg="green", fg="white", command=self.asignar_ruta)
        self.btn_asignar_ruta.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    def gestionar_pago(self):
        # Obtener los valores de los campos de pago
        id_conductor = self.entry_id_conductor_pago.get()
        monto_pago = self.entry_monto_pago.get()

        if id_conductor and monto_pago:
            # Lógica para gestionar el pago
            mensaje = self.despachador.gestionarPago(int(id_conductor), float(monto_pago))
            messagebox.showinfo("Pago Gestionado", mensaje)
        else:
            messagebox.showerror("Error", "Debe llenar todos los campos.")

    def asignar_ruta(self):
        # Obtener los valores de los campos de asignación de ruta
        id_conductor = self.entry_id_conductor_ruta.get()
        ruta = self.entry_ruta.get()

        if id_conductor and ruta:
            # Lógica para asignar la ruta
            mensaje = self.despachador.asignarRuta(int(id_conductor), ruta)
            messagebox.showinfo("Ruta Asignada", mensaje)
        else:
            messagebox.showerror("Error", "Debe llenar todos los campos.")
# Inicializar la ventana de inicio de sesión
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

