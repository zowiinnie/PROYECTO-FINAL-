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
