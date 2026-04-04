import tkinter as tk
from tkinter import ttk, messagebox
import openpyxl
import random
import pyperclip
from Header import HEADER  # Assuming Header is defined in model/Header.py
from A03 import A03,  A03Data  # Assuming A03 is defined in model/A03.py
from tools import json_to_xml
from qrbar import QrBar  # Assuming QrBar is defined in qrbar.py
from AxxGen import AxxGen  # Assuming AxxGen is defined in AxxGen.py

class A03Gen(AxxGen):
    def __init__(self, parent, log_callback=None):
        super().__init__(parent, log_callback=log_callback, color='lightgreen')

    def load_from_excel(self):
        import csv
        header = HEADER(TransactionType="A03")
        data = []
        TONo = str(random.randint(1000000, 9999999))
        try:
            with open('A03TO.csv', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for idx, row in enumerate(reader, start=1):
                    # Handle BOM in SELECTED column
                    selected_key = 'SELECTED'
                    if str(row.get(selected_key, '')).strip() != '1':
                        continue
                    # Remove SELECTED and empty values (handle BOM in key)
                    row_data = {k: v for k, v in row.items() if k.lstrip('\ufeff') != 'SELECTED' and v not in (None, '', ' ')}
                    row_data['TransferOrderNo'] = TONo
                    row_data['TransferOrderItemNo'] = str(idx)
                    try:
                        a03_data = A03Data(**row_data)
                        data.append(a03_data)
                        self.log(f"Loaded: {a03_data.MaterialCode}")
                    except Exception as e:
                        self.log(f"Error loading row: {e}")
            self.a03 = A03(Header=header, DataS=data)
            self.log(f"Data loaded from CSV successfully! ({len(data)} records)")
        except Exception as e:
            self.log(f"Error reading CSV: {e}")


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
                f.write("mat_code,control_no,expiry,label_code\n")
                bags_per_ctrl = 10
                for item in self.a03.DataS:
                    for j in range(bags_per_ctrl):
                        f.write(f"{item.MaterialCode},{item.ControlNo},{item.ExpiryDate},{random.randint(1000000, 9999999)}\n")
            # Open the QR code generator script
            ms_file = csv_file
            disp_file = "disp_labels.csv"
            cleaning_file = "cleaning_labels.csv"
            halb_file = "halb_labels.csv"
            popup = tk.Toplevel(self.winfo_toplevel())
            QrBar(popup, ms_file, disp_file, cleaning_file, halb_file)  
        except Exception as e:
            self.log(f"Error generating XML: {e}")
            messagebox.showerror("Error", f"Failed to copy XML: {e}")
