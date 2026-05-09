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