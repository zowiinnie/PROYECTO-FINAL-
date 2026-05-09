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
