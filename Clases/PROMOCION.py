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