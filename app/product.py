import tkinter as tk
from tkinter import ttk, messagebox

from .database import save_product, get_all_products


def create_product(parent):

    tk.Label(
        parent,
        text="Product Management",
        font=("Arial", 28, "bold"),
        bg="#F5F7FA"
    ).pack(pady=20)

    form = tk.Frame(parent, bg="#F5F7FA")
    form.pack()

    labels = [
        "Product Name",
        "HSN Code",
        "GST %",
        "Unit Price",
        "Stock"
    ]

    entries = {}

    for label in labels:

        tk.Label(
            form,
            text=label,
            bg="#F5F7FA",
            font=("Arial", 11)
        ).pack(anchor="w")

        entry = tk.Entry(form, width=40)
        entry.pack(pady=4)

        entries[label] = entry

    columns = (
        "Product",
        "HSN",
        "GST %",
        "Price",
        "Stock"
    )

    tree = ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=8
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    tree.pack(pady=20)

    def load_products():

        for row in tree.get_children():
            tree.delete(row)

        for product in get_all_products():
            tree.insert("", tk.END, values=product)

    load_products()

    def save():

        if entries["Product Name"].get() == "":
            messagebox.showerror(
                "Error",
                "Product Name is required."
            )
            return

        try:
            gst = float(entries["GST %"].get())
            price = float(entries["Unit Price"].get())
            stock = int(entries["Stock"].get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "GST, Price and Stock must be numeric."
            )
            return

        save_product(
            entries["Product Name"].get(),
            entries["HSN Code"].get(),
            gst,
            price,
            stock
        )

        messagebox.showinfo(
            "Success",
            "Product Saved Successfully!"
        )

        for entry in entries.values():
            entry.delete(0, tk.END)

        load_products()

    tk.Button(
        parent,
        text="Save Product",
        command=save,
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        width=20
    ).pack(pady=15)