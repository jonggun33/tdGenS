import tkinter as tk
from tkinter import ttk 
from DispLabel import  DispLabel
from LabelUI import MSLabel  
from LabelUI import LabelUI  
from HalbLabel import HalbLabel
from CleaningLabel import CleaningLabel
from MSLabel import MSLabel  
import sys

class QrBar:
    def __init__(self, root, ms_file, disp_file, cleaning_file, halb_file):
        self.root = root
        self.root.title("Barcode/QR Code Generator")
        self.root.geometry("900x750")
        saved_dir = "saved/"
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")
        tab_msl = LabelUI(notebook, MSLabel, file_path=saved_dir + ms_file)  
        notebook.add(tab_msl, text="Material Status Label")
        tab_disp = LabelUI(notebook, DispLabel, file_path=saved_dir + disp_file)
        notebook.add(tab_disp, text="Dispensing Label")
        tab_cleaning = LabelUI(notebook, CleaningLabel, file_path=saved_dir + cleaning_file)
        notebook.add(tab_cleaning, text="Cleaning Label")
        tab_halb = LabelUI(notebook, HalbLabel, file_path=saved_dir + halb_file)
        notebook.add(tab_halb, text="Halb Label")



if __name__ == "__main__":
    if len(sys.argv) == 5:
        ms_file = sys.argv[1]
        disp_file = sys.argv[2]
        cleaning_file = sys.argv[3]
        halb_file = sys.argv[4]
    else:
        ms_file = "ms_labels.csv"
        disp_file = "disp_labels.csv"
        cleaning_file = "cleaning_labels.csv"
        halb_file = "halb_labels.csv"
    existing_root = tk._default_root
    if existing_root is None:
        root = tk.Tk()
        QrBar(root, ms_file, disp_file, cleaning_file, halb_file)
        root.mainloop()
    else:
        popup = tk.Toplevel(existing_root)
        QrBar(popup, ms_file, disp_file, cleaning_file, halb_file)
