import sqlite3


def create_db():
    """
    Create a database and define tables for an inventory management system.
    This function sets up tables for employees, suppliers, categories, products, customers, and bills.
    Each table is created only if it does not already exist.
    """
    try:
        # Establish a connection to the SQLite database
        con = sqlite3.connect('ims.db')
        cur = con.cursor()

        # Create 'employee' table with appropriate types for dates and numeric fields
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob DATE,  -- Assuming date of birth is stored as a date
            doj DATE,  -- Assuming date of joining is stored as a date
            pass TEXT,
            utype TEXT,
            address TEXT,
            salary REAL  -- Assuming salary should be stored as a numeric type
        )
        """)

        # Create 'supplier' table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice TEXT,  -- Assuming invoice might contain alphanumeric characters
            name TEXT,
            contact TEXT,
            desc TEXT
        )
        """)

        # Create 'category' table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS category (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """)

        # Create 'product' table with more specific types for price and quantity
        cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,  -- Changing price to REAL to accommodate floating point values
            qty INTEGER,  -- Changing quantity to INTEGER for whole number values
            status TEXT,
            supplier_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES supplier (supplier_id),
            FOREIGN KEY (category_id) REFERENCES category (cid)
        )
        """)

        # Create 'customers' table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT
        )
        """)

        # Create 'bills' table with a DATE type for the bill_date
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            customer_id INTEGER,
            bill_date DATE,
            total_amount REAL,
            discount_given REAL,
            net_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        """)

        # Create 'bill_items' table with REAL for price and total_price
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price_per_unit REAL,
            total_price REAL,
            FOREIGN KEY (bill_id) REFERENCES bills (bill_id),
            FOREIGN KEY (product_id) REFERENCES product (pid)
        )
        """)

        # Commit changes and close the connection to apply the table creation
        con.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        con.close()
        print("Connection closed.")


# Call the create_db function to set up the database when the script is executed
if __name__ == "__main__":
    create_db()
