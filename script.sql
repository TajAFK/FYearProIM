-- Drop existing tables if they exist to avoid errors in case of re-creation
DROP TABLE IF EXISTS bill_items;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS employee;

-- Create 'employee' table
CREATE TABLE IF NOT EXISTS employee (
    eid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    gender TEXT,
    contact TEXT,
    dob DATE,
    doj DATE,
    pass TEXT,
    utype TEXT,
    address TEXT,
    salary REAL
);

-- Create 'supplier' table
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice TEXT,
    name TEXT,
    contact TEXT,
    desc TEXT
);

-- Create 'category' table
CREATE TABLE IF NOT EXISTS category (
    cid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- Create 'product' table
CREATE TABLE IF NOT EXISTS product (
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    qty INTEGER,
    status TEXT,
    supplier_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES supplier (supplier_id),
    FOREIGN KEY (category_id) REFERENCES category (cid)
);

-- Create 'customers' table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT
);

-- Create 'bills' table
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    customer_id INTEGER,
    bill_date DATE,
    total_amount REAL,
    discount_given REAL,
    net_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

-- Create 'bill_items' table
CREATE TABLE IF NOT EXISTS bill_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price_per_unit REAL,
    total_price REAL,
    FOREIGN KEY (bill_id) REFERENCES bills (bill_id),
    FOREIGN KEY (product_id) REFERENCES product (pid)
);
