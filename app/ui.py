import tkinter as tk

from .dashboard import create_dashboard, clear_parent
from .invoice import create_invoice
from .customer import create_customer
from .product import create_product
from .database import init_db

# -------------------- Window --------------------

root = tk.Tk()

init_db()

root.title("FiscalNext AI")
root.geometry("1200x700")
root.configure(bg="#F5F7FA")

# -------------------- Main Area --------------------

main = tk.Frame(root, bg="#F5F7FA")
main.pack(side="right", expand=True, fill="both")

# -------------------- Navigation --------------------

def show_page(page_name):

    clear_parent(main)

    if page_name == "Dashboard":
        create_dashboard(main)

    elif page_name == "Invoices":
        create_invoice(main)

    elif page_name == "Customers":
        create_customer(main)

    elif page_name == "Products":
        create_product(main)    

    else:

        tk.Label(
            main,
            text=page_name,
            font=("Arial", 28, "bold"),
            bg="#F5F7FA"
        ).pack(pady=30)

        tk.Label(
            main,
            text=f"{page_name} Module Coming Soon...",
            font=("Arial", 16),
            fg="gray",
            bg="#F5F7FA"
        ).pack()


# -------------------- Sidebar --------------------

sidebar = tk.Frame(
    root,
    bg="#1E293B",
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

logo = tk.Label(
    sidebar,
    text="FiscalNext AI",
    bg="#1E293B",
    fg="white",
    font=("Arial", 20, "bold")
)

logo.pack(pady=25)

menu = [
    "Dashboard",
    "Accounting",
    "GST",
    "Invoices",
    "Customers",
    "Products",
    "Reports",
    "AI Assistant",
    "Settings"
]

for item in menu:

    tk.Button(
        sidebar,
        text=item,
        font=("Arial", 12),
        bg="#334155",
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        width=20,
        pady=10,
        command=lambda x=item: show_page(x)
    ).pack(pady=5)

# -------------------- Default Page --------------------

show_page("Dashboard")