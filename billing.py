from tkinter import *  # Provides access to Tkinter GUI toolkit
from tkinter import ttk  # Provides access to themed widgets
from tkinter import messagebox  # Enables pop-up dialog windows for notifications
import sqlite3  # Facilitates interactions with SQLite database
import time  # Used for handling time-related tasks
import os  # Allows interaction with the operating system, including file and directory handling
import tempfile  # Used for generating temporary files and directories
import subprocess  # Enables running of subprocesses, useful for starting other programs
from cryptography.fernet import \
    Fernet  # Provides encryption and decryption functionality using Fernet symmetric encryption
import random
from datetime import date


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1370x700+0+0")
        self.root.title("Inventory management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # Load the encryption key and initialize the cipher
        self.cipher = self.load_key_and_initialize_cipher()

        # Title Bar
        self.icon_title = PhotoImage(file="images/logo1.png")  # Load the application logo
        # Create a label for the title bar, combining the icon and the title text
        Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
              font=("Elephant", 40, "bold"), bg="#02457A", fg="white", anchor="w", padx=20).place(x=0, y=0,
                                                                                                  relwidth=1,
                                                                                                  height=70)

        # Logout Button
        Button(self.root, text="Logout", command=self.logout,
               font=("Elephant", 15, "bold"), bg="#D32F2F", fg="white",
               # Styling the button with bold text and red background
               cursor="hand2", relief='raised', borderwidth=2,
               # Making the button raised with a hand cursor for a clickable effect
               highlightthickness=0).place(x=1150, y=10, height=50,
                                           width=150)  # Positioning the button on the top right

        # Clock Display
        self.lbl_clock = Label(self.root,
                               text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS",
                               font=("Elephant", 15), bg="#34515e", fg="white",
                               # Styling with specific font, background and text color
                               anchor='center')  # Ensuring the text is centered
        self.lbl_clock.place(x=0, y=70, relwidth=1,
                             height=30)  # Placing the label across the width of the window just below the title bar

        # ====Product_frame==========
        # Create a frame for displaying all products
        product_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        product_frame1.place(x=6, y=110, width=410, height=550)

        # Create a title label for the product frame with updated styling
        title_label = Label(product_frame1, text="All Products", font=("Arial", 20, "bold"), bg="#333", fg="white",
                            padx=10, pady=5)
        title_label.pack(side=TOP, fill=X)

        # ======Product Search Frame===============
        # Create a StringVar for search
        self.var_search = StringVar()

        # Create a frame for search options
        product_frame2 = Frame(product_frame1, bd=2, relief=RIDGE, bg="white")
        product_frame2.place(x=2, y=42, width=398, height=90)

        # Define the search label within the product frame.
        # This label acts as a prompt for users, indicating where to enter the product name for searching.
        Label(product_frame2, text="Search Product | By Name ", font=("times new roman", 15, "bold"),
              bg="white", fg="green").place(x=2, y=5)

        # This label is used as a static placeholder to indicate the field's purpose, i.e., to enter a product name.
        # Entry widget for entering the search term.
        # Users can type the product name here to search in the database.
        # It uses a 'light yellow' background for the entry field to make it visually distinct.
        Entry(product_frame2, textvariable=self.var_search,
              font=("times new roman", 15), bg="light yellow").place(
            x=128, y=47, width=150, height=22)
        # Button to initiate the search based on the entered product name.
        # Clicking this button will trigger the 'search' method in the application.
        Button(product_frame2, text="Search", command=self.search, font=("goudy old style", 15),
               bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)

        # Button to display all products.
        # This is used to reset or clear the search filter and show all entries in the database.
        Button(product_frame2, text="Show All", command=self.show, font=("goudy old style", 15),
               bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        # ====Product_frame==========
        # Create a frame for displaying all products
        product_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        product_frame1.place(x=6, y=110, width=410, height=550)

        # Create a title label for the product frame with updated styling
        title_label = Label(product_frame1, text="All Products", font=("Arial", 20, "bold"), bg="#333", fg="white",
                            padx=10, pady=5)
        title_label.pack(side=TOP, fill=X)

        # ======Product Search Frame===============
        # Create a StringVar for search
        self.var_search = StringVar()

        # Create a frame for search options
        product_frame2 = Frame(product_frame1, bd=2, relief=RIDGE, bg="white")
        product_frame2.place(x=2, y=42, width=398, height=90)

        # Label for search
        lbl_search = Label(product_frame2, text="Search Product | By Name ", font=("Arial", 15, "bold"),
                           bg="white", fg="green")
        lbl_search.place(x=2, y=5)

        # Label and Entry for entering product name
        lbl_product_name = Label(product_frame2, text="Product", font=("Arial", 15, "bold"), bg="white")
        lbl_product_name.place(x=5, y=45)
        txt_product_name = Entry(product_frame2, textvariable=self.var_search, font=("Arial", 15), bg="light yellow")
        txt_product_name.place(x=128, y=47, width=150, height=22)

        # Buttons for search and show all products
        btn_search = Button(product_frame2, text="Lookup", command=self.search, font=("Arial", 12), bg="#2196f3",
                            fg="white", cursor="hand2")
        btn_search.place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(product_frame2, text="Show All", command=self.show, font=("Arial", 12), bg="#083531",
                              fg="white", cursor="hand2")
        btn_show_all.place(x=285, y=10, width=100, height=25)

        # ======Product Details Frame===============
        product_frame3 = Frame(product_frame1, bd=3, relief=RIDGE)
        product_frame3.place(x=2, y=140, width=398, height=375)

        # Scrollbars for the product table
        scroll_y = Scrollbar(product_frame3, orient=VERTICAL)
        scroll_x = Scrollbar(product_frame3, orient=HORIZONTAL)

        # Create the treeview widget for product details
        self.product_Table = ttk.Treeview(product_frame3, columns=("pid", "name", "price", "qty", "status"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)  # Horizontal scrollbar
        scroll_y.pack(side=RIGHT, fill=Y)  # Vertical scrollbar
        scroll_x.config(command=self.product_Table.xview)  # Connect horizontal scrollbar to treeview
        scroll_y.config(command=self.product_Table.yview)  # Connect vertical scrollbar to treeview

        # Configure column headings
        self.product_Table.heading("pid", text="PID.")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")

        self.product_Table["show"] = "headings"  # Only show headings, not the default column

        # Define column widths
        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)

        self.product_Table.pack(fill=BOTH, expand=1)  # Pack to make the table visible
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)  # Bind a function to item selection

        # Note label for additional instructions
        lbl_note = Label(product_frame1, text="Note: 'Enter 0 Quantity to remove product from the cart'",
                         font=("Arial", 12), anchor='w', bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)  # Display note at the bottom of the frame

        # ========CustomerFrame==============
        # Define StringVars for customer name and contact
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        # Create a frame for customer details
        customer_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customer_frame.place(x=420, y=110, width=530, height=70)

        # Title label for the customer frame
        c_title = Label(customer_frame, text="Customer Details", font=("Arial", 15), bg="lightgray")
        c_title.pack(side=TOP, fill=X)

        # Labels and entry fields for customer name and contact
        lbl_name = Label(customer_frame, text="Name", font=("Arial", 12), bg="white")
        lbl_name.place(x=5, y=35)
        txt_name = Entry(customer_frame, textvariable=self.var_cname, font=("Arial", 10), bg="light yellow")
        txt_name.place(x=80, y=35, width=180)

        lbl_contact = Label(customer_frame, text="Contact No", font=("Arial", 12), bg="white")
        lbl_contact.place(x=270, y=35)
        txt_contact = Entry(customer_frame, textvariable=self.var_contact, font=("Arial", 10), bg="light yellow")
        txt_contact.place(x=380, y=35, width=140)

        # # Create a frame for calculations and cart management
        # cal_cart_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        # cal_cart_frame.place(x=420, y=190, width=530, height=360)
        #
        # # Create a frame within cal_cart_frame for adding notes
        # notes_frame = Frame(cal_cart_frame, bd=4, relief=RIDGE, bg="white")
        # notes_frame.place(x=5, y=10, width=245, height=342)
        #
        # # Label for notes section
        # lbl_notes = Label(notes_frame, text="Delivery Notes", font=("Arial", 15, "bold"), bg="#333", fg="white")
        # lbl_notes.pack(side=TOP, fill=X)
        #
        # # Text area for entering notes
        # self.txt_notes = Text(notes_frame, font=('Arial', 12), bd=5, relief=GROOVE)
        # self.txt_notes.pack(expand=True, fill=BOTH, padx=5, pady=5)
        #
        # # Optionally, add a scrollbar for the text area
        # scroll_notes = Scrollbar(notes_frame, command=self.txt_notes.yview)
        # scroll_notes.pack(side=RIGHT, fill=Y)
        # self.txt_notes.config(yscrollcommand=scroll_notes.set)

        # Set up a main frame for additional functionalities in the billing system, such as adding notes.
        cal_cart_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_frame.place(x=420, y=190, width=530, height=360)

        # Create a specific frame within the main cart management frame for entering delivery notes.
        notes_frame = Frame(cal_cart_frame, bd=4, relief=RIDGE, bg="white")
        notes_frame.place(x=5, y=10, width=245, height=342)  # Positioned to allow space for future additions

        # Add a label at the top of the notes frame to clearly indicate this section is for delivery notes.
        lbl_notes = Label(notes_frame, text="Delivery Notes", font=("Arial", 15, "bold"), bg="#333", fg="white")
        lbl_notes.pack(side=TOP, fill=X)  # Fill the width of the frame for clear visibility

        # Initialize a text area for inputting delivery notes, allowing multiple lines of text.
        self.txt_notes = Text(notes_frame, font=('Arial', 12), bd=5, relief=GROOVE)
        self.txt_notes.pack(expand=True, fill=BOTH, padx=5, pady=5)  # Make the text area expandable and fill the frame

        # Implement a vertical scrollbar to the text area to facilitate navigation through longer notes.
        scroll_notes = Scrollbar(notes_frame, command=self.txt_notes.yview)
        scroll_notes.pack(side=RIGHT, fill=Y)  # Attach the scrollbar to the right side of the notes area
        self.txt_notes.config(yscrollcommand=scroll_notes.set)  # Ensure the scrollbar adjusts with text area content

        '''
        Calculator was removed and instead a notes section is given for adding delivery notes as per feedback
        # Calculator frame styling and function
        # Define StringVar for calculator input
        self.var_cal_input = StringVar()

        # Create a frame for the calculator
        cal_frame = Frame(cal_cart_frame, bd=9, relief=RIDGE, bg="white")
        cal_frame.place(x=5, y=10, width=268, height=340)

        # Entry field for calculator input
        txt_cal_input = Entry(cal_frame, textvariable=self.var_cal_input, font=('Arial', 15, 'bold'), width=21, bd=10,
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        # Define buttons for calculator operations
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('c', 4, 1), ('=', 4, 2), ('/', 4, 3)
        ]

        # Function to handle button clicks and update calculator input
        def button_click(value):
            current_input = self.var_cal_input.get()
            if value == 'c':
                self.var_cal_input.set('')
            elif value == '=':
                try:
                    result = eval(current_input)
                    self.var_cal_input.set(result)
                except:
                    self.var_cal_input.set("Error")
            else:
                self.var_cal_input.set(current_input + value)

        # Create buttons for calculator operations
        for (text, row, column) in buttons:
            # Set padding for all buttons in the last row to be the same
            pady_val = 15 if text in ('0', 'c', '=', '/') else 10
            Button(cal_frame, text=text, font=('Arial', 15, 'bold'), command=lambda t=text: button_click(t), bd=5,
                   width=4, pady=pady_val, cursor='hand2').grid(row=row, column=column)
        '''

        # Cart frame styling and setup
        cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE, bg="white")
        cart_frame.place(x=280, y=8, width=245, height=342)

        # Title label for the cart frame
        self.cartTitle = Label(cart_frame, text="Cart \t Total Product:[0]", font=("Arial", 15), bg="#333", fg="white",
                               padx=10, pady=5)
        self.cartTitle.pack(side=TOP, fill=X)

        # Scrollbars for the cart table
        scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient=HORIZONTAL)

        # Treeview for displaying cart items
        self.CartTable = ttk.Treeview(cart_frame, columns=("pid", "name", "price", "qty"),
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CartTable.xview)
        scroll_y.config(command=self.CartTable.yview)

        # Set headings for columns in the cart table
        self.CartTable.heading("pid", text="PID.")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")

        self.CartTable["show"] = "headings"

        # Set column widths for the cart table
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #======ADD Cart Widgets Frame===============
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_qty = StringVar()
        self.var_price = StringVar()
        self.var_stock = StringVar()

        # Initialize the frame for adding cart widgets
        add_cart_widgets_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        add_cart_widgets_frame.place(x=420, y=550, width=530, height=110)

        # Label and entry widget for product name
        lbl_p_name = Label(add_cart_widgets_frame, text="Product Name", font=("Arial", 15), bg="white")
        lbl_p_name.place(x=5, y=5)
        txt_p_name = Entry(add_cart_widgets_frame, textvariable=self.var_pname, font=("Arial", 15),
                           bg="lightyellow", state='readonly')
        txt_p_name.place(x=5, y=35, width=190, height=22)

        # Label and entry widget for price per quantity
        lbl_p_price = Label(add_cart_widgets_frame, text="Price Per Qty", font=("Arial", 15), bg="white")
        lbl_p_price.place(x=230, y=5)
        txt_p_price = Entry(add_cart_widgets_frame, textvariable=self.var_price, font=("Arial", 15),
                            bg="lightyellow", state='readonly')
        txt_p_price.place(x=230, y=35, width=150, height=22)

        # Label and entry widget for quantity
        lbl_p_qty = Label(add_cart_widgets_frame, text="Quantity", font=("Arial", 15), bg="white")
        lbl_p_qty.place(x=390, y=5)
        txt_p_qty = Entry(add_cart_widgets_frame, textvariable=self.var_qty, font=("Arial", 15),
                          bg="lightyellow")
        txt_p_qty.place(x=390, y=35, width=120, height=22)

        # Label for displaying in stock quantity
        self.lbl_inStock = Label(add_cart_widgets_frame, text="In Stock", font=("Arial", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        # Buttons for clearing cart and adding/updating cart
        btn_clear_cart = Button(add_cart_widgets_frame, text="Clear", command=self.clear_cart,
                                font=("Arial", 15, "bold"), bg="lightgray", cursor="hand2")
        btn_clear_cart.place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(add_cart_widgets_frame, text="Add | Update Cart", command=self.add_update_cart,
                              font=("Arial", 15, "bold"), bg="orange", cursor="hand2")
        btn_add_cart.place(x=340, y=70, width=180, height=30)

        #=============Billing Area==================

        # Initialize the frame for the billing area
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        bill_frame.place(x=953, y=110, width=410, height=410)

        # Title label for the billing area
        b_title = Label(bill_frame, text="Customer Bill Area", font=("Arial", 20, "bold"), bg="#f44336",
                       fg="white")
        b_title.pack(side=TOP, fill=X)

        # Scrollbar for the billing area
        scroll_y = Scrollbar(bill_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Text widget for displaying the bill
        self.txt_bill_area = Text(bill_frame, yscrollcommand=scroll_y.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.txt_bill_area.yview)

        #=====================billing buttons============

        # Initialize the frame for the billing menu
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        bill_menu_frame.place(x=953, y=520, width=410, height=140)

        # Label for displaying bill amount
        self.lbl_amt = Label(bill_menu_frame, text='Bill Amount\n [0]', font=("Arial", 15, "bold"),
                             bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        # Label for displaying discount
        self.lbl_discount = Label(bill_menu_frame, text='Discount\n [5%]', font=("Arial", 15, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        # Label for displaying net pay
        self.lbl_net_pay = Label(bill_menu_frame, text='Net Pay\n [0]', font=("Arial", 15, "bold"),
                                 bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        # Button for printing the bill
        btn_print = Button(bill_menu_frame, text='Print', cursor='hand2', command=self.print_bill,
                           font=("Arial", 15, "bold"),
                           bg="#4caf50", fg="white")  # Change button color here
        btn_print.place(x=2, y=80, width=120, height=50)

        # Button for clearing all bill details
        btn_clear_all = Button(bill_menu_frame, text='Clear All', command=self.clear_all, cursor='hand2',
                               font=("Arial", 15, "bold"),
                               bg="#607d8b", fg="white")  # Change button color here
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        # Button for generating or saving the bill
        btn_generate = Button(bill_menu_frame, text='Generate Bill', command=self.generate_bill, cursor='hand2',
                              font=("Arial", 15, "bold"),
                              bg="#009688", fg="white")  # Change button color here
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ==Footer==
        footer_text = "© 2024 IMS | Inventory Management System | Contact Support for Assistance"
        footer_bg = "#263238"  # Dark charcoal grey background for a professional look
        footer_fg = "#FFFFFF"  # White text for contrast
        footer_font = ("Roboto", 14)  # Modern font with a suitable size for readability

        Label(self.root, text=footer_text, font=footer_font, bg=footer_bg, fg=footer_fg).pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    # =======================All Functions==========================

    @staticmethod
    def load_key_and_initialize_cipher():
        """
        Load the encryption key from a file named 'secret.key' and initialize a Fernet cipher object.
        Raises:
            FileNotFoundError: If the 'secret.key' file does not exist.
            Exception: For any issues encountered during key reading or cipher initialization.
        """
        key_path = 'secret.key'
        if not os.path.exists(key_path):
            # Raises an error if the encryption key file does not exist
            raise FileNotFoundError("Encryption key file not found")

        try:
            # Attempt to read the key from the file
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
            # Initialize and return the Fernet cipher object using the loaded key
            return Fernet(key)
        except Exception as e:
            # Handle any exceptions during file reading or cipher initialization
            raise Exception(f"An error occurred while loading the encryption key: {str(e)}")

    def encrypt_data(self, plain_text):
        """
        Encrypts the provided plain text using the initialized cipher and returns the encrypted text.
        If an error occurs during encryption, shows an error message and returns an empty string.

        Args:
            plain_text (str): The text to be encrypted.

        Returns:
            str: The encrypted text in UTF-8 encoding or an empty string if an error occurs.
        """
        if plain_text is None:
            return ""  # Immediately return an empty string if the input is None.

        # Ensure the input is a string to avoid type errors with encryption.
        plain_text = str(plain_text)

        try:
            # Encrypt the text and return the encrypted data decoded to a string for easy handling.
            encrypted_data = self.cipher.encrypt(plain_text.encode('utf-8'))
            return encrypted_data.decode('utf-8')
        except Exception as e:
            # If encryption fails, log the exception and return an empty string.
            messagebox.showerror("Encryption Error", f"Failed to encrypt data: {e}")
            return ""

    def show(self):
        """
        Fetches and displays active product records from the database into the product table.
        Only products with the status 'Active' are fetched and displayed.
        """
        # Establish connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Execute SQL query to retrieve active products
            cur.execute("SELECT pid, name, price, qty, status FROM product WHERE status='Active'")
            rows = cur.fetchall()  # Fetch all matching records

            # Clear previous entries in the product table
            self.product_Table.delete(*self.product_Table.get_children())

            # Populate the table with the active products
            for row in rows:
                self.product_Table.insert('', END, values=row)

        except Exception as ex:
            # Display an error message if an exception occurs during the database operations
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection to avoid resource leaks
            con.close()

    def search(self):
        """
        Searches for products by name in the database that are marked as 'Active'.
        The search is performed safely using parameterized queries to prevent SQL injection.
        """
        # Establish connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Validate that the search input is not empty
            if not self.var_search.get().strip():
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
                return

            # Prepare a parameterized query to find products that match the search criteria and are active
            query = "SELECT pid, name, price, qty, status FROM product WHERE name LIKE ? AND status='Active'"
            cur.execute(query, ('%' + self.var_search.get().strip() + '%',))
            rows = cur.fetchall()

            # Clear the table and repopulate with search results
            self.product_Table.delete(*self.product_Table.get_children())
            if rows:
                for row in rows:
                    self.product_Table.insert('', END, values=row)
            else:
                # Notify the user if no products are found matching the search criteria
                messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            # Display an error message if there's an issue with database operations
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection to free resources
            con.close()

    def get_data(self, ev):
        """
        Retrieves and displays data from the selected row in the product table. It populates form fields
        and initializes certain variables based on the selected product.
        """
        # Focus on the currently selected item in the product table
        focused_item = self.product_Table.focus()

        # Retrieve the item's data dictionary from the focused row
        content = self.product_Table.item(focused_item)

        # Extract the data values from the 'values' key of the dictionary
        row = content.get('values')
        if row:
            # Update form fields and labels with data from the selected row
            self.var_pid.set(row[0])  # Product ID
            self.var_pname.set(row[1])  # Product Name
            self.var_price.set(row[2])  # Product Price
            self.lbl_inStock.config(text=f"In Stock [{row[3]}]")  # Update in-stock label
            self.var_stock.set(row[3])  # Stock Quantity
            self.var_qty.set('1')  # Initialize purchase quantity to 1
        else:
            # Clear all fields or notify the user if no data is found (optional)
            self.clear_cart()  # Assuming there's a method to clear/reset relevant fields

    def get_data_cart(self, ev):
        """
        Retrieves and displays data from the selected row in the cart table.
        Populates corresponding form fields based on the selected item.
        """
        # Retrieve the identifier for the currently focused item in the cart table
        focused_item = self.CartTable.focus()

        # Retrieve the item's data dictionary from the focused row
        content = self.CartTable.item(focused_item)

        # Extract the data values from the 'values' key of the dictionary
        row = content.get('values')
        if row:
            # Update form fields with data from the selected row
            self.var_pid.set(row[0])  # Product ID
            self.var_pname.set(row[1])  # Product Name
            self.var_price.set(row[2])  # Product Price
            self.var_qty.set(row[3])  # Quantity purchased
            self.var_stock.set(row[4])  # Stock Quantity
            self.lbl_inStock.config(text=f"In Stock [{row[4]}]")  # Update the in-stock label
        else:
            # Clear all fields or notify the user if no data is found in the row
            self.clear_cart()  # Assuming there is a method to clear/reset relevant fields

    def add_update_cart(self):
        """
        Adds a new product to the cart or updates an existing one based on the user's selection and input quantity.
        Validates product selection and quantity before proceeding with cart operations.
        """
        # Check if a product has been selected
        if not self.var_pid.get():
            messagebox.showerror('Error', "Please select a product from the list", parent=self.root)
            return

        # Ensure that a quantity has been specified
        elif not self.var_qty.get():
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
            return

        # Validate that the specified quantity does not exceed available stock
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
            return

        # Calculate total price for the entered quantity
        total_price = float(self.var_price.get()) * int(self.var_qty.get())

        # Prepare the cart data for entry or update
        cart_data = [self.var_pid.get(), self.var_pname.get(), self.var_price.get(), self.var_qty.get(),
                     self.var_stock.get()]

        # Check if the product is already in the cart
        for index, item in enumerate(self.cart_list):
            if item[0] == self.var_pid.get():  # Product ID matches
                if int(self.var_qty.get()) == 0:  # Remove product if quantity is zero
                    self.cart_list.pop(index)
                    self.show_cart()
                    self.bill_updates()
                    return
                else:  # Update quantity in the cart
                    op = messagebox.askyesno('Confirm', "Product already in cart. Update quantity?",
                                             parent=self.root)
                    if op:
                        self.cart_list[index][3] = self.var_qty.get()  # Update the quantity in the cart
                        self.show_cart()
                        self.bill_updates()
                    return

        # If product is not in the cart, add it
        self.cart_list.append(cart_data)
        self.show_cart()
        self.bill_updates()

    def bill_updates(self):
        """
        Calculates the total bill amount based on the cart items, applies a discount,
        and updates the billing information on the GUI.
        """
        # Reset totals to ensure calculations start fresh each time this method is called
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0

        # Iterate over the cart list to sum the total bill amount
        for item in self.cart_list:
            # Multiply the price per unit (item[2]) by the quantity (item[3]) and add to the total bill
            self.bill_amt += float(item[2]) * int(item[3])

        # Calculate a 5% discount on the total bill amount
        self.discount = (self.bill_amt * 5) / 100

        # Calculate net payable amount by subtracting the discount from the bill amount
        self.net_pay = self.bill_amt - self.discount

        # Display the calculated bill amount on the GUI
        self.lbl_amt.config(text=f"Bill Amt.\n{str(self.bill_amt)}")

        # Display the net payable amount after discount on the GUI
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")

        # Update the cart title with the total number of products in the cart
        self.cartTitle.config(text=f"Cart \t Total Product: [{len(self.cart_list)}]")

    def show_cart(self):
        """
        Refreshes the display of items in the cart table based on the current contents of the cart list.
        """
        try:
            # Clear the cart table before adding new items
            self.CartTable.delete(*self.CartTable.get_children())

            # Populate the cart table with items from the cart list
            for item in self.cart_list:
                self.CartTable.insert('', END, values=item)

        except Exception as ex:
            # Display an error message if there's an issue updating the cart table
            messagebox.showerror("Error", f"Error updating cart display: {str(ex)}", parent=self.root)

    def get_current_date(self):
        """
        Returns the current date formatted as 'DD-MM-YYYY'.
        """
        return time.strftime("%d-%m-%Y")

    def get_current_time(self):
        """
        Returns the current time formatted as 'HH:MM:SS AM/PM'.
        """
        return time.strftime("%I:%M:%S %p")

    def generate_bill(self):
        """
        Generates a bill from the cart contents, validates customer details, saves the bill to a file,
        and updates the UI to reflect the bill generation status.
        """
        # Check for customer details
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer details are required to generate a bill.", parent=self.root)
            return

        # Ensure there are products in the cart
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Add products to the cart before generating a bill.", parent=self.root)
            return

        # Ask user for confirmation before generating the bill
        if not messagebox.askyesno("Confirm", "Are you sure? Once the bill is generated, it cannot be changed.",
                                       parent=self.root):
            return  # User clicked 'No', so exit the function

        # Prepare the bill content
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()
        self.save_bill_to_database() #Save bill to database

        # Attempt to encrypt the bill content and save it to a file
        try:
            bill_path = f'bill/{str(self.invoice)}.txt'
            with open(bill_path, 'w') as file:
                # Encrypt the bill content for security
                encrypted_data = self.encrypt_data(self.txt_bill_area.get('1.0', END))
                file.write(encrypted_data)
            messagebox.showinfo('Success', "Bill generated and saved successfully.", parent=self.root)
            # Indicate that the bill is ready for printing
            self.chk_print = 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill to a text file: {str(e)}", parent=self.root)

    def save_bill_to_database(self):
        """
        Persists bill data to the database including customer, bill, and item details, ensuring data integrity.
        """
        try:
            # Establish database connection
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            # Encrypt and store customer details
            cur.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (
                self.encrypt_data(self.var_cname.get()),
                self.encrypt_data(self.var_contact.get()),
            ))
            customer_id = cur.lastrowid  # Retrieve new customer ID

            # Insert bill details with current date
            cur.execute("""
                INSERT INTO bills (invoice_number, customer_id, bill_date, total_amount, discount_given, net_amount) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.invoice,
                customer_id,
                self.get_current_date(),
                self.bill_amt,
                self.discount,
                self.net_pay
            ))
            bill_id = cur.lastrowid  # Retrieve new bill ID

            # Process each cart item and insert into bill_items table
            for item in self.cart_list:
                cur.execute("""
                    INSERT INTO bill_items (bill_id, product_id, quantity, price_per_unit, total_price) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    bill_id,
                    item[0],  # Product ID
                    item[3],  # Quantity
                    item[2],  # Price per unit
                    float(item[2]) * int(item[3])  # Calculate total price
                ))

            # Commit transaction to save all changes
            con.commit()
            # messagebox.showinfo("Success", "Bill saved successfully.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving bill data: {str(e)}", parent=self.root)
        finally:
            con.close()  # Ensure closure of database connection

    def bill_top(self):
        """
        Prepares and displays the top section of the bill with customer and transaction details.
        Includes the store name, contact information, customer details, and column headers for the bill items.
        """
        # Generate a unique invoice number combining the current date with a random three-digit number
        self.invoice = f"{time.strftime('%Y%m%d')}{random.randint(100, 999)}"  # Format: YYYYMMDDXXX

        # Define the bill header with consistent visual styling
        bill_top_template = (
                "\tAriatech-Inventory\n"
                "\tPhone Mo. 730573****, Ipswich-IP1 5RA\n"
                + "=" * 48 + "\n"  # Divider to separate header from customer details
                + f"Customer Name: {self.var_cname.get()}\n"  # Display customer name
                + f"Ph No. : {self.var_contact.get()}\n"  # Display customer phone number
                + f"Bill No. {self.invoice}\t\tDate: {self.get_current_date()}\n"  # Display invoice number and date
                + "=" * 48 + "\n"  # Divider to separate customer details from product details
                + "{:<23}{:>3}{:>22}\n".format("Product Name", "QTY", "Price(GBP)")  # Column headers for the bill items
                + "=" * 48 + "\n"  # Divider to mark the start of the bill item listings
        )

        # Insert the top section into the billing area text widget
        self.txt_bill_area.delete('1.0', END)  # Clear existing content
        self.txt_bill_area.insert('1.0', bill_top_template)  # Insert the formatted bill top section

    def bill_bottom(self):
        """
        Appends the bottom section of the bill to the billing area, displaying the total bill amount,
        applied discounts, and the net payable amount. It also includes a section for delivery notes.
        """
        # Define the template for the bill's bottom section, including totals and financial calculations
        bill_bottom_template = (
            f"{'=' * 48}\n"  # Horizontal divider for layout separation
            f"Bill Amount\t\t\t\t\t {self.bill_amt:.2f}\n"  # Display the total amount of the bill
            f"Discount\t\t\t\t\t {self.discount:.2f}\n"  # Display the discount given on the bill
            f"Net Pay\t\t\t\t\t {self.net_pay:.2f}\n"  # Display the net amount payable after discount
            f"{'=' * 48}\n"  # End section with a horizontal divider
            "Delivery Notes:\n"  # Label for the delivery notes section
            f"{self.txt_notes.get('1.0', END)}"  # Insert text from the delivery notes input field
        )

        # Append the bottom section of the bill to the existing content in the billing text area
        self.txt_bill_area.insert(END, bill_bottom_template)

    def bill_middle(self):
        """
        Processes each item in the shopping cart, appending transaction lines to the billing area and updating
        inventory quantities in the database. This function maintains a consistent display format for product names,
        quantities, and prices in the billing section.
        """
        try:
            # Establish a database connection
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            # Iterate over each item in the cart to process billing and inventory updates
            for item in self.cart_list:
                pid = item[0]  # Extract the Product ID from the cart item
                name = item[1]  # Product name, used in the billing display
                qty = item[3]  # Quantity purchased, extracted for billing calculation
                remaining_qty = int(item[4]) - int(qty)  # Calculate remaining stock after sale
                status = 'Active' if remaining_qty > 0 else 'Inactive'  # Determine the new status based on stock level
                price = float(item[2]) * int(qty)  # Calculate the total price for the given quantity

                # Format the billing line item to ensure alignment and readability in the billing area
                formatted_line = "{:<23}{:>3}\t{:>20.2f}\n".format(name, qty, price)
                self.txt_bill_area.insert(END, formatted_line)  # Insert formatted line into the billing text area

                # Update the product's quantity and status in the database based on the sale
                cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?', (remaining_qty, status, pid))

            con.commit()  # Commit all changes to the database
            self.show()  # Refresh the product display to reflect the updated inventory status
        except Exception as ex:
            # Handle any exceptions during the process by displaying an error message
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Ensure the database connection is closed to prevent resource leakage
            con.close()

    def clear_cart(self):
        """
        Clears all product input fields and resets stock information, preparing the GUI for new transactions
        or clearing current data.
        """
        # Reset all related variables to their default state
        self.var_pid.set('')  # Clear product ID
        self.var_pname.set('')  # Clear product name
        self.var_price.set('')  # Reset price field
        self.var_qty.set('')  # Reset quantity field
        self.var_stock.set('')  # Clear stock variable

        # Clear the notes field
        self.txt_notes.delete('1.0', END)  # Clear all content from the Text widget used for notes

        # Update the stock label to indicate no specific stock information
        self.lbl_inStock.config(text="In Stock")

        # Optionally, you can also clear the cart list if needed
        # self.cart_list.clear()
        # self.show_cart()

    def clear_all(self):
        """
        Resets all user inputs and application state to initial conditions. This includes clearing cart items,
        customer details, search fields, and resetting display areas.
        """
        # Clear the cart list and update the cart display
        self.cart_list.clear()
        self.show_cart()

        # Reset customer information fields to their default empty states
        self.var_cname.set('')
        self.var_contact.set('')

        # Clear the billing area to remove any previous bill data
        self.txt_bill_area.delete('1.0', END)

        # Update cart title to reflect an empty cart
        self.cartTitle.config(text="Cart \t Total Product: [0]")

        # Clear search field and reset any search-based displays
        self.var_search.set('')
        self.show()

        # Reset product details and stock information using clear_cart
        self.clear_cart()

    def update_date_time(self):
        """
        Updates the display with the current date and time continuously at specified intervals.
        This helps in keeping the interface dynamically updated with the current system time.
        """

        # Update the clock label with the new time and date, formatted for easy reading
        self.lbl_clock.config(
            text=f"Welcome To Inventory Management System\t\t Date: {self.get_current_date()}\t\t Time: {self.get_current_time()}")

        # Schedule the function to automatically update every 200 milliseconds
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        """
        Initiates the printing process for a generated bill. It checks if a bill has been prepared and,
        using system capabilities, sends the bill to the default printer. Alerts the user if no bill is available to print.
        """
        # Check if the bill has been set to be ready for printing
        if self.chk_print == 1:
            try:
                # Notify the user that printing is starting
                messagebox.showinfo('Print', "Please wait while printing", parent=self.root)

                # Create a temporary file that will automatically delete on close, saving it with a .txt suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as tf:
                    # Write the content of the billing text area to this temporary file
                    tf.write(self.txt_bill_area.get('1.0', END))
                    # Ensure all data is written to the file before proceeding
                    tf.flush()

                # Open the default print dialog to print the file
                os.startfile(tf.name, 'print')
            except Exception as ex:
                # Handle any exceptions during the print operation and show an error message
                messagebox.showerror('Print Error', f"Failed to print bill: {str(ex)}", parent=self.root)
        else:
            # Inform the user to generate a bill first if it has not been set to be ready for printing
            messagebox.showerror('Print', "Please generate bill to print the receipt", parent=self.root)

    def logout(self):
        """
        Destroys the current application window and restarts the login interface.
        """
        try:
            # First, attempt to close the current root window
            self.root.destroy()
            # Then, try to open the login interface using a subprocess
            subprocess.run(["python", "login.py"], check=True)
        except subprocess.CalledProcessError as e:
            # Handle exceptions related to subprocess execution, such as the script not executing correctly
            messagebox.showerror("Logout Failed", f"Failed to start login process: {e}")
        except Exception as e:
            # Handle other potential errors
            messagebox.showerror("Logout Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
