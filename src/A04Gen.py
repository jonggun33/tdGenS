from AxxGen import AxxGen  
from Header import HEADER  
from A04 import A04,  A04Data , Component 
import openpyxl
import pyperclip
from tools import json_to_xml
from tkinter import messagebox, ttk  
from tkinter import BooleanVar
import datetime
import random


class A04Gen(AxxGen):
    def __init__(self, parent, log_callback=None, color='lightyellow'):
        super().__init__(parent, log_callback=log_callback, color=color)

    def _build_ui(self, color):
        super()._build_ui(color='lightyellow')
        self.include_to =  BooleanVar()
        ttk.Checkbutton(self, text="Generate Transfer Order (A03)", variable=self.include_to).pack(pady=5)


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
        if self.include_to.get()==True:
            self.update_excel_for_a03()  # Update Excel for A03 generation
    def update_excel_for_a03(self):
        self.log('Updating Excel for A03 generation...')
        try:
            wb = openpyxl.load_workbook('data.xlsx')
            ws = wb['A03']
            table = ws.tables['AThree']
            ref = table.ref
            for row in ws[ref][1:]:  # Skip header
                ws.cell(row=row[0].row, column=1).value = 0  # Clear SELECTED column

            start_row = ws[ref][-1][-1].row + 1  # Start after the last row of the table
            self.log(f"start_row: {start_row}")
            row_num = start_row
            for i, component in enumerate(self.a04.DataS[0].Components):  
                row_num = start_row + i
                ws.cell(row=row_num, column=1).value =1
                ws.cell(row=row_num, column=2, value=component.ComponentCode)  
                ws.cell(row=row_num, column=6, value=component.Target)
                ws.cell(row= row_num, column=9, value=component.StorageLocation)  
                ws.cell(row=row_num, column=7, value=component.ComponentUOM)  
            new_ref = f"A1:J{row_num}"  # Update the reference to include new rows (assuming 10 columns)
            print(new_ref)
            table.ref = new_ref  # Update the table reference to include new rows
            wb.save('data.xlsx')
            self.log("Excel updated for A03 generation successfully!")
        except Exception as e:
            self.log(f"Error updating Excel for A03: {e}")