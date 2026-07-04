import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from .database import (
    save_invoice,
    get_next_invoice_number,
    get_all_invoices
)


def create_invoice(parent):

    today = datetime.now().strftime("%d-%m-%Y")

    tk.Label(
        parent,
        text="Invoices",
        font=("Arial",28,"bold"),
        bg="#F5F7FA"
    ).pack(pady=15)

    invoice_label = tk.Label(
        parent,
        text="",
        font=("Arial",13,"bold"),
        fg="blue",
        bg="#F5F7FA"
    )

    invoice_label.pack()

    tk.Label(
        parent,
        text=f"Date : {today}",
        bg="#F5F7FA",
        fg="gray"
    ).pack(pady=(0,20))

    tk.Label(
        parent,
        text="Customer Name",
        bg="#F5F7FA"
    ).pack()

    customer_entry = tk.Entry(parent,width=40)
    customer_entry.pack(pady=5)

    tk.Label(
        parent,
        text="Invoice Amount",
        bg="#F5F7FA"
    ).pack()

    amount_entry = tk.Entry(parent,width=40)
    amount_entry.pack(pady=5)

    result = tk.Label(
        parent,
        text="",
        bg="#F5F7FA",
        fg="green",
        font=("Arial",11)
    )

    result.pack(pady=10)

    tk.Label(
        parent,
        text="Invoice History",
        font=("Arial",16,"bold"),
        bg="#F5F7FA"
    ).pack(pady=15)

    columns=("Invoice No","Customer","Amount","Date")

    tree=ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=8
    )

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,width=150,anchor="center")

    tree.pack()

    def load_history():

        invoice_label.config(
            text=f"Invoice No : {get_next_invoice_number()}"
        )

        for row in tree.get_children():
            tree.delete(row)

        for row in get_all_invoices():
            tree.insert("",tk.END,values=row)

    load_history()

    def generate_invoice():

        customer=customer_entry.get().strip()
        amount=amount_entry.get().strip()

        if customer=="" or amount=="":
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        try:
            amount=float(amount)
        except:
            messagebox.showerror(
                "Error",
                "Amount must be numeric."
            )
            return

        invoice_no=get_next_invoice_number()

        save_invoice(
            invoice_no,
            customer,
            amount,
            today
        )

        result.config(
            text="✅ Invoice Saved Successfully!"
        )

        customer_entry.delete(0,tk.END)
        amount_entry.delete(0,tk.END)

        load_history()

    tk.Button(
        parent,
        text="Generate Invoice",
        command=generate_invoice,
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        width=20
    ).pack(pady=20)