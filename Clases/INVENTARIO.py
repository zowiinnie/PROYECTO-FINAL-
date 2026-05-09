class INVENTARIO:
    def __init__(self, db):
        self.db = db

    def mostrar_productos(self):
        with self.db.conectar() as conn:
            return conn.execute("SELECT * FROM productos").fetchall()

    def buscar_producto(self, nombre):
        with self.db.conectar() as conn:
            return conn.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",)).fetchall()
