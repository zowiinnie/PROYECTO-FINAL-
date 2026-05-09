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