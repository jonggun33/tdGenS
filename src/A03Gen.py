import tkinter as tk
from tkinter import ttk, messagebox
from model.A03 import A03  # Assuming A03 is defined in model/A03.py

class A03Gen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill='x')
        ttk.Label(frm, text="Transaction ID:").grid(row=0, column=0)
        ttk.Label(frm, text="TransferOrderNo:").grid(row=1, column=0)

        headings = ['ItemNo', 'MAT_CODE', 'CONTROL_NO', 'CTR_QTY', 'NoContainers', 'Quantity',
                    'UOM', 'SLOC_FROM', 'SLOC_TO','ExpiryDate']
        tree_frame = ttk.Frame(frm)
        tree_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=2)
        columns = headings
        tree = ttk.Treeview(tree_frame, columns=columns, height=10, show='headings')
        for i, heading in enumerate(headings):
            tree.heading(heading, text=heading)
            tree.column(heading, width=100) # Set a default width for all columns   
        tree.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscroll=scrollbar.set)
        rows = 5
        for i in range(rows):
            tree.insert('', 'end', values=[''] * len(headings))
        
