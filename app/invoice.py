import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from datetime import datetime

from .database import (
    save_invoice_with_items,
    get_next_invoice_number,
    get_all_invoices,
    get_invoice_by_number,
    get_invoice_items,
    get_all_customers,
    get_all_products
)


def create_invoice(parent):

    invoice_no = get_next_invoice_number()
    today = datetime.now().strftime("%d-%m-%Y")

    invoice_total = 0.0
    total_gst = 0.0
    grand_total = 0.0

    # =====================================================
    # SCROLLABLE MAIN CONTAINER
    # =====================================================

    canvas = tk.Canvas(
        parent,
        bg="#F5F7FA",
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        parent,
        orient="vertical",
        command=canvas.yview
    )

    container = tk.Frame(
    canvas,
    bg="#F5F7FA"
    )

    container_window = canvas.create_window(
        (0, 0),
        window=container,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # =====================================================
    # UPDATE SCROLL REGION
    # =====================================================

    def update_scroll_region(event):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )


    container.bind(
        "<Configure>",
        update_scroll_region
    )
    
    # =====================================================
    # KEEP CONTENT WIDTH SAME AS CANVAS
    # =====================================================

    def resize_container(event):

        canvas.itemconfig(
            container_window,
            width=event.width
        )


    canvas.bind(
        "<Configure>",
        resize_container
    )


    # =====================================================
    # MOUSE WHEEL SCROLLING
    # =====================================================

    def mouse_scroll(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    canvas.bind_all(
        "<MouseWheel>",
        mouse_scroll
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
    # PRODUCT DETAILS
    # =====================================================

    product_frame = tk.LabelFrame(
        invoice_card,
        text="  Product Details  ",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1E293B",
        padx=10,
        pady=10
    )

    product_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    # Get products from database

    products = get_all_products()

    product_names = [
        product[0] for product in products
    ]

    # Product Selection

    tk.Label(
        product_frame,
        text="Product",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    product_entry = ttk.Combobox(
        product_frame,
        values=product_names,
        width=20,
        state="readonly"
    )

    product_entry.grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    # Quantity

    tk.Label(
        product_frame,
        text="Quantity",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    quantity_entry = tk.Entry(
        product_frame,
        width=10
    )

    quantity_entry.grid(
        row=1,
        column=1,
        padx=5,
        pady=5
    )

    # Rate

    tk.Label(
        product_frame,
        text="Rate",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    rate_entry = tk.Entry(
        product_frame,
        width=12
    )

    rate_entry.grid(
        row=1,
        column=2,
        padx=5,
        pady=5
    )

    # GST

    tk.Label(
        product_frame,
        text="GST %",
        bg="white",
        fg="#475569",
        font=("Arial", 10)
    ).grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    gst_entry = tk.Entry(
        product_frame,
        width=10
    )

    gst_entry.grid(
        row=1,
        column=3,
        padx=5,
        pady=5
    )

        # =====================================================
    # AUTO FILL PRODUCT DETAILS
    # =====================================================

    def fill_product_details(event=None):

        selected_product = product_entry.get()

        for product in products:

            if product[0] == selected_product:

                gst = product[2]
                price = product[3]

                rate_entry.delete(0, tk.END)
                rate_entry.insert(0, price)

                gst_entry.delete(0, tk.END)
                gst_entry.insert(0, gst)

                break

    product_entry.bind(
        "<<ComboboxSelected>>",
        fill_product_details
    )

        # =====================================================
    # INVOICE PRODUCT TABLE
    # =====================================================

    product_table_frame = tk.Frame(
        invoice_card,
        bg="white"
    )

    product_table_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    product_columns = (
        "Product",
        "HSN",
        "Quantity",
        "Rate",
        "GST %",
        "Amount"
    )

    product_tree = ttk.Treeview(
        product_table_frame,
        columns=product_columns,
        show="headings",
        height=4
    )

    for col in product_columns:

        product_tree.heading(
            col,
            text=col
        )

        product_tree.column(
            col,
            width=120,
            anchor="center"
        )

    product_tree.pack(
        fill="x"
    )
    
    # =====================================================
    # ADD PRODUCT TO INVOICE
    # =====================================================

    def add_product():

        nonlocal invoice_total, total_gst, grand_total

        selected_product = product_entry.get()
        quantity = quantity_entry.get().strip()
        rate = rate_entry.get().strip()
        gst = gst_entry.get().strip()

        # Check empty fields

        if (
            selected_product == ""
            or quantity == ""
            or rate == ""
            or gst == ""
        ):

            messagebox.showerror(
                "Error",
                "Please select a product and enter quantity."
            )

            return

        # Check numeric values

        try:

            quantity = float(quantity)
            rate = float(rate)
            gst = float(gst)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quantity, Rate and GST must be numeric."
            )

            return

        # Quantity validation

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than zero."
            )

            return

        # Find HSN Code

        hsn_code = ""

        for product in products:

            if product[0] == selected_product:

                hsn_code = product[1]

                break

        # Calculate amount before GST

        amount = quantity * rate

        invoice_total += amount

        gst_amount = amount * gst / 100

        total_gst += gst_amount

        grand_total = invoice_total + total_gst

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, f"{grand_total:.2f}")

        subtotal_label.config(text=f"Subtotal: Rs. {invoice_total:.2f}")
        gst_total_label.config(text=f"Total GST: Rs. {total_gst:.2f}")
        grand_total_label.config(text=f"Grand Total: Rs. {grand_total:.2f}")

        # Add product to table

        product_tree.insert(
            "",
            tk.END,
            values=(
                selected_product,
                hsn_code,
                quantity,
                f"{rate:.2f}",
                f"{gst:.2f}",
                f"{amount:.2f}"
            )
        )

        # Clear product fields

        product_entry.set("")

        quantity_entry.delete(
            0,
            tk.END
        )

        rate_entry.delete(
            0,
            tk.END
        )

        gst_entry.delete(
            0,
            tk.END
        )

        # =====================================================
    # ADD PRODUCT BUTTON
    # =====================================================

    add_product_button = tk.Button(
        product_frame,
        text="Add Product",
        command=add_product,
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold"),
        width=14,
        relief="flat",
        cursor="hand2"
    )

    add_product_button.grid(
        row=1,
        column=4,
        padx=15,
       pady=5
    )   

        # =====================================================
    # GST AND TOTALS SECTION
    # =====================================================

    totals_frame = tk.Frame(
        invoice_card,
        bg="#F8FAFC",
        bd=1,
        relief="solid"
    )

    totals_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    subtotal_label = tk.Label(
    totals_frame,
    text="Subtotal: Rs. 0.00",
    bg="#F8FAFC",
    fg="#475569",
    font=("Arial", 11)
)

    subtotal_label.pack(
        anchor="e",
        padx=20,
        pady=3
    )

    gst_total_label = tk.Label(
        totals_frame,
        text="Total GST: Rs. 0.00",
        bg="#F8FAFC",
        fg="#475569",
        font=("Arial", 11)
    )

    gst_total_label.pack(
        anchor="e",
        padx=20,
        pady=3
    )

    grand_total_label = tk.Label(
        totals_frame,
        text="Grand Total: Rs. 0.00",
        bg="#E0E7FF",
        fg="#1E293B",
        font=("Arial", 13, "bold")
    )

    grand_total_label.pack(
        anchor="e",
        padx=20,
        pady=5
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
        height=4
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
    # VIEW INVOICE DETAILS
    # =====================================================

    def view_invoice_details(event=None):

        selected_rows = tree.selection()

        if not selected_rows:
            return

        selected_invoice = tree.item(selected_rows[0], "values")

        if not selected_invoice:
            return

        selected_invoice_no = selected_invoice[0]

        try:

            invoice = get_invoice_by_number(selected_invoice_no)
            invoice_items = get_invoice_items(selected_invoice_no)

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to retrieve invoice details: {error}"
            )

            return

        if invoice is None:

            messagebox.showerror(
                "Error",
                "Invoice details could not be found."
            )

            return

        invoice_no, customer, saved_grand_total, invoice_date = invoice

        subtotal = 0.0
        total_gst = 0.0

        for product, hsn, quantity, rate, gst, item_amount in invoice_items:

            amount = float(item_amount)
            gst_amount = amount * float(gst) / 100

            subtotal += amount
            total_gst += gst_amount

        calculated_grand_total = subtotal + total_gst

        details_window = tk.Toplevel(invoice_card)
        details_window.title("Invoice Details")
        details_window.geometry("850x600")
        details_window.configure(bg="#F5F7FA")

        details_frame = tk.Frame(
            details_window,
            bg="white",
            bd=1,
            relief="solid"
        )

        details_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            details_frame,
            text="Invoice Details",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1E293B"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        invoice_info_frame = tk.Frame(
            details_frame,
            bg="#F8FAFC"
        )

        invoice_info_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        invoice_details = (
            ("Invoice Number", invoice_no),
            ("Invoice Date", invoice_date),
            ("Customer Name", customer),
            ("Saved Grand Total", f"Rs. {saved_grand_total:.2f}")
        )

        for column, (label, value) in enumerate(invoice_details):

            tk.Label(
                invoice_info_frame,
                text=label,
                font=("Arial", 9),
                bg="#F8FAFC",
                fg="#64748B"
            ).grid(
                row=0,
                column=column,
                padx=15,
                pady=(12, 3),
                sticky="w"
            )

            tk.Label(
                invoice_info_frame,
                text=value,
                font=("Arial", 11, "bold"),
                bg="#F8FAFC",
                fg="#1E293B"
            ).grid(
                row=1,
                column=column,
                padx=15,
                pady=(0, 12),
                sticky="w"
            )

        item_columns = (
            "Product",
            "HSN",
            "Quantity",
            "Rate",
            "GST %",
            "Amount"
        )

        items_tree = ttk.Treeview(
            details_frame,
            columns=item_columns,
            show="headings",
            height=10
        )

        for column in item_columns:

            items_tree.heading(column, text=column)
            items_tree.column(column, width=125, anchor="center")

        for product, hsn, quantity, rate, gst, item_amount in invoice_items:

            items_tree.insert(
                "",
                tk.END,
                values=(
                    product,
                    hsn,
                    f"{quantity:.2f}",
                    f"{rate:.2f}",
                    f"{gst:.2f}",
                    f"{item_amount:.2f}"
                )
            )

        items_tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        totals_details_frame = tk.Frame(
            details_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        totals_details_frame.pack(
            anchor="e",
            padx=20,
            pady=(0, 20)
        )

        tk.Label(
            totals_details_frame,
            text=f"Subtotal: Rs. {subtotal:.2f}",
            font=("Arial", 11),
            bg="#F8FAFC",
            fg="#475569"
        ).pack(
            anchor="e",
            padx=20,
            pady=(10, 3)
        )

        tk.Label(
            totals_details_frame,
            text=f"Total GST: Rs. {total_gst:.2f}",
            font=("Arial", 11),
            bg="#F8FAFC",
            fg="#475569"
        ).pack(
            anchor="e",
            padx=20,
            pady=3
        )

        tk.Label(
            totals_details_frame,
            text=f"Grand Total: Rs. {calculated_grand_total:.2f}",
            font=("Arial", 13, "bold"),
            bg="#E0E7FF",
            fg="#1E293B"
        ).pack(
            anchor="e",
            padx=20,
            pady=(3, 10)
        )

    tree.bind("<Double-1>", view_invoice_details)

    # =====================================================
    # SAVE INVOICE
    # =====================================================

    def generate_invoice():

        customer = customer_entry.get().strip()

        if customer == "":

            messagebox.showerror(
                "Error",
                "Please select a customer."
            )

            return

        product_rows = product_tree.get_children()

        if not product_rows:

            messagebox.showerror(
                "Error",
                "Please add at least one product."
            )

            return

        invoice_items = []

        try:

            for row in product_rows:

                product, hsn, quantity, rate, gst, item_amount = (
                    product_tree.item(row, "values")
                )

                invoice_items.append((
                    product,
                    hsn,
                    float(quantity),
                    float(rate),
                    float(gst),
                    float(item_amount)
                ))

        except (TypeError, ValueError):

            messagebox.showerror(
                "Error",
                "One or more invoice items contain invalid values."
            )

            return

        try:

            save_invoice_with_items(
                invoice_no,
                customer,
                grand_total,
                today,
                invoice_items
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to save invoice: {error}"
            )

            return

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
