import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fiscalnext.db")


def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- INVOICES ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT UNIQUE,
        customer TEXT,
        amount REAL,
        date TEXT
    )
    """)

    # ---------------- CUSTOMERS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        company_name TEXT,
        gstin TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        state TEXT,
        pin_code TEXT
    )
    """)

    # ---------------- PRODUCTS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        hsn_code TEXT,
        gst REAL,
        price REAL,
        stock INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ======================================================
# INVOICE FUNCTIONS
# ======================================================

def save_invoice(invoice_no, customer, amount, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO invoices(invoice_no,customer,amount,date)
    VALUES(?,?,?,?)
    """,(invoice_no,customer,amount,date))

    conn.commit()
    conn.close()


def get_all_invoices():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    SELECT invoice_no,customer,amount,date
    FROM invoices
    ORDER BY id DESC
    """)

    data=cursor.fetchall()

    conn.close()

    return data


def get_next_invoice_number():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT MAX(id) FROM invoices")

    last=cursor.fetchone()[0]

    conn.close()

    if last is None:
        return "INV-0001"

    return f"INV-{last+1:04d}"


# ======================================================
# CUSTOMER FUNCTIONS
# ======================================================

def save_customer(
    customer_name,
    company_name,
    gstin,
    phone,
    email,
    address,
    state,
    pin_code
):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO customers(
        customer_name,
        company_name,
        gstin,
        phone,
        email,
        address,
        state,
        pin_code
    )
    VALUES(?,?,?,?,?,?,?,?)
    """,(
        customer_name,
        company_name,
        gstin,
        phone,
        email,
        address,
        state,
        pin_code
    ))

    conn.commit()
    conn.close()


def get_all_customers():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    SELECT
    customer_name,
    company_name,
    gstin,
    phone,
    email,
    state
    FROM customers
    ORDER BY customer_name
    """)

    data=cursor.fetchall()

    conn.close()

    return data


# ======================================================
# PRODUCT FUNCTIONS
# ======================================================

def save_product(
    product_name,
    hsn_code,
    gst,
    price,
    stock
):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO products(
        product_name,
        hsn_code,
        gst,
        price,
        stock
    )
    VALUES(?,?,?,?,?)
    """,(
        product_name,
        hsn_code,
        gst,
        price,
        stock
    ))

    conn.commit()
    conn.close()


def get_all_products():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    SELECT
    product_name,
    hsn_code,
    gst,
    price,
    stock
    FROM products
    ORDER BY product_name
    """)

    data=cursor.fetchall()

    conn.close()

    return data


def get_all_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        customer_name,
        company_name,
        gstin,
        phone,
        email,
        state
    FROM customers
    ORDER BY customer_name
    """)

    data = cursor.fetchall()

    conn.close()

    return data