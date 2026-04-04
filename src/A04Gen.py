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
        import csv
        header = HEADER(TransactionType="A04")
        data = []
        try:
            # Read PO data
            with open('A04PO.csv', newline='', encoding='utf-8-sig') as po_file:
                po_reader = csv.DictReader(po_file)
                po_rows = [row for row in po_reader if str(row.get('SELECTED', '')).strip() == '1']

            # Read Component data
            with open('A04POComponent.csv', newline='', encoding='utf-8-sig') as comp_file:
                comp_reader = csv.DictReader(comp_file)
                comp_rows = [row for row in comp_reader if str(row.get('SELECTED', '')).strip() == '1']

            for po_row in po_rows:
                row_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in po_row.items()}
                row_data = {k: v for k, v in row_data.items() if k != 'SELECTED' and v not in (None, '', ' ')}
                try:
                    comp_list = []
                    for comp_row in comp_rows:
                        comp_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in comp_row.items()}
                        comp_data = {k: v for k, v in comp_data.items() if k != 'SELECTED' and v not in (None, '', ' ')}
                        comp_list.append(Component(**comp_data))
                    row_data['Components'] = comp_list
                    a04_data = A04Data(**row_data)
                    data.append(a04_data)
                    self.log(f"Loaded PO: {a04_data.PurchaseOrderNo if hasattr(a04_data, 'PurchaseOrderNo') else ''}")
                except Exception as e:
                    self.log(f"Error loading PO row: {e}")
            self.a04 = A04(Header=header, DataS=data)
            self.log(f"Data loaded from CSV successfully! ({len(data)} records)")
        except Exception as e:
            self.log(f"Error reading CSV: {e}")
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
        self.log('Appending to A03TO.csv for A03 generation (new format)...')
        import csv
        import os
        try:
            header = ["SELECTED","MaterialCode","ControlNo","GRTF_Quantity","QMNo_ofContainers","Quantity","UOM","SourceLocation","TargetLocation","ExpiryDate"]
            rows = []
            for component in self.a04.DataS[0].Components:
                row = {
                    "SELECTED": 1,
                    "MaterialCode": getattr(component, "ComponentCode", ""),
                    "ControlNo": getattr(component, "ControlNo", ""),
                    "GRTF_Quantity": getattr(component, "GRTF_Quantity", ""),
                    "QMNo_ofContainers": getattr(component, "QMNo_ofContainers", ""),
                    "Quantity": getattr(component, "Target", ""),
                    "UOM": getattr(component, "ComponentUOM", ""),
                    "SourceLocation": getattr(component, "SourceLocation", ""),
                    "TargetLocation": getattr(component, "StorageLocation", ""),
                    "ExpiryDate": getattr(component, "ExpiryDate", "")
                }
                rows.append(row)
            # Check if file exists and has content
            file_exists = os.path.isfile('A03TO.csv')
            existing_rows = []
            if file_exists:
                with open('A03TO.csv', 'r', encoding='utf-8-sig') as f:
                    reader = list(csv.DictReader(f))
                    if reader:
                        # Set all existing SELECTED to 0
                        for r in reader:
                            r['SELECTED'] = '0'
                        existing_rows = reader
            # Always write the header, then all rows
            with open('A03TO.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                if existing_rows:
                    writer.writerows(existing_rows)
                writer.writerows(rows)
            self.log(f"Appended {len(rows)} rows to A03TO.csv for A03 generation successfully! (existing SELECTED set to 0)")
        except Exception as e:
            self.log(f"Error appending to A03TO.csv for A03: {e}")