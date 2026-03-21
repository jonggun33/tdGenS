import tkinter as tk
from tkinter import ttk, messagebox
import openpyxl
import random
import pyperclip
import datetime
import os
import subprocess
import csv
from model.A03 import A03, A03Header, A03Data  # Assuming A03 is defined in model/A03.py
from model.tools import json_to_xml
from qrbar import QrBar  # Assuming QrBar is defined in qrbar.py

class A03Gen(ttk.Frame):
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
        self.a03 = None
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill='x')
        ttk.Label(frm, text="Transaction ID:").grid(row=0, column=0)
        ttk.Label(frm, text="TransferOrderNo:").grid(row=1, column=0)

       # headings = ['ItemNo', 'MAT_CODE', 'CONTROL_NO', 'CTR_QTY', 'NoContainers', 'Quantity',
       #             'UOM', 'SLOC_FROM', 'SLOC_TO','ExpiryDate']
        bExcel = ttk.Button(frm, text="Load from Excel", command=self.load_from_excel)
        bExcel.grid(row=2, column=0, columnspan=2, pady=10)
        bCopy2Clipboard = ttk.Button(frm, text="Copy XML to Clipboard", command=self.copy_to_clipboard)
        bCopy2Clipboard.grid(row=3, column=0, columnspan=2, pady=10)

    def load_from_excel(self):
        header = A03Header()
        data = []
        # Load data from excel
        wb = openpyxl.load_workbook('data.xlsx')
        ws = wb['A03']
        table = ws.tables['AThree']
        ref = table.ref
        cols = [cell.value for cell in ws[ref][0]]  # Get column headers
        TONo = str(random.randint(1000000, 9999999))
        for row in ws[ref][1:]:  # Skip header
            row_data = {cols[i]: cell.value for i, cell in enumerate(row)}
            print(row_data.get('SELECTED', ''))  # Debug print to check SELECTED value
            if row_data.get('SELECTED', '') != 1:
                continue  # Skip rows that are not selected:
            # Convert numeric values to strings
            row_data = {k: str(v) if isinstance(v, (int, float)) else v for k, v in row_data.items()}
            # Remove SELECTED column and empty values
            row_data = {k: v for k, v in row_data.items() if k != 'SELECTED' and v is not None}
            row_data['TransferOrderNo'] = TONo
            row_data['TransferOrderItemNo']= str(row[0].row - 1)  # Assuming ItemNo is the first column and starts from 1
            try:
                a03_data = A03Data(**row_data)
                data.append(a03_data)
                self.log(f"Loaded: {a03_data.MaterialCode}")
            except Exception as e:
                self.log(f"Error loading row: {e}")
        self.a03 = A03(Header=header, DataS=data) 
        self.log(f"Data loaded from Excel successfully! ({len(data)} records)")


    def copy_to_clipboard(self):
        if self.a03 is None:
            self.log("Error: No A03 data loaded. Please load from Excel first.")
            messagebox.showerror("Error", "No data loaded")
            return
        try:
            self.log("Generating XML...")
            xml_string = json_to_xml(self.a03.model_dump(), root_name="TransactionRequest")
            pyperclip.copy(xml_string)
            self.log("XML copied to clipboard successfully!")
            messagebox.showinfo("Success", "XML data copied to clipboard!")
            self.log('opening the qr code generator....')
            #save the csv file for label generation
            csv_file = f"ms_label_{self.a03.Header.TransactionId}.csv"
            with open(f"saved/{csv_file}", 'w', newline='') as f:
                f.write("mat_code,control_no,expiry,label_code,timestamp\n")
                for item in self.a03.DataS:
                    f.write(f"{item.MaterialCode},{item.ControlNo},{item.ExpiryDate},123456789,00000000\n")
            # Open the QR code generator script
            ms_file = csv_file
            disp_file = "disp_labels.csv"
            cleaning_file = "cleaning_labels.csv"
            halb_file = "halb_labels.csv"
            QrBar(tk.Tk(), ms_file, disp_file, cleaning_file, halb_file).root.mainloop()

        except Exception as e:
            self.log(f"Error generating XML: {e}")
            messagebox.showerror("Error", f"Failed to copy XML: {e}")
