import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

COLORES = {
    "fondo": "#F9F4E8",
    "primario": "#D94A38",
    "secundario": "#7A8450",
    "acento": "#E9C46A",
    "texto": "#2F2F2F",
    "blanco": "#FFFFFF",
    "rojo": "#E76F51",
    "naranja": "#F4A261"
}

class DatabaseManager:

    def __init__(self, db_name="tienda.db"):
        self.db_name = db_name
        self.iniciar_base_datos()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def iniciar_base_datos(self):

        with self.conectar() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE,
                clave TEXT,
                tipo TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                stock INTEGER,
                caducidad TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS promociones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
            """)

            admin = cursor.execute(
                "SELECT * FROM usuarios WHERE nombre='admin'"
            ).fetchone()

            if not admin:

                cursor.execute("""
                INSERT INTO usuarios(nombre, clave, tipo)
                VALUES('admin','1234','Administrador')
                """)

            conn.commit()

class USUARIO:

    def __init__(self, db):
        self.db = db

    def registrar_usuario(self, nombre, clave, tipo):

        with self.db.conectar() as conn:

            conn.execute("""
            INSERT INTO usuarios(nombre, clave, tipo)
            VALUES(?,?,?)
            """, (nombre, clave, tipo))

            conn.commit()

    def eliminar_usuario(self, uid):

        with self.db.conectar() as conn:

            conn.execute(
                "DELETE FROM usuarios WHERE id=?",
                (uid,)
            )

            conn.commit()

    def iniciar_sesion(self, nombre, clave):

        with self.db.conectar() as conn:

            return conn.execute("""
            SELECT * FROM usuarios
            WHERE nombre=? AND clave=?
            """, (nombre, clave)).fetchone()

class PRODUCTO:

    def __init__(self, db):
        self.db = db

    def agregar_producto(self, nombre, stock, caducidad):

        with self.db.conectar() as conn:

            conn.execute("""
            INSERT INTO productos(nombre, stock, caducidad)
            VALUES(?,?,?)
            """, (nombre, stock, caducidad))

            conn.commit()

    def eliminar_producto(self, pid):

        with self.db.conectar() as conn:

            conn.execute(
                "DELETE FROM productos WHERE id=?",
                (pid,)
            )

            conn.commit()

    def verificar_estado(self, fecha):

        hoy = datetime.now()

        try:

            dias = (
                datetime.strptime(fecha, "%Y-%m-%d") - hoy
            ).days

            if dias < 0:
                return "🔴 CADUCADO"

            elif dias <= 7:
                return "🟠 POR CADUCAR"

            else:
                return "🟢 VIGENTE"

        except:
            return "SIN FECHA"

class INVENTARIO:

    def __init__(self, db):
        self.db = db

    def mostrar_productos(self):

        with self.db.conectar() as conn:

            return conn.execute(
                "SELECT * FROM productos"
            ).fetchall()

    def buscar_producto(self, nombre):

        with self.db.conectar() as conn:

            return conn.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ?
            """, (f"%{nombre}%",)).fetchall()


class ALERTA:

    def __init__(self, db):
        self.db = db

    def generar_alerta(self):

        alertas = []
        hoy = datetime.now()

        with self.db.conectar() as conn:

            productos = conn.execute("""
            SELECT nombre, caducidad
            FROM productos
            """).fetchall()

        for nombre, fecha in productos:

            try:

                dias = (
                    datetime.strptime(fecha, "%Y-%m-%d") - hoy
                ).days

                if dias < 0:

                    alertas.append(
                        f"❌ {nombre} CADUCADO"
                    )

                elif dias <= 7:

                    alertas.append(
                        f"⚠️ {nombre} vence en {dias} días"
                    )

            except:
                pass

        return alertas


class PROMOCION:

    def __init__(self, db):
        self.db = db

    def crear_promocion(self, nombre):

        with self.db.conectar() as conn:

            conn.execute("""
            INSERT INTO promociones(nombre)
            VALUES(?)
            """, (nombre,))

            conn.commit()

    def eliminar_promocion(self, pid):

        with self.db.conectar() as conn:

            conn.execute("""
            DELETE FROM promociones
            WHERE id=?
            """, (pid,))

            conn.commit()


