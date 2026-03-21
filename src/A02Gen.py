from tkinter import ttk


class A02Gen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill='x')
        ttk.Label(frm, text="X02 Generator Coming Soon!").grid(row=0, column=0, sticky='w', pady=2)