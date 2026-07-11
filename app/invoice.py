import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from .database import (
    save_invoice,
    get_next_invoice_number,
    get_all_invoices,
    get_all_customers
)


def create_invoice(parent):

    invoice_no = get_next_invoice_number()
    today = datetime.now().strftime("%d-%m-%Y")

    # =====================================================
    # MAIN CONTAINER
    # =====================================================

    container = tk.Frame(
        parent,
        bg="#F5F7FA"
    )

    container.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # PAGE TITLE
    # =====================================================

    title_frame = tk.Frame(
        container,
        bg="#F5F7FA"
    )

    title_frame.pack(
        fill="x",
        padx=30,
        pady=(20, 10)
    )

    tk.Label(
        title_frame,
        text="Create GST Invoice",
        font=("Arial", 24, "bold"),
        bg="#F5F7FA",
        fg="#1E293B"
    ).pack(side="left")

    # =====================================================
    # INVOICE CARD
    # =====================================================

    invoice_card = tk.Frame(
        container,
        bg="white",
        bd=1,
        relief="solid"
    )

    invoice_card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    # =====================================================
    # PROFESSIONAL HEADER
    # =====================================================

    header = tk.Frame(
        invoice_card,
        bg="#1E293B",
        height=100
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    # LEFT SIDE - COMPANY

    company_frame = tk.Frame(
        header,
        bg="#1E293B"
    )

    company_frame.pack(
        side="left",
        padx=25,
        pady=15
    )

    tk.Label(
        company_frame,
        text="FiscalNext AI",
        font=("Arial", 20, "bold"),
        bg="#1E293B",
        fg="white"
    ).pack(anchor="w")

    tk.Label(
        company_frame,
        text="AI Powered Accounting Software",
        font=("Arial", 10),
        bg="#1E293B",
        fg="#CBD5E1"
    ).pack(anchor="w", pady=(5, 0))

    # RIGHT SIDE - TAX INVOICE

    invoice_title_frame = tk.Frame(
        header,
        bg="#1E293B"
    )

    invoice_title_frame.pack(
        side="right",
        padx=25,
        pady=15
    )

    tk.Label(
        invoice_title_frame,
        text="TAX INVOICE",
        font=("Arial", 22, "bold"),
        bg="#1E293B",
        fg="white"
    ).pack(anchor="e")

    tk.Label(
        invoice_title_frame,
        text="GST Invoice",
        font=("Arial", 10),
        bg="#1E293B",
        fg="#CBD5E1"
    ).pack(anchor="e")

    # =====================================================
    # INVOICE INFORMATION BAR
    # =====================================================

    info_frame = tk.Frame(
        invoice_card,
        bg="#F8FAFC"
    )

    info_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    tk.Label(
        info_frame,
        text="Invoice Number",
        font=("Arial", 9),
        bg="#F8FAFC",
        fg="#64748B"
    ).grid(
        row=0,
        column=0,
        padx=15,
        sticky="w"
    )

    tk.Label(
        info_frame,
        text=invoice_no,
        font=("Arial", 12, "bold"),
        bg="#F8FAFC",
        fg="#1E293B"
    ).grid(
        row=1,
        column=0,
        padx=15,
        pady=(3, 10),
        sticky="w"
    )

    tk.Label(
        info_frame,
        text="Invoice Date",
        font=("Arial", 9),
        bg="#F8FAFC",
        fg="#64748B"
    ).grid(
        row=0,
        column=1,
        padx=50,
        sticky="w"
    )

    tk.Label(
        info_frame,
        text=today,
        font=("Arial", 12, "bold"),
        bg="#F8FAFC",
        fg="#1E293B"
    ).grid(
        row=1,
        column=1,
        padx=50,
        pady=(3, 10),
        sticky="w"
    )

    # =====================================================
    # CUSTOMER INFORMATION
    # =====================================================

    customer_frame = tk.LabelFrame(
        invoice_card,
        text="  Customer Details  ",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1E293B",
        padx=20,
        pady=15
    )

    customer_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    tk.Label(
        customer_frame,
        text="Customer Name",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    customers = get_all_customers()

    customer_names = [
        customer[0] for customer in customers
    ]

    customer_entry = ttk.Combobox(
        customer_frame,
        values=customer_names,
        width=33,
        font=("Arial", 11),
        state="readonly"
    )

    customer_entry.grid(
        row=1,
        column=0,
        padx=10,
        pady=(0, 10)
    )

    tk.Label(
        customer_frame,
        text="Invoice Amount",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=1,
        padx=30,
        pady=5,
        sticky="w"
    )

    amount_entry = tk.Entry(
        customer_frame,
        width=25,
        font=("Arial", 11)
    )

    amount_entry.grid(
        row=1,
        column=1,
        padx=30,
        pady=(0, 10)
    )

    # =====================================================
    # INVOICE HISTORY
    # =====================================================

    history_frame = tk.LabelFrame(
        invoice_card,
        text="  Recent Invoices  ",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1E293B",
        padx=10,
        pady=10
    )

    history_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    columns = (
        "Invoice No",
        "Customer",
        "Amount",
        "Date"
    )

    tree = ttk.Treeview(
        history_frame,
        columns=columns,
        show="headings",
        height=7
    )

    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            width=150,
            anchor="center"
        )

    tree.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # RESULT MESSAGE
    # =====================================================

    result = tk.Label(
        invoice_card,
        text="",
        bg="white",
        fg="#16A34A",
        font=("Arial", 10, "bold")
    )

    result.pack()

    # =====================================================
    # LOAD INVOICE HISTORY
    # =====================================================

    def load_history():

        for row in tree.get_children():
            tree.delete(row)

        for invoice in get_all_invoices():

            tree.insert(
                "",
                tk.END,
                values=invoice
            )

    load_history()

    # =====================================================
    # SAVE INVOICE
    # =====================================================

    def generate_invoice():

        customer = customer_entry.get().strip()
        amount = amount_entry.get().strip()

        if customer == "" or amount == "":

            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )

            return

        try:

            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Amount must be numeric."
            )

            return

        new_invoice_no = get_next_invoice_number()

        save_invoice(
            new_invoice_no,
            customer,
            amount,
            today
        )

        customer_entry.delete(
            0,
            tk.END
        )

        amount_entry.delete(
            0,
            tk.END
        )

        result.config(
            text="Invoice Saved Successfully!"
        )

        load_history()

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    button_frame = tk.Frame(
        invoice_card,
        bg="white"
    )

    button_frame.pack(
        pady=(0, 20)
    )

    tk.Button(
        button_frame,
        text="Save Invoice",
        command=generate_invoice,
        bg="#16A34A",
        fg="white",
        font=("Arial", 10, "bold"),
        width=16,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    tk.Button(
        button_frame,
        text="Generate PDF",
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold"),
        width=16,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    tk.Button(
        button_frame,
        text="Print Invoice",
        bg="#F59E0B",
        fg="white",
        font=("Arial", 10, "bold"),
        width=16,
        relief="flat",
        cursor="hand2"
    ).grid(
        row=0,
        column=2,
        padx=8
    )