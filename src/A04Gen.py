from AxxGen import AxxGen  # Assuming AxxGen is defined in AxxGen.py
from model.Header import HEADER  # Assuming Header is defined in model/Header.py
from model.A04 import A04,  A04Data , Component # Assuming A04  is defined
import openpyxl
import pyperclip
from model.tools import json_to_xml
from tkinter import messagebox  

class A04Gen(AxxGen):
    def __init__(self, parent, log_callback=None):
        super().__init__(parent, log_callback=log_callback)

    def load_from_excel(self):
        header = HEADER(TransactionType="A04")
        data = []
        # Load data from excel
        wb = openpyxl.load_workbook('data.xlsx')
        ws = wb['A04']
        tablePO = ws.tables['PO']
        tableComponent = ws.tables['Component']
        refPO = tablePO.ref
        refComponent = tableComponent.ref
        colsPO = [cell.value for cell in ws[refPO][0]]  # Get column headers for PO
        colsComponent = [cell.value for cell in ws[refComponent][0]]  # Get column headers for Component
        for row in ws[refPO][1:]:  # Skip header
            row_data = {colsPO[i]: cell.value for i, cell in enumerate(row)}
            if row_data.get('SELECTED', '') != 1:
                continue  # Skip rows that are not selected:
            # Convert numeric values to strings
            row_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in row_data.items()}
            # Remove SELECTED column and empty values
            row_data = {k: v for k, v in row_data.items() if k != 'SELECTED' and v is not None}
            try:
                comp_list = []
                for comp_row in ws[refComponent][1:]:  # Skip header for Component
                    comp_data = {colsComponent[i]: cell.value for i, cell in enumerate(comp_row)}
                    if comp_data.get('SELECTED', '') != 1:
                        continue  # Skip rows that are not selected:
                    # Convert numeric values to strings
                    comp_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in comp_data.items()}
                    # Remove SELECTED column and empty values
                    comp_data = {k: v for k, v in comp_data.items() if k != 'SELECTED' and v is not None}
                    comp_list.append(Component(**comp_data))
                print(comp_list)
                row_data['Components'] = comp_list
                a04_data = A04Data(**row_data)
                print(a04_data)
                data.append(a04_data)
                self.log(f"Loaded PO: {a04_data.PurchaseOrderNo}")
            except Exception as e:
                self.log(f"Error loading PO row: {e}")  
        self.a04 = A04(Header=header, DataS=data)
        self.log(f"Data loaded from Excel successfully! ({len(data)} records)") 
    def copy_to_clipboard(self):
        if self.a04 is None:
            self.log("Error: No A04 data loaded. Please load from Excel first.")
            messagebox.showerror("Error", "No data loaded")
            return
        try:
            self.log("Generating XML...")
            xml_string = json_to_xml(self.a04.model_dump(), root_name="TransactionRequest")
            pyperclip.copy(xml_string)
            self.log("XML copied to clipboard successfully!")
            messagebox.showinfo("Success", "XML data copied to clipboard!")
        except Exception as e:
            self.log(f"Error generating XML: {e}")
            messagebox.showerror("Error", f"Failed to generate XML: {e}")