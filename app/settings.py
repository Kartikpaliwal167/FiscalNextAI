import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from .database import get_company_profile, save_company_profile


def create_settings(parent):

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

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    def update_scroll_region(event):

        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_container(event):

        canvas.itemconfig(container_window, width=event.width)

    def mouse_scroll(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def bind_mousewheel(widget):

        widget.bind("<MouseWheel>", mouse_scroll, add="+")

        for child in widget.winfo_children():
            bind_mousewheel(child)

    container.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_container)

    title_frame = tk.Frame(container, bg="#F5F7FA")
    title_frame.pack(fill="x", padx=30, pady=(20, 10))

    tk.Label(
        title_frame,
        text="Settings",
        font=("Arial", 24, "bold"),
        bg="#F5F7FA",
        fg="#1E293B"
    ).pack(anchor="w")

    profile_card = tk.Frame(
        container,
        bg="white",
        bd=1,
        relief="solid"
    )

    profile_card.pack(fill="x", padx=30, pady=(0, 20))

    tk.Label(
        profile_card,
        text="Company Profile",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#1E293B"
    ).pack(anchor="w", padx=20, pady=(20, 4))

    tk.Label(
        profile_card,
        text="Business and bank information used across FiscalNext AI.",
        font=("Arial", 10),
        bg="white",
        fg="#64748B"
    ).pack(anchor="w", padx=20, pady=(0, 15))

    form = tk.Frame(profile_card, bg="white")
    form.pack(fill="x", padx=20, pady=(0, 10))

    fields = (
        ("company_name", "Company Name *"),
        ("legal_name", "Legal Name"),
        ("address_line_1", "Address Line 1"),
        ("address_line_2", "Address Line 2"),
        ("city", "City"),
        ("state", "State"),
        ("pincode", "Pincode"),
        ("gstin", "GSTIN"),
        ("pan", "PAN"),
        ("phone", "Phone"),
        ("email", "Email"),
        ("website", "Website"),
        ("bank_name", "Bank Name"),
        ("account_number", "Account Number"),
        ("ifsc_code", "IFSC Code"),
        ("branch_name", "Branch Name")
    )

    entries = {}

    for index, (field_name, label) in enumerate(fields):

        row = (index // 2) * 2
        column = (index % 2) * 2

        tk.Label(
            form,
            text=label,
            font=("Arial", 10),
            bg="white",
            fg="#475569"
        ).grid(
            row=row,
            column=column,
            padx=(0, 20),
            pady=(5, 3),
            sticky="w"
        )

        entry = tk.Entry(form, width=35, font=("Arial", 10))
        entry.grid(
            row=row + 1,
            column=column,
            padx=(0, 20),
            pady=(0, 10),
            sticky="ew"
        )

        entries[field_name] = entry

    tk.Label(
        form,
        text="Invoice Terms",
        font=("Arial", 10),
        bg="white",
        fg="#475569"
    ).grid(
        row=16,
        column=0,
        padx=(0, 20),
        pady=(5, 3),
        sticky="w"
    )

    invoice_terms = tk.Text(
        form,
        width=78,
        height=5,
        font=("Arial", 10)
    )

    invoice_terms.grid(
        row=17,
        column=0,
        columnspan=3,
        padx=(0, 20),
        pady=(0, 15),
        sticky="ew"
    )

    def load_company_profile():

        try:

            profile = get_company_profile()

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load company profile: {error}"
            )

            return

        if profile is None:
            return

        for (field_name, _), value in zip(fields, profile[:-1]):
            entries[field_name].insert(0, value or "")

        invoice_terms.insert("1.0", profile[-1] or "")

    def save_profile():

        company_name = entries["company_name"].get().strip()

        if company_name == "":

            messagebox.showerror(
                "Error",
                "Company Name is required."
            )

            return

        try:

            save_company_profile(
                company_name,
                entries["legal_name"].get().strip(),
                entries["address_line_1"].get().strip(),
                entries["address_line_2"].get().strip(),
                entries["city"].get().strip(),
                entries["state"].get().strip(),
                entries["pincode"].get().strip(),
                entries["gstin"].get().strip(),
                entries["pan"].get().strip(),
                entries["phone"].get().strip(),
                entries["email"].get().strip(),
                entries["website"].get().strip(),
                entries["bank_name"].get().strip(),
                entries["account_number"].get().strip(),
                entries["ifsc_code"].get().strip(),
                entries["branch_name"].get().strip(),
                invoice_terms.get("1.0", tk.END).strip()
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to save company profile: {error}"
            )

            return

        messagebox.showinfo(
            "Success",
            "Company Profile Saved Successfully!"
        )

    tk.Button(
        profile_card,
        text="Save Company Profile",
        command=save_profile,
        bg="#16A34A",
        fg="white",
        font=("Arial", 10, "bold"),
        width=22,
        relief="flat",
        cursor="hand2"
    ).pack(anchor="e", padx=20, pady=(0, 20))

    bind_mousewheel(canvas)
    bind_mousewheel(scrollbar)

    load_company_profile()
