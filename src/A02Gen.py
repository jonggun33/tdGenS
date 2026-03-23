from AxxGen import AxxGen  # Assuming AxxGen is defined in AxxGen.py
from Header import HEADER  # Assuming Header is defined in model/Header.py
from A02 import A02, A02Data  # Assuming A02 is defined in
import openpyxl
import pyperclip
from tools import json_to_xml
from tkinter import messagebox  


class A02Gen(AxxGen):
    def __init__(self, parent, log_callback=None):
        super().__init__(parent, log_callback=log_callback)

    def load_from_excel(self):
        header = HEADER(TransactionType="A02")
        data = []
        # Load data from excel
        wb = openpyxl.load_workbook('data.xlsx')
        ws = wb['A02']
        table = ws.tables['ATwo']
        ref = table.ref
        cols = [cell.value for cell in ws[ref][0]]  # Get column headers
        for row in ws[ref][1:]:  # Skip header
            row_data = {cols[i]: cell.value for i, cell in enumerate(row)}
            if row_data.get('SELECTED', '') != 1:
                continue  # Skip rows that are not selected:
            # Convert numeric values to strings
            row_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in row_data.items()}
            # Remove SELECTED column and empty values
            row_data = {k: v for k, v in row_data.items() if k != 'SELECTED' and v is not None}
            try:
                a02_data = A02Data(**row_data)
                data.append(a02_data)
                self.log(f"Loaded: {a02_data.MaterialCode}")
            except Exception as e:
                self.log(f"Error loading row: {e}")
        self.a02 = A02(Header=header, DataS=data)
        self.log(f"Data loaded from Excel successfully! ({len(data)} records)")     
    def copy_to_clipboard(self):
        if self.a02 is None:
            self.log("Error: No A02 data loaded. Please load from Excel first.")
            messagebox.showerror("Error", "No data loaded")
            return
        try:
            self.log("Generating XML...")
            xml_string = json_to_xml(self.a02.model_dump(), root_name="TransactionRequest")
            pyperclip.copy(xml_string)
            self.log("XML copied to clipboard successfully!")
            messagebox.showinfo("Success", "XML data copied to clipboard!")
        except Exception as e:
            self.log(f"Error generating XML: {e}")
            messagebox.showerror("Error", f"Failed to generate XML: {e}")
