from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class productclass:
    # Constructor method to initialize the class
    def __init__(self, root):
        """
        Initialize the main application window and set up variables and GUI components for product management.
        """
        # Set up the main window
        self.root = root
        self.root.geometry("1100x500+220+130")  # Window size and position
        self.root.title("Inventory Management System")  # Window title
        self.root.config(bg="white")  # Background color
        self.root.focus_force()  # Focus the window

        # Initialize variables for search functionality
        self.var_search = StringVar()  # Variable for selecting search type
        self.var_searchbar = StringVar()  # Variable for entering search text

        # Initialize variables for product details
        self.var_pid = StringVar()  # Product ID
        self.var_cat = StringVar()  # Category
        self.var_sup = StringVar()  # Supplier
        self.var_name = StringVar()  # Product name
        self.var_price = StringVar()  # Product price
        self.var_qty = StringVar()  # Quantity
        self.var_status = StringVar()  # Product status

        # Fetch initial data for categories and suppliers from the database
        self.cat_list = []  # List for categories
        self.sup_list = []  # List for suppliers
        self.fetch_cat_sup()

        # Set up a frame for displaying product details within the main window
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)  # Position and size of the frame

        # Title label for the product management section
        title = Label(product_frame, text="Manage Products Details", font=("Arial Rounded MT Bold", 18), bg="#0f4d7d",
                      fg="white")
        title.pack(side=TOP, fill=X)  # Display the title at the top of the frame, spanning the full width

        # Labels for product attributes in the first column of the product management frame
        lbl_category = Label(product_frame, text="Category", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_category.place(x=30, y=60)  # Category label

        lbl_supplier = Label(product_frame, text="Supplier", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_supplier.place(x=30, y=110)  # Supplier label

        lbl_name = Label(product_frame, text="Name", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_name.place(x=30, y=160)  # Product name label

        lbl_price = Label(product_frame, text="Price", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_price.place(x=30, y=210)  # Price label

        lbl_quantity = Label(product_frame, text="Quantity", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_quantity.place(x=30, y=260)  # Quantity label

        lbl_status = Label(product_frame, text="Status", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_status.place(x=30, y=310)  # Status label

        # Buttons for operations on product details, placed in column 1 of the product management frame
        Button(product_frame, text="Save", command=self.add, font=("Arial Rounded MT Bold", 15), bg="#2196f3",
               fg="white", cursor="hand2").place(x=10, y=400, width=100,
                                                 height=40)  # Button to save new product details

        Button(product_frame, text="Update", command=self.update, font=("Arial Rounded MT Bold", 15), bg="#4caf50",
               fg="white", cursor="hand2").place(x=120, y=400, width=100,
                                                 height=40)  # Button to update existing product details

        Button(product_frame, text="Delete", command=self.delete, font=("Arial Rounded MT Bold", 15), bg="#f44336",
               fg="white", cursor="hand2").place(x=230, y=400, width=100,
                                                 height=40)  # Button to delete selected product details

        Button(product_frame, text="Clear", command=self.clear, font=("Arial Rounded MT Bold", 15), bg="#607d8b",
               fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)  # Button to clear the form fields

        # Column 1 GUI components for product attributes with dropdown menus and input fields
        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, values=self.cat_list, state='readonly',
                               justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_cat.place(x=150, y=60, width=200)  # Dropdown for selecting product category
        cmb_cat.current(0)  # Set the default selection to the first item in the category list

        cmb_sup = ttk.Combobox(product_frame, textvariable=self.var_sup, values=self.sup_list, state='readonly',
                               justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_sup.place(x=150, y=110, width=200)  # Dropdown for selecting supplier
        cmb_sup.current(0)  # Set the default selection to the first item in the supplier list

        txt_name = Entry(product_frame, textvariable=self.var_name, font=("Arial Rounded MT Bold", 15),
                         bg='lightyellow')
        txt_name.place(x=150, y=160, width=200)  # Input field for entering product name

        txt_price = Entry(product_frame, textvariable=self.var_price, font=("Arial Rounded MT Bold", 15),
                          bg='lightyellow')
        txt_price.place(x=150, y=210, width=200)  # Input field for entering product price

        txt_qty = Entry(product_frame, textvariable=self.var_qty, font=("Arial Rounded MT Bold", 15),
                        bg='lightyellow')
        txt_qty.place(x=150, y=260, width=200)  # Input field for entering product quantity

        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, values=("Active", "Inactive"),
                                  state='readonly', justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_status.place(x=150, y=310, width=200)  # Dropdown for selecting product status
        cmb_status.current(0)  # Set the default status to 'Active'

        # Setup a frame for searching products, positioned within the main window
        search_frame = LabelFrame(self.root, text="Search Products", bg="white",
                                  font=("Arial Rounded MT Bold", 12, "bold"), bd=2, relief=RIDGE)
        search_frame.place(x=480, y=10, width=600, height=80)  # Define the size and position of the search frame

        # Search options within the search frame for filtering product details
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search,
                                  values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER,
                                  font=("Arial Rounded MT Bold", 15))
        cmb_search.place(x=10, y=10, width=180)  # Dropdown menu to select the type of search
        cmb_search.current(0)  # Default to 'Select' option

        Entry(search_frame, textvariable=self.var_searchbar, font=("Arial Rounded MT Bold", 15),
              bg="lightyellow").place(x=200, y=10, width=200)  # Input field for entering search text

        Button(search_frame, text="Search", command=self.search, font=("Arial Rounded MT Bold", 15), bg="#007BFF",
               fg="white", cursor="hand2").place(x=420, y=9, width=150, height=30)  # Button to initiate the search

        # Setup the main frame for displaying product details as a table
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)  # Position and size of the product frame

        # Scrollbars for the product table
        scrolly = Scrollbar(p_frame, orient=VERTICAL)  # Vertical scrollbar
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)  # Horizontal scrollbar

        # Product table initialization with columns for product attributes
        self.product_table = ttk.Treeview(p_frame, columns=(
            "pid", "Supplier", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)  # Pack the horizontal scrollbar at the bottom
        scrolly.pack(side=RIGHT, fill=Y)  # Pack the vertical scrollbar on the right
        scrollx.config(command=self.product_table.xview)  # Configure horizontal scroll handling
        scrolly.config(command=self.product_table.yview)  # Configure vertical scroll handling

        # Define headings for each column
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")

        # Configure the display properties of the table
        self.product_table["show"] = "headings"  # Show only the headings, not the internal column names

        # Set the width of each column
        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)

        self.product_table.pack(fill=BOTH, expand=1)  # Pack the table to fill the frame
        self.product_table.bind("<ButtonRelease-1>", self.get_data)  # Bind a function to select table entries

        self.show()  # Display initial product data

    def fetch_cat_sup(self):
        """
        Fetches categories and suppliers from the database to update dropdown menus. It initializes the category
        and supplier lists with 'Select', then appends actual data fetched from the database.
        Handles database connections and exceptions to ensure robust application performance.
        """
        try:
            # Connect to the database using a context manager to handle the connection lifecycle
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()

                # Reset lists and add 'Select' as the first item
                self.cat_list = ["Select"]
                self.sup_list = ["Select"]

                # Execute queries to fetch category and supplier names
                cur.execute("SELECT name FROM category")
                categories = cur.fetchall()
                self.cat_list.extend(cat[0] for cat in categories if cat[0])  # Extend cat_list with category names

                cur.execute("SELECT name FROM supplier")
                suppliers = cur.fetchall()
                self.sup_list.extend(sup[0] for sup in suppliers if sup[0])  # Extend sup_list with supplier names

        except Exception as ex:
            # Handle any exceptions that occur and display an error message
            messagebox.showerror("Error", f"Error retrieving data: {str(ex)}", parent=self.root)

    # def add(self):
    #     """
    #     Adds a new product to the database after validating that all required fields are filled and ensuring no duplicate product names exist.
    #     Handles exceptions and ensures the database connection is closed properly to maintain data integrity and system performance.
    #     """
    #     try:
    #         with sqlite3.connect(database=r'ims.db') as con:
    #             cur = con.cursor()
    #
    #             # Validate all required fields
    #             if any(not getattr(self, f"var_{field}").get() or self.var_cat.get() in ["Select", "Empty"]
    #                    for field in ["sup", "name", "price", "qty", "status"]):
    #                 messagebox.showerror("Error", "All fields are required, please fill all the fields",
    #                                      parent=self.root)
    #                 return  # Early exit if any field is empty or unselected
    #
    #                 # Get supplier_id from supplier name
    #                 cur.execute("SELECT supplier_id FROM supplier WHERE name=?", (self.var_sup.get(),))
    #                 supplier_id = cur.fetchone()
    #                 if supplier_id is None:
    #                     messagebox.showerror("Error", "Selected supplier does not exist", parent=self.root)
    #                     return
    #
    #                 # Get category_id from category name
    #                 cur.execute("SELECT cid FROM category WHERE name=?", (self.var_cat.get(),))
    #                 category_id = cur.fetchone()
    #                 if category_id is None:
    #                     messagebox.showerror("Error", "Selected category does not exist", parent=self.root)
    #                     return
    #
    #             # Prevent duplicate product names in the database
    #             cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
    #             if cur.fetchone():
    #                 messagebox.showerror("Error", "This Product already exists, try a different name", parent=self.root)
    #                 return  # Stop execution if a duplicate name is found
    #
    #             # Insert the new product into the database
    #             cur.execute(
    #                 "INSERT INTO product (supplier_id, category_id, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
    #                 (supplier_id[0], category_id[0], self.var_name.get(), self.var_price.get(),
    #                  self.var_qty.get(), self.var_status.get()))
    #             con.commit()
    #             messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
    #             #self.show()  # Refresh the display to show the new product
    #
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # def add(self):
    #     """
    #     Adds a new product to the database after validating that all required fields are filled and ensuring no duplicate product names exist.
    #     Handles exceptions and ensures the database connection is closed properly to maintain data integrity and system performance.
    #     """
    #     try:
    #         with sqlite3.connect(database=r'ims.db') as con:
    #             cur = con.cursor()
    #
    #             # Validate all required fields
    #             if any(not getattr(self, f"var_{field}").get() or self.var_cat.get() == "Select"
    #                    for field in ["name", "price", "qty", "status"]):
    #                 messagebox.showerror("Error", "All fields are required, please fill all the fields",
    #                                      parent=self.root)
    #                 return  # Early exit if any field is empty or unselected
    #
    #             # Get supplier_id from supplier name
    #             cur.execute("SELECT supplier_id FROM supplier WHERE name=?", (self.var_sup.get(),))
    #             supplier_id = cur.fetchone()
    #             if supplier_id is None:
    #                 messagebox.showerror("Error", "Selected supplier does not exist", parent=self.root)
    #                 return
    #
    #             # Get category_id from category name
    #             cur.execute("SELECT cid FROM category WHERE name=?", (self.var_cat.get(),))
    #             category_id = cur.fetchone()
    #             if category_id is None:
    #                 messagebox.showerror("Error", "Selected category does not exist", parent=self.root)
    #                 return
    #
    #             # Prevent duplicate product names in the database
    #             cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
    #             if cur.fetchone():
    #                 messagebox.showerror("Error", "This Product already exists, try a different name", parent=self.root)
    #                 return  # Stop execution if a duplicate name is found
    #
    #             # Insert the new product into the database
    #             cur.execute(
    #                 "INSERT INTO product (supplier_id, category_id, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
    #                 (supplier_id[0], category_id[0], self.var_name.get(), self.var_price.get(),
    #                  self.var_qty.get(), self.var_status.get()))
    #             con.commit()
    #             messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
    #             self.show()  # Refresh the display to show the new product
    #
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def add(self):
        """
        Adds a new product after verifying required fields and checking for duplicates.
        Communicates errors and confirms successful additions.
        """
        # Check for missing field entries or unselected categories
        if any(not getattr(self, f"var_{field}").get() for field in
               ["name", "price", "qty", "status"]) or self.var_cat.get() == "Select":
            messagebox.showerror("Error", "All fields are required, please fill all fields", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()

                # Ensure the supplier exists and fetch the supplier_id
                supplier_id = cur.execute("SELECT supplier_id FROM supplier WHERE name=?",
                                          (self.var_sup.get(),)).fetchone()
                if not supplier_id:
                    messagebox.showerror("Error", "Selected supplier does not exist", parent=self.root)
                    return

                # Ensure the category exists and fetch the category_id
                category_id = cur.execute("SELECT cid FROM category WHERE name=?", (self.var_cat.get(),)).fetchone()
                if not category_id:
                    messagebox.showerror("Error", "Selected category does not exist", parent=self.root)
                    return

                # Check for duplicate product names
                if cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),)).fetchone():
                    messagebox.showerror("Error", "This Product already exists, try a different name", parent=self.root)
                    return

                # Insert the new product record into the database
                cur.execute("""
                    INSERT INTO product (supplier_id, category_id, name, price, qty, status) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (supplier_id[0], category_id[0], self.var_name.get(), self.var_price.get(), self.var_qty.get(),
                      self.var_status.get()))

                con.commit()
                messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                self.show()  # Refresh the product display

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # def show(self):
    #     """
    #     Fetches and displays all product records from the database into the product_table,
    #     ensuring the display is up-to-date. This method handles database operations safely,
    #     ensuring exceptions are caught and resources are properly managed.
    #     """
    #     try:
    #         # Use context manager to handle database connection
    #         with sqlite3.connect(database=r'ims.db') as con:
    #             cur = con.cursor()
    #             cur.execute("SELECT * FROM product")
    #             rows = cur.fetchall()
    #
    #         # Clear the table before inserting new rows to reflect the latest data
    #         self.product_table.delete(*self.product_table.get_children())
    #
    #         # Populate the table with fresh data from the database
    #         for row in rows:
    #             self.product_table.insert('', END, values=row)
    #
    #         # Center align the table headers and content for aesthetics and readability
    #         for col in self.product_table["columns"]:
    #             self.product_table.heading(col, anchor=CENTER)
    #             self.product_table.column(col, anchor=CENTER)
    #
    #     except Exception as ex:
    #         # Inform the user if an error occurs during the database operation
    #         messagebox.showerror("Error", f"Error retrieving data: {str(ex)}", parent=self.root)

    # def show(self):
    #     """
    #     Fetches and displays all product records from the database into the product_table,
    #     ensuring the display is up-to-date. This method handles database operations safely,
    #     ensuring exceptions are caught and resources are properly managed.
    #     """
    #     try:
    #         # Use context manager to handle database connection
    #         with sqlite3.connect(database=r'ims.db') as con:
    #             cur = con.cursor()
    #             # Modify the SQL query to join the product and supplier tables
    #             cur.execute(
    #                 "SELECT product.pid, supplier.name, category.name, product.name, product.price, product.qty, product.status FROM product INNER JOIN supplier ON product.supplier_id = supplier.supplier_id INNER JOIN category ON product.category_id = category.cid")
    #             rows = cur.fetchall()
    #
    #         # Clear the table before inserting new rows to reflect the latest data
    #         self.product_table.delete(*self.product_table.get_children())
    #
    #         # Populate the table with fresh data from the database
    #         for row in rows:
    #             self.product_table.insert('', END, values=row)
    #
    #         # Center align the table headers and content for aesthetics and readability
    #         for col in self.product_table["columns"]:
    #             self.product_table.heading(col, anchor=CENTER)
    #             self.product_table.column(col, anchor=CENTER)
    #
    #     except Exception as ex:
    #         # Inform the user if an error occurs during the database operation
    #         messagebox.showerror("Error", f"Error retrieving data: {str(ex)}", parent=self.root)

    def show(self):
        """
        Fetches and displays all product records from the database. It combines information
        across the product, supplier, and category tables to provide a comprehensive view.
        Exception handling ensures robustness.
        """
        try:
            # Establish database connection and fetch data
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Execute a SQL query to join product with supplier and category tables
                cur.execute("""
                    SELECT p.pid, s.name AS supplier_name, c.name AS category_name, 
                           p.name, p.price, p.qty, p.status
                    FROM product p
                    JOIN supplier s ON p.supplier_id = s.supplier_id
                    JOIN category c ON p.category_id = c.cid
                """)
                rows = cur.fetchall()

            # Clear previous entries from the product_table
            self.product_table.delete(*self.product_table.get_children())

            # Insert new data into the product_table
            for row in rows:
                self.product_table.insert('', END, values=row)

            # Update column settings for better presentation
            for col in self.product_table["columns"]:
                self.product_table.heading(col, anchor=CENTER)
                self.product_table.column(col, anchor=CENTER)

        except Exception as ex:
            # Handle exceptions and inform the user
            messagebox.showerror("Error", f"Error retrieving data: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        """
        Retrieves data from the selected row in the product table and updates the form fields for editing.
        This function is called when a row in the product table is selected.
        """
        # Get the currently focused item in the product table
        f = self.product_table.focus()
        if not f:
            return  # Exit the function if no item is focused

        # Retrieve the data from the focused item
        content = self.product_table.item(f)
        row = content.get('values')

        # Check if the row has data to prevent errors on empty row selection
        if not row:
            return  # Exit the function if the row is empty

        # Update form fields with the data from the selected row
        self.var_pid.set(row[0])  # Set Product ID
        self.var_sup.set(row[1])  # Set Supplier
        self.var_cat.set(row[2])  # Set Category
        self.var_name.set(row[3])  # Set Product Name
        self.var_price.set(row[4])  # Set Price
        self.var_qty.set(row[5])  # Set Quantity
        self.var_status.set(row[6])  # Set Status

    # ====================UPDATE DATA======================

    # def update(self):
    #     """
    #     Updates the details of an existing product in the database based on the provided Product ID.
    #     Validates the product's existence before updating and handles exceptions.
    #     """
    #     if self.var_pid.get() == "":
    #         messagebox.showerror("Error", "Please select product from list", parent=self.root)
    #         return
    #
    #     # Using a context manager to handle database connections
    #     with sqlite3.connect(database=r'ims.db') as con:
    #         cur = con.cursor()
    #
    #         try:
    #             # Verify the existence of the product using the provided Product ID
    #             cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
    #             row = cur.fetchone()
    #             if not row:
    #                 messagebox.showerror("Error", "Invalid Product", parent=self.root)
    #                 return
    #
    #             # Update product details in the database
    #             cur.execute("""
    #                 UPDATE product SET
    #                 Category=?, Supplier=?, name=?, price=?, qty=?, status=?
    #                 WHERE pid=?
    #                 """, (
    #                 self.var_cat.get(),
    #                 self.var_sup.get(),
    #                 self.var_name.get(),
    #                 self.var_price.get(),
    #                 self.var_qty.get(),
    #                 self.var_status.get(),
    #                 self.var_pid.get()
    #             ))
    #             con.commit()
    #             messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
    #             self.show()
    #
    #         except Exception as ex:
    #             # Handle any exceptions during the database operation
    #             messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def update(self):
        """
        Updates an existing product in the database. Ensures the product exists and valid foreign keys are provided for supplier and category.
        """
        if not self.var_pid.get():
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            return

        with sqlite3.connect(database=r'ims.db') as con:
            cur = con.cursor()

            try:
                # Verify the existence of the product using the provided Product ID
                if not cur.execute("SELECT pid FROM product WHERE pid=?", (self.var_pid.get(),)).fetchone():
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                    return

                # Check for valid supplier and category
                supplier_id = cur.execute("SELECT supplier_id FROM supplier WHERE name=?",
                                          (self.var_sup.get(),)).fetchone()
                category_id = cur.execute("SELECT cid FROM category WHERE name=?", (self.var_cat.get(),)).fetchone()
                if not supplier_id or not category_id:
                    messagebox.showerror("Error", "Invalid Supplier or Category", parent=self.root)
                    return

                # Update product details in the database
                cur.execute("""
                    UPDATE product SET 
                    supplier_id=?, category_id=?, name=?, price=?, qty=?, status=? 
                    WHERE pid=?
                    """, (
                    supplier_id[0],  # supplier_id is a tuple, index 0 to get the actual id
                    category_id[0],  # category_id is a tuple, index 0 to get the actual id
                    self.var_name.get(),
                    self.var_price.get(),
                    self.var_qty.get(),
                    self.var_status.get(),
                    self.var_pid.get()
                ))
                con.commit()
                messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                self.show()  # Refresh the display

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        """
        Deletes a selected product from the database after user confirmation. Ensures that a product is
        actually selected and validates its existence before deletion. This function uses parameterized
        queries to enhance security and prevent SQL injection.
        """
        # Establish a connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Check if a product ID has been selected
            if not self.var_pid.get():
                messagebox.showerror("Error", "Select product from the list", parent=self.root)
                return

            # Verify the existence of the product using a parameterized query
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Product", parent=self.root)
                return

            # Confirm deletion with the user
            if messagebox.askyesno("Confirm", "Do you really want to delete", parent=self.root):
                # Delete the product from the database
                cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Product deleted Successfully", parent=self.root)
                self.show()  # Refresh the display to update the product list
                self.clear()  # Clear form fields if necessary

        except Exception as ex:
            # Handle any exceptions that occur during the delete operation
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection to avoid resource leaks
            con.close()

    def clear(self):
        """
        Resets all input fields in the product management form to their default states, preparing the form
        for new entries or clearing it after operations like add, update, or delete. The product table
        is also refreshed to reflect the most current data.
        """
        # Reset fields related to product details
        self.var_cat.set("Select")  # Default for category dropdown
        self.var_sup.set("Select")  # Default for supplier dropdown
        self.var_name.set("")  # Clear the name input
        self.var_price.set("")  # Clear the price input
        self.var_qty.set("")  # Clear the quantity input
        self.var_status.set("Active")  # Default status is 'Active'
        self.var_pid.set("")  # Clear the product ID input

        # Reset fields related to search functionality
        self.var_searchbar.set("")  # Clear the search text
        self.var_search.set("Select")  # Default search category

        # Refresh the display to show updated or default data
        self.show()

    def search(self):
        """
        Executes a search query based on user-selected criteria and keyword, updating the product table
        with results. This method employs parameterized queries to safeguard against SQL injection, ensuring
        application security.
        """
        # Open database connection
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Ensure valid search criteria and keyword are provided
            if self.var_search.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
                return
            if not self.var_searchbar.get():
                messagebox.showerror("Error", "Search input is required", parent=self.root)
                return

            # Execute parameterized query to fetch records based on search criteria
            query = f"SELECT * FROM product WHERE {self.var_search.get()} LIKE ?"
            cur.execute(query, ('%' + self.var_searchbar.get() + '%',))
            rows = cur.fetchall()

            # Update product table with search results or show error if no match is found
            if rows:
                self.product_table.delete(*self.product_table.get_children())
                for row in rows:
                    self.product_table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close database connection
            con.close()


# Entry point of the programú
if __name__ == "__main__":
    # Create a Tkinter root window
    root = Tk()

    # Create an instance of the product class with the root window as its parent
    obj = productclass(root)

    # Start the Tkinter event loop
    root.mainloop()
