# IMPORTACIÓN DE LIBRERÍAS
# Librerías para la interfaz gráfica
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Librería para la base de datos SQLite
import sqlite3

# Librería para manejar fechas
from datetime import datetime

# COLORES DEL SISTEMA
# Diccionario de colores utilizados en la interfaz
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

# CLASE BASE DE DATOS
# Clase encargada de crear y conectar la base de datos
class DatabaseManager:

    # Método constructor
    def __init__(self, db_name="tienda.db"):
        self.db_name = db_name
        self.iniciar_base_datos()

    # Método para conectar con SQLite
    def conectar(self):
        return sqlite3.connect(self.db_name)

    # Método que crea las tablas del sistema
    def iniciar_base_datos(self):

        with self.conectar() as conn:
            cursor = conn.cursor()

            # Tabla de usuarios
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE,
                clave TEXT,
                tipo TEXT
            )""")

            # Tabla de productos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                stock INTEGER,
                caducidad TEXT
            )""")

            # Tabla de promociones
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS promociones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )""")

            # Crear usuario administrador si no existe
            admin = cursor.execute(
                "SELECT * FROM usuarios WHERE nombre='admin'"
            ).fetchone()

            if not admin:
                cursor.execute("""
                INSERT INTO usuarios(nombre, clave, tipo)
                VALUES('admin','1234','Administrador')
                """)

            conn.commit()

# CLASE USUARIO
# Clase encargada de administrar usuarios
class USUARIO:

    # Método constructor
    def __init__(self, db):
        self.db = db

    # Método para registrar usuarios
    def registrar_usuario(self, nombre, clave, tipo):

        with self.db.conectar() as conn:
            conn.execute(
                "INSERT INTO usuarios(nombre, clave, tipo) VALUES(?,?,?)",
                (nombre, clave, tipo)
            )
            conn.commit()

    # Método para eliminar usuarios
    def eliminar_usuario(self, uid):

        with self.db.conectar() as conn:
            conn.execute(
                "DELETE FROM usuarios WHERE id=?",
                (uid,)
            )
            conn.commit()

    # Método para iniciar sesión
    def iniciar_sesion(self, nombre, clave):

        with self.db.conectar() as conn:
            return conn.execute(
                "SELECT * FROM usuarios WHERE nombre=? AND clave=?",
                (nombre, clave)
            ).fetchone()

# CLASE PRODUCTO
# Clase encargada de administrar productos
class PRODUCTO:

    # Método constructor
    def __init__(self, db):
        self.db = db

    # Método para agregar productos
    def agregar_producto(self, nombre, stock, caducidad):

        with self.db.conectar() as conn:
            conn.execute(
                "INSERT INTO productos(nombre, stock, caducidad) VALUES(?,?,?)",
                (nombre, stock, caducidad)
            )
            conn.commit()

    # Método para eliminar productos
    def eliminar_producto(self, pid):

        with self.db.conectar() as conn:
            conn.execute(
                "DELETE FROM productos WHERE id=?",
                (pid,)
            )
            conn.commit()

    # Método para verificar el estado de caducidad
    def verificar_estado(self, fecha):

        hoy = datetime.now()

        try:
            dias = (datetime.strptime(fecha, "%Y-%m-%d") - hoy).days

            # Producto ya caducado
            if dias < 0:
                return "🔴 CADUCADO"

            # Producto próximo a caducar
            elif dias <= 7:
                return "🟠 POR CADUCAR"

            # Producto vigente
            else:
                return "🟢 VIGENTE"

        except:
            return "SIN FECHA"

# CLASE INVENTARIO
# Clase encargada de mostrar productos
class INVENTARIO:

    # Método constructor
    def __init__(self, db):
        self.db = db

    # Método para mostrar todos los productos
    def mostrar_productos(self):

        with self.db.conectar() as conn:
            return conn.execute(
                "SELECT * FROM productos"
            ).fetchall()

    # Método para buscar productos por nombre
    def buscar_producto(self, nombre):

        with self.db.conectar() as conn:
            return conn.execute(
                "SELECT * FROM productos WHERE nombre LIKE ?",
                (f"%{nombre}%",)
            ).fetchall()

# CLASE ALERTA
# Clase encargada de generar alertas
class ALERTA:

    # Método constructor
    def __init__(self, db):
        self.db = db

    # Método para generar alertas
    def generar_alerta(self):

        alertas = []

        hoy = datetime.now()

        # Stock mínimo permitido
        UMBRAL_STOCK = 5

        with self.db.conectar() as conn:
            productos = conn.execute(
                "SELECT nombre, stock, caducidad FROM productos"
            ).fetchall()

        # Recorrer productos
        for nombre, stock, fecha in productos:

            # Verificar stock bajo
            if stock <= UMBRAL_STOCK:
                alertas.append(
                    f"📦 STOCK BAJO: {nombre} (Quedan {stock})"
                )

            # Verificar caducidad
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

# CLASE PROMOCIÓN
# Clase encargada de administrar promociones
class PROMOCION:

    # Método constructor
    def __init__(self, db):
        self.db = db

    # Método para crear promociones
    def crear_promocion(self, nombre):

        with self.db.conectar() as conn:
            conn.execute(
                "INSERT INTO promociones(nombre) VALUES(?)",
                (nombre,)
            )
            conn.commit()

    # Método para eliminar promociones
    def eliminar_promocion(self, pid):

        with self.db.conectar() as conn:
            conn.execute(
                "DELETE FROM promociones WHERE id=?",
                (pid,)
            )
            conn.commit()

# CLASE TARJETA MÓDULO
# Clase para crear tarjetas del menú
class TarjetaModulo(tk.Frame):

    # Método constructor
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

        # Icono de la tarjeta
        tk.Label(
            self,
            text=icono,
            font=("Arial", 28),
            bg="white"
        ).pack(pady=(15, 5))

        # Título de la tarjeta
        tk.Label(
            self,
            text=titulo,
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack()

        # Evento de clic
        self.bind("<Button-1>", lambda e: comando())

        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda e: comando())

# CLASE PRINCIPAL SISTEMA
# Clase principal del sistema
class SISTEMA:

    # Método constructor
    def __init__(self, root):

        self.root = root

        # Inicialización de clases
        self.db = DatabaseManager()
        self.usuario_modelo = USUARIO(self.db)
        self.producto_modelo = PRODUCTO(self.db)
        self.inventario_modelo = INVENTARIO(self.db)
        self.alerta_modelo = ALERTA(self.db)
        self.promocion_modelo = PROMOCION(self.db)

        # Configuración principal
        self.root.title("Manzana Loca - Gestión de Tienda")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORES["fondo"])

        # Contenedor principal
        self.contenedor = tk.Frame(
            self.root,
            bg=COLORES["fondo"]
        )

        self.contenedor.pack(
            fill="both",
            expand=True
        )

        # Mostrar login
        self.pantalla_login()

# EJECUCIÓN PRINCIPAL
# Punto de inicio del programa
if __name__ == "__main__":

    # Crear ventana principal
    root = tk.Tk()

    # Ejecutar sistema
    app = SISTEMA(root)

    # Mantener ventana abierta
    root.mainloop()