class TarjetaModulo(tk.Frame):

    def __init__(self, parent, titulo, icono, comando):

        super().__init__(
            parent,
            bg="white",
            width=180,
            height=120,
            highlightbackground="#DDD",
            highlightthickness=1,
            cursor="hand2"
        )

        self.pack_propagate(False)

        tk.Label(
            self,
            text=icono,
            font=("Arial", 28),
            bg="white"
        ).pack(pady=(15, 5))

        tk.Label(
            self,
            text=titulo,
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack()

        self.bind("<Button-1>", lambda e: comando())

        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda e: comando())

class SISTEMA:

    def __init__(self, root):

        self.root = root

        self.db = DatabaseManager()

        self.usuario_modelo = USUARIO(self.db)
        self.producto_modelo = PRODUCTO(self.db)
        self.inventario_modelo = INVENTARIO(self.db)
        self.alerta_modelo = ALERTA(self.db)
        self.promocion_modelo = PROMOCION(self.db)

        self.root.title("Manzana Loca")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORES["fondo"])

        self.contenedor = tk.Frame(
            self.root,
            bg=COLORES["fondo"]
        )

        self.contenedor.pack(fill="both", expand=True)

        self.pantalla_login()

    
    def limpiar(self):

        for widget in self.contenedor.winfo_children():
            widget.destroy()

    
    def pantalla_login(self):

        self.limpiar()

        frame = tk.Frame(
            self.contenedor,
            bg="white",
            padx=40,
            pady=40
        )

        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text="🍎",
            font=("Arial", 60),
            bg="white"
        ).pack()

        tk.Label(
            frame,
            text="MANZANA LOCA",
            font=("Arial", 22, "bold"),
            bg="white",
            fg=COLORES["primario"]
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Usuario",
            bg="white"
        ).pack(anchor="w")

        self.ent_usuario = tk.Entry(frame, width=30)
        self.ent_usuario.pack(pady=5)

        tk.Label(
            frame,
            text="Contraseña",
            bg="white"
        ).pack(anchor="w")

        self.ent_clave = tk.Entry(
            frame,
            width=30,
            show="●"
        )

        self.ent_clave.pack(pady=5)

        tk.Button(
            frame,
            text="Entrar",
            bg=COLORES["primario"],
            fg="white",
            width=25,
            command=self.validar_login
        ).pack(pady=15)

    def validar_login(self):

        usuario = self.usuario_modelo.iniciar_sesion(
            self.ent_usuario.get(),
            self.ent_clave.get()
        )

        if usuario:

            self.menu_principal()

        else:

            messagebox.showerror(
                "Error",
                "Credenciales incorrectas"
            )

    
    def menu_principal(self):

        self.limpiar()

        top = tk.Frame(
            self.contenedor,
            bg=COLORES["primario"],
            height=60
        )

        top.pack(fill="x")

        tk.Label(
            top,
            text="🍎 Panel Administrativo",
            bg=COLORES["primario"],
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=20)

        tk.Button(
            top,
            text="Cerrar Sesión",
            bg="#B03A2E",
            fg="white",
            command=self.pantalla_login
        ).pack(side="right", padx=20, pady=10)

        grid = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo"]
        )

        grid.pack(pady=50)

        modulos = [
            ("Inventario", "📦", self.ventana_inventario),
            ("Agregar Producto", "➕", self.ventana_agregar_producto),
            ("Usuarios", "👥", self.ventana_usuarios),
            ("Promociones", "🏷️", self.ventana_promociones),
            ("Alertas", "⚠️", self.ventana_alertas)
        ]

        for i, (titulo, icono, comando) in enumerate(modulos):

            TarjetaModulo(
                grid,
                titulo,
                icono,
                comando
            ).grid(
                row=i//3,
                column=i%3,
                padx=20,
                pady=20
            )

    def ventana_inventario(self):

        self.limpiar()

        tk.Label(
            self.contenedor,
            text="Inventario",
            font=("Arial", 20, "bold"),
            bg=COLORES["fondo"]
        ).pack(pady=15)

        buscador = tk.Entry(
            self.contenedor,
            width=40
        )

        buscador.pack(pady=10)

        columnas = (
            "ID",
            "Producto",
            "Stock",
            "Caducidad",
            "Estado"
        )

        tree = ttk.Treeview(
            self.contenedor,
            columns=columnas,
            show="headings"
        )

        for col in columnas:

            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        def cargar(filtro=""):

            for item in tree.get_children():
                tree.delete(item)

            productos = self.inventario_modelo.buscar_producto(filtro)

            for p in productos:

                estado = self.producto_modelo.verificar_estado(p[3])

                tree.insert(
                    "",
                    tk.END,
                    values=(p[0], p[1], p[2], p[3], estado)
                )

        cargar()

        buscador.bind(
            "<KeyRelease>",
            lambda e: cargar(buscador.get())
        )

        botones = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo"]
        )

        botones.pack(pady=10)

        def eliminar_producto():

            seleccion = tree.selection()

            if not seleccion:
                return

            datos = tree.item(seleccion[0])["values"]

            self.producto_modelo.eliminar_producto(datos[0])

            cargar()

        tk.Button(
            botones,
            text="Eliminar",
            bg="red",
            fg="white",
            command=eliminar_producto
        ).pack(side="left", padx=10)

        tk.Button(
            botones,
            text="Regresar",
            command=self.menu_principal
        ).pack(side="left", padx=10)

    
    def ventana_agregar_producto(self):

        self.limpiar()

        frame = tk.Frame(
            self.contenedor,
            bg="white",
            padx=30,
            pady=30
        )

        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text="Agregar Producto",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        e1 = tk.Entry(frame, width=35)
        e1.pack(pady=5)

        e2 = tk.Entry(frame, width=35)
        e2.pack(pady=5)

        e3 = tk.Entry(frame, width=35)
        e3.insert(0, "AAAA-MM-DD")
        e3.pack(pady=5)

        def guardar():

            self.producto_modelo.agregar_producto(
                e1.get(),
                e2.get(),
                e3.get()
            )

            messagebox.showinfo(
                "Éxito",
                "Producto agregado"
            )

            self.menu_principal()

        tk.Button(
            frame,
            text="Guardar",
            bg=COLORES["secundario"],
            fg="white",
            command=guardar
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Cancelar",
            command=self.menu_principal
        ).pack()

    
    def ventana_usuarios(self):

        self.limpiar()

        tk.Label(
            self.contenedor,
            text="Gestión de Usuarios",
            font=("Arial", 20, "bold"),
            bg=COLORES["fondo"]
        ).pack(pady=15)

        columnas = (
            "ID",
            "Usuario",
            "Contraseña",
            "Tipo"
        )

        tree = ttk.Treeview(
            self.contenedor,
            columns=columnas,
            show="headings"
        )

        for col in columnas:

            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        with self.db.conectar() as conn:

            usuarios = conn.execute(
                "SELECT * FROM usuarios"
            ).fetchall()

        for u in usuarios:
            tree.insert("", tk.END, values=u)

        botones = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo"]
        )

        botones.pack(pady=10)

        def agregar_usuario():

            nombre = simpledialog.askstring(
                "Usuario",
                "Nombre"
            )

            clave = simpledialog.askstring(
                "Contraseña",
                "Clave"
            )

            if nombre and clave:

                self.usuario_modelo.registrar_usuario(
                    nombre,
                    clave,
                    "Empleado"
                )

                self.ventana_usuarios()

        def eliminar_usuario():

            seleccion = tree.selection()

            if not seleccion:
                return

            datos = tree.item(seleccion[0])["values"]

            self.usuario_modelo.eliminar_usuario(datos[0])

            self.ventana_usuarios()

        tk.Button(
            botones,
            text="Agregar Usuario",
            bg=COLORES["secundario"],
            fg="white",
            command=agregar_usuario
        ).pack(side="left", padx=10)

        tk.Button(
            botones,
            text="Eliminar Usuario",
            bg="red",
            fg="white",
            command=eliminar_usuario
        ).pack(side="left", padx=10)

        tk.Button(
            botones,
            text="Regresar",
            command=self.menu_principal
        ).pack(side="left", padx=10)

    def ventana_promociones(self):

        self.limpiar()

        tk.Label(
            self.contenedor,
            text="Promociones",
            font=("Arial", 20, "bold"),
            bg=COLORES["fondo"]
        ).pack(pady=15)

        botones = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo"]
        )

        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Agregar Promoción",
            bg=COLORES["secundario"],
            fg="white",
            command=self.crear_promocion
        ).pack(side="left", padx=10)

        tk.Button(
            botones,
            text="⬅ Regresar",
            bg=COLORES["primario"],
            fg="white",
            command=self.menu_principal
        ).pack(side="left", padx=10)

        
        frame = tk.Frame(
            self.contenedor,
            bg=COLORES["fondo"]
        )

        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            frame,
            bg=COLORES["fondo"],
            highlightthickness=0
        )

        canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(
            frame,
            orient="vertical",
            command=canvas.yview
        )

        scroll.pack(side="right", fill="y")

        contenedor_promos = tk.Frame(
            canvas,
            bg=COLORES["fondo"]
        )

        contenedor_promos.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=contenedor_promos,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scroll.set
        )

        with self.db.conectar() as conn:

            promociones = conn.execute("""
            SELECT * FROM promociones
            ORDER BY id DESC
            """).fetchall()

        if not promociones:

            tk.Label(
                contenedor_promos,
                text="No hay promociones registradas",
                bg=COLORES["fondo"],
                font=("Arial", 12)
            ).pack(pady=30)

        else:

            for pid, nombre in promociones:

                tarjeta = tk.Frame(
                    contenedor_promos,
                    bg="white",
                    padx=20,
                    pady=20,
                    highlightbackground="#DDD",
                    highlightthickness=1
                )

                tarjeta.pack(
                    fill="x",
                    padx=60,
                    pady=10
                )

                tk.Label(
                    tarjeta,
                    text=f"🎉 {nombre}",
                    bg="white",
                    font=("Arial", 13, "bold")
                ).pack(side="left")

                tk.Button(
                    tarjeta,
                    text="Eliminar",
                    bg="red",
                    fg="white",
                    command=lambda i=pid: self.eliminar_promocion(i)
                ).pack(side="right")

    def crear_promocion(self):

        promo = simpledialog.askstring(
            "Nueva Promoción",
            "Escribe la promoción:"
        )

        if promo and promo.strip() != "":

            self.promocion_modelo.crear_promocion(promo)

            messagebox.showinfo(
                "Éxito",
                "Promoción agregada correctamente"
            )

            self.ventana_promociones()

    def eliminar_promocion(self, pid):

        self.promocion_modelo.eliminar_promocion(pid)

        self.ventana_promociones()

    
    def ventana_alertas(self):

        self.limpiar()

        tk.Label(
            self.contenedor,
            text="Alertas",
            font=("Arial", 20, "bold"),
            bg=COLORES["fondo"]
        ).pack(pady=15)

        frame = tk.Frame(
            self.contenedor,
            bg="white",
            padx=20,
            pady=20
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        alertas = self.alerta_modelo.generar_alerta()

        if alertas:

            for alerta in alertas:

                tk.Label(
                    frame,
                    text=alerta,
                    bg="white",
                    font=("Arial", 12, "bold")
                ).pack(anchor="w")

        else:

            tk.Label(
                frame,
                text="No hay alertas",
                bg="white"
            ).pack()

        tk.Button(
            self.contenedor,
            text="Regresar",
            command=self.menu_principal
        ).pack(pady=10)

if __name__ == "__main__":

    root = tk.Tk()

    app = SISTEMA(root)

    root.mainloop()