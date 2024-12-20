# Wallee Transaction Export Tool

import time
import threading
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from wallee import Configuration
from wallee.api import TransactionServiceApi, RefundBankTransactionServiceApi, ChargeBankTransactionServiceApi, ShopifyTransactionServiceApi
from wallee.models import EntityQuery, EntityQueryFilter

# Configuration for Wallee API
API_USER_ID = "your_user_id"
API_SECRET = "your_api_secret"
SPACE_ID = 31423

class WalleeTransactionExporter:
    def __init__(self):
        self.config = Configuration(
            user_id=API_USER_ID,
            api_secret=API_SECRET,
            request_timeout=60
        )

    def fetch_transactions(self, year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2):
        query = self._build_query(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2)

        charge_api = ChargeBankTransactionServiceApi(self.config)
        refund_api = RefundBankTransactionServiceApi(self.config)
        
        charge_transactions = charge_api.search(space_id=SPACE_ID, query=query)
        refund_transactions = refund_api.search(space_id=SPACE_ID, query=query)
        
        return self._process_results(charge_transactions, refund_transactions)

    def _build_query(self, year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2):
        greater_filter = EntityQueryFilter(type='LEAF', operator='GREATER_THAN', field_name='bankTransaction.valueDate', value=f'{year}-{mon}-{day}T{h}:{m}:{s}.000Z')
        less_filter = EntityQueryFilter(type='LEAF', operator='LESS_THAN', field_name='bankTransaction.valueDate', value=f'{y2}-{mon2}-{d2}T{h2}:{m2}:{s2}.000Z')
        state_filter = EntityQueryFilter(type='LEAF', operator='EQUALS', field_name='bankTransaction.state', value='SETTLED')
        
        query = EntityQuery(
            filter=EntityQueryFilter(type='AND', children=[greater_filter, less_filter, state_filter]),
            language='en'
        )
        return query

    def _process_results(self, charges, refunds):
        data = []
        for transaction in charges + refunds:
            bank_transaction = transaction.bank_transaction
            data.append({
                'Currency': bank_transaction.currency_bank_account.currency,
                'PostingAmount': bank_transaction.posting_amount,
                'State': bank_transaction.state,
                'ValueDate': bank_transaction.value_date,
                'TransactionID': transaction.transaction.id,
                'MerchantReference': transaction.transaction.merchant_reference
            })
        return data

    def export_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Export Tool")
        self.root.configure(background='#176B87')
        self.exporter = WalleeTransactionExporter()

        self._build_gui()

    def _build_gui(self):
        from_frame = ttk.Frame(self.root, padding=10)
        to_frame = ttk.Frame(self.root, padding=10)

        self._build_date_fields(from_frame, "From", "start")
        self._build_date_fields(to_frame, "To", "end")

        from_frame.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        to_frame.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        export_button = ttk.Button(self.root, text="Export", command=self.export_data)
        export_button.grid(row=2, column=0, pady=10)

    def _build_date_fields(self, frame, label_text, prefix):
        label = ttk.Label(frame, text=f"{label_text} Date (YYYY-MM-DD HH:MM:SS)")
        label.grid(row=0, column=0, columnspan=6)

        setattr(self, f"{prefix}_year", ttk.Entry(frame, width=5))
        setattr(self, f"{prefix}_mon", ttk.Entry(frame, width=3))
        setattr(self, f"{prefix}_day", ttk.Entry(frame, width=3))
        setattr(self, f"{prefix}_hour", ttk.Entry(frame, width=3))
        setattr(self, f"{prefix}_min", ttk.Entry(frame, width=3))
        setattr(self, f"{prefix}_sec", ttk.Entry(frame, width=3))

        fields = [f"{prefix}_year", f"{prefix}_mon", f"{prefix}_day", f"{prefix}_hour", f"{prefix}_min", f"{prefix}_sec"]
        for i, field in enumerate(fields):
            getattr(self, field).grid(row=1, column=i, padx=5)

    def export_data(self):
        try:
            year, mon, day, h, m, s = [
                getattr(self, f"start_{unit}").get().zfill(2) for unit in ["year", "mon", "day", "hour", "min", "sec"]
            ]
            y2, mon2, d2, h2, m2, s2 = [
                getattr(self, f"end_{unit}").get().zfill(2) for unit in ["year", "mon", "day", "hour", "min", "sec"]
            ]

            if not self._validate_inputs(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2):
                return

            data = self.exporter.fetch_transactions(year, mon, day, h, m, s, y2, mon2, d2, h2, m2, s2)
            filename = f"C:/Users/Public/settled_transactions_{y2}-{mon2}-{d2}.csv"
            self.exporter.export_to_csv(data, filename)
            messagebox.showinfo("Success", f"Data exported successfully to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def _validate_inputs(self, *args):
        try:
            for arg in args:
                if not arg.isdigit():
                    raise ValueError("Inputs must be numeric.")
            return True
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()
