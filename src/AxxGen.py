import tkinter as tk
from tkinter import ttk, messagebox

class AxxGen(ttk.Frame):
    def __init__(self, parent, log_callback=None, color='beige'):
        super().__init__(parent)
        self.log_callback = log_callback
        self._build_ui(color)

    def log(self, message):
        if callable(self.log_callback):
            self.log_callback(message)
        else:
            print(message)

    def _build_ui(self, color):
        s = ttk.Style()
        # Use a unique style name per tab instance so tabs can have different colors.
        frame_style = f"{self.__class__.__name__}.{id(self)}.TFrame"
        s.configure(frame_style, background=color)
        self.configure(style=frame_style)
        frm = ttk.Frame(self, style=frame_style)
        frm.pack(padx=10, pady=10, fill='x')
        bExcel = ttk.Button(frm, text="Load from Excel", command=self.load_from_excel)
        bExcel.grid(row=2, column=0, columnspan=2, pady=10)
        bCopy2Clipboard = ttk.Button(frm, text="Copy XML to Clipboard", command=self.copy_to_clipboard)
        bCopy2Clipboard.grid(row=3, column=0, columnspan=2, pady=10)
