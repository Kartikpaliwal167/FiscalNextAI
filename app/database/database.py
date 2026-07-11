import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fiscalnext.db")


def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)
def migrate_customers_table(cursor):

    cursor.execute("PRAGMA table_info(customers)")
    existing_columns = {column[1].lower() for column in cursor.fetchall()}

    required_columns = (
        ("legal_name", "TEXT"),
        ("billing_address_line_1", "TEXT"),
        ("billing_address_line_2", "TEXT"),
        ("city", "TEXT"),
        ("pincode", "TEXT"),
        ("pan", "TEXT")
    )

    for column_name, column_type in required_columns:

        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE customers ADD COLUMN {column_name} {column_type}"
            )

    cursor.execute("""
    UPDATE customers
    SET
        legal_name = COALESCE(NULLIF(legal_name, ''), company_name, ''),
        billing_address_line_1 = COALESCE(
            NULLIF(billing_address_line_1, ''),
            address,
            ''
        ),
        pincode = COALESCE(NULLIF(pincode, ''), pin_code, '')
    """)


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

    # ---------------- INVOICE ITEMS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT NOT NULL,
        product TEXT NOT NULL,
        hsn TEXT,
        quantity REAL NOT NULL,
        rate REAL NOT NULL,
        gst REAL NOT NULL,
        amount REAL NOT NULL
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
        pin_code TEXT,
        legal_name TEXT,
        billing_address_line_1 TEXT,
        billing_address_line_2 TEXT,
        city TEXT,
        pincode TEXT,
        pan TEXT
    )
    """)

    migrate_customers_table(cursor)

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

    # ---------------- COMPANY PROFILE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_profile(
        id INTEGER PRIMARY KEY CHECK (id = 1),
        company_name TEXT NOT NULL,
        legal_name TEXT,
        address_line_1 TEXT,
        address_line_2 TEXT,
        city TEXT,
        state TEXT,
        pincode TEXT,
        gstin TEXT,
        pan TEXT,
        phone TEXT,
        email TEXT,
        website TEXT,
        bank_name TEXT,
        account_number TEXT,
        ifsc_code TEXT,
        branch_name TEXT,
        invoice_terms TEXT
    )
    """)

    conn.commit()
    conn.close()


# ======================================================
# INVOICE FUNCTIONS
# ======================================================

def save_invoice(invoice_no, customer, amount, date, conn=None):

    connection = conn or get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO invoices(invoice_no,customer,amount,date)
        VALUES(?,?,?,?)
        """,(invoice_no,customer,amount,date))

        if conn is None:
            connection.commit()

    except sqlite3.Error:

        if conn is None:
            connection.rollback()

        raise

    finally:

        if conn is None:
            connection.close()


def save_invoice_item(
    invoice_no,
    product,
    hsn,
    quantity,
    rate,
    gst,
    amount,
    conn=None
):

    connection = conn or get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO invoice_items(
            invoice_no,
            product,
            hsn,
            quantity,
            rate,
            gst,
            amount
        )
        VALUES(?,?,?,?,?,?,?)
        """,(
            invoice_no,
            product,
            hsn,
            quantity,
            rate,
            gst,
            amount
        ))

        if conn is None:
            connection.commit()

    except sqlite3.Error:

        if conn is None:
            connection.rollback()

        raise

    finally:

        if conn is None:
            connection.close()


def save_invoice_with_items(
    invoice_no,
    customer,
    amount,
    date,
    invoice_items
):

    conn = get_connection()

    try:

        save_invoice(
            invoice_no,
            customer,
            amount,
            date,
            conn
        )

        for product, hsn, quantity, rate, gst, item_amount in invoice_items:

            save_invoice_item(
                invoice_no,
                product,
                hsn,
                quantity,
                rate,
                gst,
                item_amount,
                conn
            )

        conn.commit()

    except sqlite3.Error:

        conn.rollback()
        raise

    finally:

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


def get_invoice_by_number(invoice_no):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT invoice_no, customer, amount, date
    FROM invoices
    WHERE invoice_no = ?
    """, (invoice_no,))

    invoice = cursor.fetchone()

    conn.close()

    return invoice


def get_invoice_items(invoice_no):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT product, hsn, quantity, rate, gst, amount
    FROM invoice_items
    WHERE invoice_no = ?
    ORDER BY id
    """, (invoice_no,))

    items = cursor.fetchall()

    conn.close()

    return items


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
# COMPANY PROFILE FUNCTIONS
# ======================================================

