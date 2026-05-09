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
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                stock INTEGER,
                caducidad TEXT
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS promociones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )""")
            
            admin = cursor.execute("SELECT * FROM usuarios WHERE nombre='admin'").fetchone()
            if not admin:
                cursor.execute("INSERT INTO usuarios(nombre, clave, tipo) VALUES('admin','1234','Administrador')")
            conn.commit()

class USUARIO:
    def __init__(self, db):
        self.db = db

    def registrar_usuario(self, nombre, clave, tipo):
        with self.db.conectar() as conn:
            conn.execute("INSERT INTO usuarios(nombre, clave, tipo) VALUES(?,?,?)", (nombre, clave, tipo))
            conn.commit()

    def eliminar_usuario(self, uid):
        with self.db.conectar() as conn:
            conn.execute("DELETE FROM usuarios WHERE id=?", (uid,))
            conn.commit()

    def iniciar_sesion(self, nombre, clave):
        with self.db.conectar() as conn:
            return conn.execute("SELECT * FROM usuarios WHERE nombre=? AND clave=?", (nombre, clave)).fetchone()

class PRODUCTO:
    def __init__(self, db):
        self.db = db

    def agregar_producto(self, nombre, stock, caducidad):
        with self.db.conectar() as conn:
            conn.execute("INSERT INTO productos(nombre, stock, caducidad) VALUES(?,?,?)", (nombre, stock, caducidad))
            conn.commit()

    def eliminar_producto(self, pid):
        with self.db.conectar() as conn:
            conn.execute("DELETE FROM productos WHERE id=?", (pid,))
            conn.commit()

    def verificar_estado(self, fecha):
        hoy = datetime.now()
        try:
            dias = (datetime.strptime(fecha, "%Y-%m-%d") - hoy).days
            if dias < 0: return "🔴 CADUCADO"
            elif dias <= 7: return "🟠 POR CADUCAR"
            else: return "🟢 VIGENTE"
        except:
            return "SIN FECHA"

class INVENTARIO:
    def __init__(self, db):
        self.db = db

    def mostrar_productos(self):
        with self.db.conectar() as conn:
            return conn.execute("SELECT * FROM productos").fetchall()

    def buscar_producto(self, nombre):
        with self.db.conectar() as conn:
            return conn.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",)).fetchall()

class ALERTA:
    def __init__(self, db):
        self.db = db

    def generar_alerta(self):
        alertas = []
        hoy = datetime.now()
        UMBRAL_STOCK = 5 

        with self.db.conectar() as conn:
            productos = conn.execute("SELECT nombre, stock, caducidad FROM productos").fetchall()

        for nombre, stock, fecha in productos:
            
            if stock <= UMBRAL_STOCK:
                alertas.append(f"📦 STOCK BAJO: {nombre} (Quedan {stock})")
            
           
            try:
                dias = (datetime.strptime(fecha, "%Y-%m-%d") - hoy).days
                if dias < 0:
                    alertas.append(f"❌ {nombre} CADUCADO")
                elif dias <= 7:
                    alertas.append(f"⚠️ {nombre} vence en {dias} días")
            except:
                pass
        return alertas

class PROMOCION:
    def __init__(self, db):
        self.db = db

    def crear_promocion(self, nombre):
        with self.db.conectar() as conn:
            conn.execute("INSERT INTO promociones(nombre) VALUES(?)", (nombre,))
            conn.commit()

    def eliminar_promocion(self, pid):
        with self.db.conectar() as conn:
            conn.execute("DELETE FROM promociones WHERE id=?", (pid,))
            conn.commit()

class TarjetaModulo(tk.Frame):
    def __init__(self, parent, titulo, icono, comando):
        super().__init__(parent, bg="white", width=180, height=120, highlightbackground="#DDD", highlightthickness=1, cursor="hand2")
        self.pack_propagate(False)
        tk.Label(self, text=icono, font=("Arial", 28), bg="white").pack(pady=(15, 5))
        tk.Label(self, text=titulo, font=("Arial", 11, "bold"), bg="white").pack()
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

        self.root.title("Manzana Loca - Gestión de Tienda")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORES["fondo"])

        self.contenedor = tk.Frame(self.root, bg=COLORES["fondo"])
        self.contenedor.pack(fill="both", expand=True)
        self.pantalla_login()

    def limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def pantalla_login(self):
        self.limpiar()
        frame = tk.Frame(self.contenedor, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🍎", font=("Arial", 60), bg="white").pack()
        tk.Label(frame, text="MANZANA LOCA", font=("Arial", 22, "bold"), bg="white", fg=COLORES["primario"]).pack(pady=10)
        
        tk.Label(frame, text="Usuario", bg="white").pack(anchor="w")
        self.ent_usuario = tk.Entry(frame, width=30)
        self.ent_usuario.pack(pady=5)
        
        tk.Label(frame, text="Contraseña", bg="white").pack(anchor="w")
        self.ent_clave = tk.Entry(frame, width=30, show="●")
        self.ent_clave.pack(pady=5)

        tk.Button(frame, text="Entrar", bg=COLORES["primario"], fg="white", width=25, command=self.validar_login).pack(pady=15)

    def validar_login(self):
        usuario = self.usuario_modelo.iniciar_sesion(self.ent_usuario.get(), self.ent_clave.get())
        if usuario: self.menu_principal()
        else: messagebox.showerror("Error", "Credenciales incorrectas")

    def menu_principal(self):
        self.limpiar()
        top = tk.Frame(self.contenedor, bg=COLORES["primario"], height=60)
        top.pack(fill="x")
        tk.Label(top, text="🍎 Panel Administrativo", bg=COLORES["primario"], fg="white", font=("Arial", 16, "bold")).pack(side="left", padx=20)
        tk.Button(top, text="Cerrar Sesión", bg="#B03A2E", fg="white", command=self.pantalla_login).pack(side="right", padx=20, pady=10)

        grid = tk.Frame(self.contenedor, bg=COLORES["fondo"])
        grid.pack(pady=50)

        modulos = [
            ("Inventario", "📦", self.ventana_inventario),
            ("Agregar Producto", "➕", self.ventana_agregar_producto),
            ("Usuarios", "👥", self.ventana_usuarios),
            ("Promociones", "🏷️", self.ventana_promociones),
            ("Alertas", "⚠️", self.ventana_alertas)
        ]

        for i, (titulo, icono, comando) in enumerate(modulos):
            TarjetaModulo(grid, titulo, icono, comando).grid(row=i//3, column=i%3, padx=20, pady=20)

    def ventana_inventario(self):
        self.limpiar()
        tk.Label(self.contenedor, text="Inventario de Productos", font=("Arial", 20, "bold"), bg=COLORES["fondo"]).pack(pady=15)
        
        buscador = tk.Entry(self.contenedor, width=40)
        buscador.pack(pady=10)
        buscador.insert(0, "Buscar producto...")

        columnas = ("ID", "Producto", "Stock", "Caducidad", "Estado")
        tree = ttk.Treeview(self.contenedor, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        def cargar(filtro=""):
            for item in tree.get_children(): tree.delete(item)
            productos = self.inventario_modelo.buscar_producto(filtro) if filtro and filtro != "Buscar producto..." else self.inventario_modelo.mostrar_productos()
            for p in productos:
                estado = self.producto_modelo.verificar_estado(p[3])
                tree.insert("", tk.END, values=(p[0], p[1], p[2], p[3], estado))

        cargar()
        buscador.bind("<KeyRelease>", lambda e: cargar(buscador.get()))

        botones = tk.Frame(self.contenedor, bg=COLORES["fondo"])
        botones.pack(pady=10)

        tk.Button(botones, text="Eliminar Seleccionado", bg="red", fg="white", 
                  command=lambda: [self.producto_modelo.eliminar_producto(tree.item(tree.selection()[0])['values'][0]), cargar()] if tree.selection() else None).pack(side="left", padx=10)
        tk.Button(botones, text="Regresar", command=self.menu_principal).pack(side="left", padx=10)

    def ventana_agregar_producto(self):
        self.limpiar()
        frame = tk.Frame(self.contenedor, bg="white", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Nuevo Producto", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text="Nombre:", bg="white").pack(anchor="w")
        e1 = tk.Entry(frame, width=35); e1.pack(pady=5)
        tk.Label(frame, text="Cantidad (Stock):", bg="white").pack(anchor="w")
        e2 = tk.Entry(frame, width=35); e2.pack(pady=5)
        tk.Label(frame, text="Fecha Caducidad (AAAA-MM-DD):", bg="white").pack(anchor="w")
        e3 = tk.Entry(frame, width=35); e3.pack(pady=5)

        def guardar():
            if e1.get() and e2.get():
                self.producto_modelo.agregar_producto(e1.get(), e2.get(), e3.get())
                messagebox.showinfo("Éxito", "Producto registrado")
                self.menu_principal()
            else: messagebox.showwarning("Atención", "Nombre y Stock son obligatorios")

        tk.Button(frame, text="Guardar", bg=COLORES["secundario"], fg="white", command=guardar).pack(pady=10, fill="x")
        tk.Button(frame, text="Cancelar", command=self.menu_principal).pack(fill="x")

    def ventana_usuarios(self):
        self.limpiar()
        tk.Label(self.contenedor, text="Gestión de Usuarios", font=("Arial", 20, "bold"), bg=COLORES["fondo"]).pack(pady=15)
        tree = ttk.Treeview(self.contenedor, columns=("ID", "Usuario", "Tipo"), show="headings")
        for col in ("ID", "Usuario", "Tipo"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        def cargar_u():
            for item in tree.get_children(): tree.delete(item)
            with self.db.conectar() as conn:
                for u in conn.execute("SELECT id, nombre, tipo FROM usuarios").fetchall():
                    tree.insert("", tk.END, values=u)
        cargar_u()

        botones = tk.Frame(self.contenedor, bg=COLORES["fondo"])
        botones.pack(pady=10)
        
        tk.Button(botones, text="Agregar Empleado", bg=COLORES["secundario"], fg="white", 
                  command=lambda: [self.usuario_modelo.registrar_usuario(simpledialog.askstring("U", "Nombre"), simpledialog.askstring("P", "Clave"), "Empleado"), cargar_u()]).pack(side="left", padx=5)
        tk.Button(botones, text="Regresar", command=self.menu_principal).pack(side="left", padx=5)

    def ventana_promociones(self):
        self.limpiar()
        tk.Label(self.contenedor, text="Promociones Activas", font=("Arial", 20, "bold"), bg=COLORES["fondo"]).pack(pady=15)
        
        btn_frame = tk.Frame(self.contenedor, bg=COLORES["fondo"])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Nueva Promoción", bg=COLORES["secundario"], fg="white", command=self.crear_promocion).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Regresar", command=self.menu_principal).pack(side="left", padx=10)

        lista_frame = tk.Frame(self.contenedor, bg=COLORES["fondo"])
        lista_frame.pack(fill="both", expand=True, padx=50)

        with self.db.conectar() as conn:
            for pid, nombre in conn.execute("SELECT * FROM promociones").fetchall():
                f = tk.Frame(lista_frame, bg="white", pady=5, padx=10, highlightthickness=1, highlightbackground="#EEE")
                f.pack(fill="x", pady=2)
                tk.Label(f, text=f"🎉 {nombre}", bg="white", font=("Arial", 11)).pack(side="left")
                tk.Button(f, text="X", bg="red", fg="white", command=lambda i=pid: [self.promocion_modelo.eliminar_promocion(i), self.ventana_promociones()]).pack(side="right")

    def crear_promocion(self):
        p = simpledialog.askstring("Promoción", "Escribe el texto de la promoción:")
        if p:
            self.promocion_modelo.crear_promocion(p)
            self.ventana_promociones()

    def ventana_alertas(self):
        self.limpiar()
        tk.Label(self.contenedor, text="⚠️ Panel de Alertas Críticas", font=("Arial", 20, "bold"), bg=COLORES["fondo"]).pack(pady=15)
        
        alert_container = tk.Frame(self.contenedor, bg="white", padx=20, pady=20)
        alert_container.pack(fill="both", expand=True, padx=40, pady=10)

        alertas = self.alerta_modelo.generar_alerta()
        
        if alertas:
            for msg in alertas:
                # Color naranja para stock, rojo para caducidad
                color = COLORES["naranja"] if "STOCK" in msg else COLORES["rojo"]
                tk.Label(alert_container, text=msg, bg="white", fg=color, font=("Arial", 12, "bold"), pady=3).pack(anchor="w")
        else:
            tk.Label(alert_container, text="✅ No hay alertas pendientes", bg="white", font=("Arial", 12)).pack()

        tk.Button(self.contenedor, text="Regresar", bg=COLORES["primario"], fg="white", command=self.menu_principal).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SISTEMA(root)
    root.mainloop()