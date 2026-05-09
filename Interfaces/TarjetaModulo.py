class TarjetaModulo(tk.Frame):
    def __init__(self, parent, titulo, icono, comando):
        super().__init__(parent, bg="white", width=180, height=120, highlightbackground="#DDD", highlightthickness=1, cursor="hand2")
        self.pack_propagate(False)
        tk.Label(self, text=icono, font=("Arial", 28), bg="white").pack(pady=(15, 5))
        tk.Label(self, text=titulo, font=("Arial", 11, "bold"), bg="white").pack()
        self.bind("<Button-1>", lambda e: comando())
        for widget in self.winfo_children():
            widget.bind("<Button-1>", lambda e: comando())