def save_company_profile(
    company_name,
    legal_name,
    address_line_1,
    address_line_2,
    city,
    state,
    pincode,
    gstin,
    pan,
    phone,
    email,
    website,
    bank_name,
    account_number,
    ifsc_code,
    branch_name,
    invoice_terms
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT id FROM company_profile WHERE id = 1"
        )

        profile_exists = cursor.fetchone() is not None

        if profile_exists:

            cursor.execute("""
            UPDATE company_profile
            SET
                company_name = ?,
                legal_name = ?,
                address_line_1 = ?,
                address_line_2 = ?,
                city = ?,
                state = ?,
                pincode = ?,
                gstin = ?,
                pan = ?,
                phone = ?,
                email = ?,
                website = ?,
                bank_name = ?,
                account_number = ?,
                ifsc_code = ?,
                branch_name = ?,
                invoice_terms = ?
            WHERE id = 1
            """, (
                company_name,
                legal_name,
                address_line_1,
                address_line_2,
                city,
                state,
                pincode,
                gstin,
                pan,
                phone,
                email,
                website,
                bank_name,
                account_number,
                ifsc_code,
                branch_name,
                invoice_terms
            ))

        else:

            cursor.execute("""
            INSERT INTO company_profile(
                id,
                company_name,
                legal_name,
                address_line_1,
                address_line_2,
                city,
                state,
                pincode,
                gstin,
                pan,
                phone,
                email,
                website,
                bank_name,
                account_number,
                ifsc_code,
                branch_name,
                invoice_terms
            )
            VALUES(1,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                company_name,
                legal_name,
                address_line_1,
                address_line_2,
                city,
                state,
                pincode,
                gstin,
                pan,
                phone,
                email,
                website,
                bank_name,
                account_number,
                ifsc_code,
                branch_name,
                invoice_terms
            ))

        conn.commit()

    except sqlite3.Error:

        conn.rollback()
        raise

    finally:

        conn.close()


def get_company_profile():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        company_name,
        legal_name,
        address_line_1,
        address_line_2,
        city,
        state,
        pincode,
        gstin,
        pan,
        phone,
        email,
        website,
        bank_name,
        account_number,
        ifsc_code,
        branch_name,
        invoice_terms
    FROM company_profile
    WHERE id = 1
    """)

    profile = cursor.fetchone()

    conn.close()

    return profile


# ======================================================
# CUSTOMER FUNCTIONS
# ======================================================

def save_customer(
    customer_name,
    legal_name,
    billing_address_line_1,
    billing_address_line_2,
    city,
    state,
    pincode,
    gstin,
    pan,
    phone,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT id FROM customers
        WHERE lower(customer_name) = lower(?)
        """, (customer_name,))

        if cursor.fetchone() is not None:
            raise ValueError("A customer with this name already exists.")

        cursor.execute("""
        INSERT INTO customers(
            customer_name,
            company_name,
            gstin,
            phone,
            email,
            address,
            state,
            pin_code,
            legal_name,
            billing_address_line_1,
            billing_address_line_2,
            city,
            pincode,
            pan
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,(
            customer_name,
            legal_name,
            gstin,
            phone,
            email,
            billing_address_line_1,
            state,
            pincode,
            legal_name,
            billing_address_line_1,
            billing_address_line_2,
            city,
            pincode,
            pan
        ))

        conn.commit()

    except sqlite3.Error:

        conn.rollback()
        raise

    finally:

        conn.close()


def get_all_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        customer_name,
        COALESCE(NULLIF(legal_name, ''), company_name),
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


def get_customer_list():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        customer_name,
        COALESCE(NULLIF(legal_name, ''), company_name),
        gstin,
        phone,
        email,
        state
    FROM customers
    ORDER BY customer_name
    """)

    customers = cursor.fetchall()

    conn.close()

    return customers


def get_customer_by_id(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        customer_name,
        COALESCE(NULLIF(legal_name, ''), company_name),
        COALESCE(NULLIF(billing_address_line_1, ''), address),
        billing_address_line_2,
        city,
        state,
        COALESCE(NULLIF(pincode, ''), pin_code),
        gstin,
        pan,
        phone,
        email
    FROM customers
    WHERE id = ?
    """, (customer_id,))

    customer = cursor.fetchone()

    conn.close()

    return customer


def update_customer(
    customer_id,
    customer_name,
    legal_name,
    billing_address_line_1,
    billing_address_line_2,
    city,
    state,
    pincode,
    gstin,
    pan,
    phone,
    email
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT id FROM customers
        WHERE lower(customer_name) = lower(?)
        AND id != ?
        """, (customer_name, customer_id))

        if cursor.fetchone() is not None:
            raise ValueError("A customer with this name already exists.")

        cursor.execute("""
        UPDATE customers
        SET
            customer_name = ?,
            company_name = ?,
            gstin = ?,
            phone = ?,
            email = ?,
            address = ?,
            state = ?,
            pin_code = ?,
            legal_name = ?,
            billing_address_line_1 = ?,
            billing_address_line_2 = ?,
            city = ?,
            pincode = ?,
            pan = ?
        WHERE id = ?
        """, (
            customer_name,
            legal_name,
            gstin,
            phone,
            email,
            billing_address_line_1,
            state,
            pincode,
            legal_name,
            billing_address_line_1,
            billing_address_line_2,
            city,
            pincode,
            pan,
            customer_id
        ))

        conn.commit()

    except sqlite3.Error:

        conn.rollback()
        raise

    finally:

        conn.close()


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
