from tkinter import ttk


class A02Gen(ttk.Frame):
    def __init__(self, parent, log_callback=None):
        super().__init__(parent)
        self.log_callback = log_callback
        self._build_ui()

    def log(self, message):
        if callable(self.log_callback):
            self.log_callback(message)
        else:
            print(message)

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill='x')
        ttk.Label(frm, text="X02 Generator Coming Soon!").grid(row=0, column=0, sticky='w', pady=2)