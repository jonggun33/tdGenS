import random

from AxxGen import AxxGen  # Assuming AxxGen is defined in AxxGen.py
from Header import HEADER  # Assuming Header is defined in model/Header.py
from A13 import A13,  A13Data  # Assuming A13 is defined in model/A13.py
from tools import json_to_xml 
import pyperclip
from tkinter import messagebox  
import openpyxl

class A13Gen(AxxGen):
    def __init__(self, parent, log_callback=None):
        super().__init__(parent, log_callback=log_callback, color='lightcoral')

    def load_from_excel(self):
        import csv
        header = HEADER(TransactionType="A13")
        data = []
        reservation_number = random.randint(10000000, 99999999)  # Generate random 8-digit number for ReservationNo
        try:
            with open('A13Reservation.csv', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Handle BOM in SELECTED column
                    selected_key = 'SELECTED'
                    if str(row.get(selected_key, '')).strip() != '1':
                        continue
                    # Remove SELECTED and empty values (handle BOM in key)
                    self.log(f"Processing row: {row}")
                    row_data = {k: v for k, v in row.items() if k.lstrip('\ufeff') != 'SELECTED' and v not in (None, '', ' ')}
                    row_data['ReservationNo'] = str(reservation_number)
                    try:
                        a13_data = A13Data(**row_data)
                        data.append(a13_data)
                        self.log(f"Loaded: {a13_data.Material}")
                    except Exception as e:
                        self.log(f"Error loading row: {e}")
            self.a13 = A13(Header=header, DataS=data)
            self.log(f"Data loaded from CSV successfully! ({len(data)} records)")
        except Exception as e:
            self.log(f"Error reading CSV: {e}")

    def copy_to_clipboard(self):
        if self.a13 is None:
            self.log("Error: No A13 data loaded. Please load from Excel first.")
            messagebox.showerror("Error", "No data loaded")
            return
        try:
            self.log("Generating XML...")
            xml_string = json_to_xml(self.a13.model_dump(), root_name="TransactionRequest")
            pyperclip.copy(xml_string)
            self.log("XML copied to clipboard successfully!")
            messagebox.showinfo("Success", "XML data copied to clipboard!")
        except Exception as e:
            self.log(f"Error generating XML: {e}")
            messagebox.showerror("Error", f"Failed to generate XML: {e}")