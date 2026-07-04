import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from .database import (
    save_invoice,
    get_next_invoice_number,
    get_all_invoices
)

def create_invoice(parent):

    invoice_no = get_next_invoice_number()
    today = datetime.now().strftime("%d-%m-%Y")

    # ==============================
    # Main Container
    # ==============================

    container = tk.Frame(
        parent,
        bg="#F5F7FA",
        padx=20,
        pady=20
    )

    container.pack(fill="both", expand=True)

    # ==============================
    # Header
    # ==============================

    header = tk.Frame(
        container,
        bg="white",
        bd=1,
        relief="solid"
    )

    header.pack(fill="x", pady=(0,15))

    tk.Label(
        header,
        text="GST TAX INVOICE",
        font=("Arial",24,"bold"),
        bg="white",
        fg="#1E293B"
    ).pack(pady=(15,5))

    tk.Label(
        header,
        text="FiscalNext AI",
        font=("Arial",15,"bold"),
        bg="white",
        fg="#2563EB"
    ).pack()

    tk.Label(
        header,
        text="AI Powered Accounting Software",
        font=("Arial",10),
        bg="white",
        fg="gray"
    ).pack(pady=(0,15))

    # ==============================
    # Invoice Details
    # ==============================

    info = tk.Frame(
        container,
        bg="white",
        bd=1,
        relief="solid"
    )

    info.pack(fill="x", pady=(0,15))

    tk.Label(
        info,
        text=f"Invoice No : {invoice_no}",
        font=("Arial",12,"bold"),
        bg="white"
    ).pack(side="left", padx=20, pady=15)

    tk.Label(
        info,
        text=f"Date : {today}",
        font=("Arial",12),
        bg="white"
    ).pack(side="right", padx=20, pady=15)

    # ==============================
    # Customer Information
    # ==============================

    customer_frame = tk.LabelFrame(
        container,
        text="Customer Information",
        font=("Arial",11,"bold"),
        bg="white",
        padx=15,
        pady=15
    )

    customer_frame.pack(fill="x", pady=(0,20))

        # =====================================================
    # Customer Form
    # =====================================================

    tk.Label(
        customer_frame,
        text="Customer Name",
        bg="white",
        font=("Arial",11)
    ).grid(row=0,column=0,padx=10,pady=8,sticky="w")

    customer_entry=tk.Entry(
        customer_frame,
        width=35,
        font=("Arial",11)
    )
    customer_entry.grid(row=0,column=1,padx=10,pady=8)

    tk.Label(
        customer_frame,
        text="Invoice Amount",
        bg="white",
        font=("Arial",11)
    ).grid(row=1,column=0,padx=10,pady=8,sticky="w")

    amount_entry=tk.Entry(
        customer_frame,
        width=35,
        font=("Arial",11)
    )

    amount_entry.grid(row=1,column=1,padx=10,pady=8)

    # =====================================================
    # Invoice History Frame
    # =====================================================

    history_frame=tk.LabelFrame(
        container,
        text="Invoice History",
        bg="white",
        font=("Arial",11,"bold"),
        padx=10,
        pady=10
    )

    history_frame.pack(fill="both",expand=True,pady=10)

    columns=(
        "Invoice No",
        "Customer",
        "Amount",
        "Date"
    )

    tree=ttk.Treeview(
        history_frame,
        columns=columns,
        show="headings",
        height=8
    )

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,width=150,anchor="center")

    tree.pack(fill="x")

    result=tk.Label(
        container,
        text="",
        bg="#F5F7FA",
        fg="green",
        font=("Arial",11,"bold")
    )

    result.pack(pady=10)

    # =====================================================
    # Load Invoice History
    # =====================================================

    def load_history():

        for row in tree.get_children():
            tree.delete(row)

        for invoice in get_all_invoices():
            tree.insert("",tk.END,values=invoice)

    load_history()

    # =====================================================
    # Save Invoice
    # =====================================================

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

        except ValueError:

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

        customer_entry.delete(0,tk.END)
        amount_entry.delete(0,tk.END)

        result.config(
            text="✅ Invoice Saved Successfully!"
        )

        load_history()

    # =====================================================
    # Buttons
    # =====================================================

    button_frame=tk.Frame(
        container,
        bg="#F5F7FA"
    )

    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Generate Invoice",
        command=generate_invoice,
        bg="#16A34A",
        fg="white",
        font=("Arial",11,"bold"),
        width=18
    ).grid(row=0,column=0,padx=10)

    tk.Button(
        button_frame,
        text="Generate PDF",
        bg="#2563EB",
        fg="white",
        font=("Arial",11,"bold"),
        width=18
    ).grid(row=0,column=1,padx=10)

    tk.Button(
        button_frame,
        text="Print",
        bg="#F59E0B",
        fg="white",
        font=("Arial",11,"bold"),
        width=18
    ).grid(row=0,column=2,padx=10)