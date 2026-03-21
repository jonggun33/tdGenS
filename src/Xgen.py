import tkinter as tk
from tkinter import ttk, messagebox
from A03Gen import A03Gen  # Assuming A03Gen is defined in A03Gen.
from A02Gen import A02Gen  # Assuming X02Gen is defined in X02Gen.py

class Xgen:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Transaction Generator")
        self.root.geometry("1100x500")
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")
        tab_A03 = A03Gen(notebook)  # Assuming A03Gen is defined in A03Gen.py
        notebook.add(tab_A03, text="A03 Transaction")
        tab_A02 = A02Gen(notebook)  # Assuming X02Gen is defined in X02Gen.py
        notebook.add(tab_A02, text="X02 Transaction")

        # Create a log window
        self.log_frame = ttk.Frame(root)
        self.log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(self.log_frame, text="Log:").pack(anchor="w")
        
        self.log_text = tk.Text(self.log_frame, height=10, width=80)
        self.log_text.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

if __name__ == "__main__":
    Xgen(tk.Tk()).root.mainloop()