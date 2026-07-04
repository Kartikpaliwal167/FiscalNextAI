import tkinter as tk
from tkinter import ttk, messagebox

from .database import save_customer, get_all_customers


def create_customer(parent):

    tk.Label(
        parent,
        text="Customer Management",
        font=("Arial", 28, "bold"),
        bg="#F5F7FA"
    ).pack(pady=20)

    form = tk.Frame(parent, bg="#F5F7FA")
    form.pack()

    labels = [
        "Customer Name",
        "Company Name",
        "GSTIN",
        "Phone",
        "Email",
        "Address",
        "State",
        "PIN Code"
    ]

    entries = {}

    for label in labels:

        tk.Label(
            form,
            text=label,
            bg="#F5F7FA",
            font=("Arial", 11)
        ).pack(anchor="w")

        entry = tk.Entry(form, width=45)
        entry.pack(pady=4)

        entries[label] = entry

    columns = (
        "Customer",
        "Company",
        "GSTIN",
        "Phone",
        "Email",
        "State"
    )

    tree = ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=8
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(pady=20)

    def load_customers():

        for row in tree.get_children():
            tree.delete(row)

        for customer in get_all_customers():
            tree.insert("", tk.END, values=customer)

    load_customers()

    def save():

        if entries["Customer Name"].get() == "":
            messagebox.showerror(
                "Error",
                "Customer Name is required."
            )
            return

        save_customer(
            entries["Customer Name"].get(),
            entries["Company Name"].get(),
            entries["GSTIN"].get(),
            entries["Phone"].get(),
            entries["Email"].get(),
            entries["Address"].get(),
            entries["State"].get(),
            entries["PIN Code"].get()
        )

        messagebox.showinfo(
            "Success",
            "Customer Saved Successfully!"
        )

        for entry in entries.values():
            entry.delete(0, tk.END)

        load_customers()

    tk.Button(
        parent,
        text="Save Customer",
        command=save,
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        width=20
    ).pack(pady=15)