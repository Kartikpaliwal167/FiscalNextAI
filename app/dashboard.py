import tkinter as tk


def create_dashboard(parent):

    title = tk.Label(
        parent,
        text="Dashboard",
        font=("Arial", 28, "bold"),
        bg="#F5F7FA"
    )
    title.pack(pady=20)

    cards = tk.Frame(parent, bg="#F5F7FA")
    cards.pack()

    data = [
        ("Total Sales", "₹12,50,000"),
        ("GST Due", "₹48,500"),
        ("Pending Invoices", "18"),
        ("AI Tasks", "5")
    ]

    for heading, value in data:

        card = tk.Frame(cards, bg="white", bd=1, relief="solid")
        card.pack(side="left", padx=20)

        tk.Label(
            card,
            text=heading,
            bg="white",
            font=("Arial", 12)
        ).pack(padx=30, pady=(20, 5))

        tk.Label(
            card,
            text=value,
            bg="white",
            fg="green",
            font=("Arial", 22, "bold")
        ).pack(pady=(0, 20))


def clear_parent(parent):
    for widget in parent.winfo_children():
        widget.destroy()