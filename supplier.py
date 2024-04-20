import os
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from cryptography.fernet import Fernet


class supplierclass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")  # Set the size and position of the window
        self.root.title("Inventory Management System")  # Set the window title
        self.root.config(bg="white")  # Set the background color of the window
        self.root.focus_force()  # Set focus on the main window to capture all keyboard inputs

        # Initialize tkinter string variables for form handling
        self.var_searchby = StringVar()  # Variable to handle search mode (by email, name, etc.)
        self.var_searctxt = StringVar()  # Variable to handle the search input text
        self.var_sup_invoice = StringVar()  # Variable to manage supplier invoice number
        self.var_name = StringVar()  # Variable to manage the name input for various forms
        self.var_contact = StringVar()  # Variable to manage the contact input

        # Load encryption key and initialize the cipher for securing sensitive data
        self.cipher = self.load_key_and_initialize_cipher()

        # Search Frame
        # lbl_search = Label(self.root, text="Invoice No", bg="white", font=("goudy old style", 15))
        # lbl_search.place(x=700, y=80)
        # Entry(self.root, textvariable=self.var_searctxt, font=("goudy old style", 15), bg="lightyellow").place(x=800,
        #                                                                                                        y=80,
        #                                                                                                        width=160)
        # Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white",
        #        cursor="hand2").place(x=980, y=79, width=100, height=28)
        # Search Frame
        # search_frame = Frame(self.root, bg="white")
        # search_frame.place(x=700, y=80)
        #
        # lbl_search = Label(search_frame, text="Invoice No", bg="white", font=("Arial Rounded MT Bold", 14))
        # lbl_search.grid(row=0, column=0, padx=(0, 10))
        #
        # entry_search = Entry(search_frame, textvariable=self.var_searctxt, font=("Arial", 14), bg="lightyellow", bd=1,
        #                      relief="solid",width=15)
        # entry_search.grid(row=0, column=1, padx=(0, 10))
        #
        # search_button = Button(search_frame, text="Search", command=self.search, font=("Arial Rounded MT Bold", 12),
        #                        bg="#4caf50", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
        # search_button.grid(row=0, column=2, padx=(0, 10))

        # Search Frame setup for the application
        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=700, y=80)  # Positioning the frame on the window

        # Label for search input field
        lbl_search = Label(search_frame, text="Invoice No", bg="white", font=("Arial Rounded MT Bold", 14))
        lbl_search.grid(row=0, column=0, padx=(0, 10))  # Grid positioning with padding for better spacing

        # Entry widget for searching by invoice number
        entry_search = Entry(search_frame, textvariable=self.var_searctxt, font=("Arial", 14), bg="lightyellow", bd=1,
                             relief="solid", width=15)
        entry_search.grid(row=0, column=1, padx=(0, 10))  # Grid positioning with padding

        # Button for initiating the search
        search_button = Button(search_frame, text="Search", command=self.search, font=("Arial Rounded MT Bold", 12),
                               bg="#4caf50", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
        search_button.grid(row=0, column=2, padx=(0, 10))  # Grid positioning with padding

        # # Title
        # title = Label(self.root, text="Supplier Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d",
        #               fg="white").place(x=50, y=10, width=1000, height=40)

        # # Title
        # title_frame = Frame(self.root, bg="#0f4d7d")
        # title_frame.place(x=50, y=10, width=1030, height=40)
        #
        # title_label = Label(title_frame, text="Supplier Details", font=("Arial Rounded MT Bold", 24), bg="#0f4d7d",
        #                     fg="white")
        # title_label.pack(fill="both", expand=True)

        # Title frame setup for displaying the section header
        title_frame = Frame(self.root, bg="#0f4d7d")
        title_frame.place(x=50, y=10, width=1030, height=40)  # Position and size of the title frame

        # Title label within the frame for "Supplier Details"
        title_label = Label(title_frame, text="Supplier Details", font=("Arial Rounded MT Bold", 24), bg="#0f4d7d",
                            fg="white")
        title_label.pack(fill="both", expand=True)  # Fill the frame fully with the label, allow expansion

        # # Content
        # lbl_supplier_invoice = Label(self.root, text="Invoice No", font=("goudy old style", 15), bg="white").place(x=50,
        #                                                                                                            y=80)
        # txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15),
        #                              bg="lightyellow").place(x=180, y=80, width=180)
        # lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=120)
        # txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(
        #     x=180, y=120, width=180)
        # lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=50, y=160)
        # txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15),
        #                     bg="lightyellow").place(x=180, y=160, width=180)
        # lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        # self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        # self.txt_desc.place(x=180, y=200, width=470, height=120)
        #
        # # Buttons
        # Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white",
        #        cursor="hand2").place(x=180, y=370, width=110, height=35)
        # Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white",
        #        cursor="hand2").place(x=300, y=370, width=110, height=35)
        # Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white",
        #        cursor="hand2").place(x=420, y=370, width=110, height=35)
        # Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white",
        #        cursor="hand2").place(x=540, y=370, width=110, height=35)

        # # Content
        # lbl_supplier_invoice = Label(self.root, text="Invoice No", font=("Arial Rounded MT Bold", 15), bg="white")
        # lbl_supplier_invoice.place(x=50, y=80)
        #
        # txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("Arial", 14), bg="lightyellow")
        # txt_supplier_invoice.place(x=180, y=80, width=180)
        #
        # lbl_name = Label(self.root, text="Name", font=("Arial Rounded MT Bold", 15), bg="white")
        # lbl_name.place(x=50, y=120)
        #
        # txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 14), bg="lightyellow")
        # txt_name.place(x=180, y=120, width=180)
        #
        # lbl_contact = Label(self.root, text="Contact", font=("Arial Rounded MT Bold", 15), bg="white")
        # lbl_contact.place(x=50, y=160)
        #
        # txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Arial", 14), bg="lightyellow")
        # txt_contact.place(x=180, y=160, width=180)
        #
        # lbl_desc = Label(self.root, text="Description", font=("Arial Rounded MT Bold", 15), bg="white")
        # lbl_desc.place(x=50, y=200)
        #
        # self.txt_desc = Text(self.root, font=("Arial", 14), bg="lightyellow")
        # self.txt_desc.place(x=180, y=200, width=470, height=120)

        # Label and entry for "Invoice No"
        lbl_supplier_invoice = Label(self.root, text="Invoice No", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_supplier_invoice.place(x=50, y=80)
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("Arial", 14), bg="lightyellow")
        txt_supplier_invoice.place(x=180, y=80, width=180)

        # Label and entry for "Name"
        lbl_name = Label(self.root, text="Name", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_name.place(x=50, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 14), bg="lightyellow")
        txt_name.place(x=180, y=120, width=180)

        # Label and entry for "Contact"
        lbl_contact = Label(self.root, text="Contact", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_contact.place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Arial", 14), bg="lightyellow")
        txt_contact.place(x=180, y=160, width=180)

        # Label and text field for "Description"
        lbl_desc = Label(self.root, text="Description", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_desc.place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("Arial", 14), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # # Buttons
        # Button(self.root, text="Save", command=self.add, font=("Arial Rounded MT Bold", 14), bg="#007BFF", fg="white",
        #        cursor="hand2", activebackground="#00B0F0", activeforeground="white").place(x=180, y=370, width=110,
        #                                                                                    height=35)
        # Button(self.root, text="Update", command=self.update, font=("Arial Rounded MT Bold", 14), bg="#28A745",
        #        fg="white", cursor="hand2", activebackground="#34D058", activeforeground="white").place(x=300, y=370,
        #                                                                                                width=110,
        #                                                                                                height=35)
        # Button(self.root, text="Delete", command=self.delete, font=("Arial Rounded MT Bold", 14), bg="#DC3545",
        #        fg="white", cursor="hand2", activebackground="#FF383F", activeforeground="white").place(x=420, y=370,
        #                                                                                                width=110,
        #                                                                                                height=35)
        # Button(self.root, text="Clear", command=self.clear, font=("Arial Rounded MT Bold", 14), bg="#6C757D",
        #        fg="white", cursor="hand2", activebackground="#808B94", activeforeground="white").place(x=540, y=370,
        #                                                                                                width=110,
        #                                                                                                height=35)

        # Button for saving new supplier details
        Button(self.root, text="Save", command=self.add, font=("Arial Rounded MT Bold", 14), bg="#007BFF", fg="white",
               cursor="hand2", activebackground="#00B0F0", activeforeground="white").place(x=180, y=370, width=110,
                                                                                           height=35)

        # Button for updating existing supplier details
        Button(self.root, text="Update", command=self.update, font=("Arial Rounded MT Bold", 14), bg="#28A745",
               fg="white",
               cursor="hand2", activebackground="#34D058", activeforeground="white").place(x=300, y=370, width=110,
                                                                                           height=35)

        # Button for deleting supplier details
        Button(self.root, text="Delete", command=self.delete, font=("Arial Rounded MT Bold", 14), bg="#DC3545",
               fg="white",
               cursor="hand2", activebackground="#FF383F", activeforeground="white").place(x=420, y=370, width=110,
                                                                                           height=35)

        # Button for clearing the form fields
        Button(self.root, text="Clear", command=self.clear, font=("Arial Rounded MT Bold", 14), bg="#6C757D",
               fg="white",
               cursor="hand2", activebackground="#808B94", activeforeground="white").place(x=540, y=370, width=110,
                                                                                           height=35)

        # # Employee Details
        # emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        # emp_frame.place(x=700, y=120, width=380, height=350)
        # scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        # scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        # self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"),
        #                                   yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        # scrollx.pack(side=BOTTOM, fill=X)
        # scrolly.pack(side=RIGHT, fill=Y)
        # scrollx.config(command=self.supplierTable.xview)
        # scrolly.config(command=self.supplierTable.yview)
        # self.supplierTable.heading("invoice", text="Invoice No.")
        # self.supplierTable.heading("name", text="Name")
        # self.supplierTable.heading("contact", text="Contact")
        # self.supplierTable.heading("desc", text="Description")
        # self.supplierTable["show"] = "headings"
        # self.supplierTable.column("invoice", width=90)
        # self.supplierTable.column("name", width=100)
        # self.supplierTable.column("contact", width=100)
        # self.supplierTable.column("desc", width=100)
        # self.supplierTable.pack(fill=BOTH, expand=1)
        # self.supplierTable.bind("<ButtonRelease-1>", self.get_data)
        # self.show()

        # Frame to contain the employee details table
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        # Scrollbars for the table
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        # Treeview table to display supplier details
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        # Setting up the headings and column widths
        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = "headings"
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)  # Binding a function to handle row selection

        # Display the current supplier information in the table
        self.show()

    # Load encryption key from file and initialize cipher
    # @staticmethod
    # def load_key_and_initialize_cipher():
    #     """
    #     Load encryption key from file and initialize cipher.
    #     """
    #     key_path = 'secret.key'
    #     if not os.path.exists(key_path):
    #         raise Exception("Encryption key file not found")
    #     with open(key_path, 'rb') as key_file:
    #         key = key_file.read()
    #     return Fernet(key)

    @staticmethod
    def load_key_and_initialize_cipher():
        """
        Loads the encryption key from a specified file and initializes a Fernet cipher object.
        If the key file does not exist, it raises an informative exception to prevent further operations
        without proper encryption setup.
        """
        key_path = 'secret.key'

        # Check if the encryption key file exists
        if not os.path.exists(key_path):
            raise FileNotFoundError("Encryption key file 'secret.key' not found. Please ensure the key exists.")

        # Read the encryption key from the file
        try:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
        except IOError as e:
            raise IOError(f"Failed to read the encryption key file: {str(e)}")

        # Return the cipher object initialized with the loaded key
        return Fernet(key)

    # Encrypt data using the initialized cipher
    # def encrypt_data(self, plain_text):
    #     if plain_text is None:
    #         return ""
    #     if not isinstance(plain_text, str):
    #         plain_text = str(plain_text)
    #     try:
    #         return self.cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
    #     except Exception as e:
    #         messagebox.showerror("Encryption Error", f"Failed to encrypt data: {e}")
    #         return ""

    def encrypt_data(self, plain_text):
        """
        Encrypts the given plain text using the Fernet cipher.

        Args:
            plain_text (str, optional): The text to be encrypted. If it is not a string,
                                        it will be converted to a string. If None, returns an empty string.

        Returns:
            str: The encrypted text as a base64-encoded string. If encryption fails, returns an empty string.
        """
        # Handle None input gracefully by returning an empty encrypted string
        if plain_text is None:
            return ""

        # Ensure the input is a string, convert if necessary
        if not isinstance(plain_text, str):
            plain_text = str(plain_text)

        try:
            # Encrypt the text and return the ciphertext
            return self.cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            # If encryption fails, log the error and show a messagebox error
            messagebox.showerror("Encryption Error", f"Failed to encrypt data: {e}")
            return ""

    # Decrypt data using the initialized cipher
    # def decrypt_data(self, cipher_text):
    #     if cipher_text is None:
    #         return ""
    #     if not isinstance(cipher_text, str):
    #         cipher_text = str(cipher_text)
    #     try:
    #         return self.cipher.decrypt(cipher_text.encode('utf-8')).decode('utf-8')
    #     except Exception as e:
    #         messagebox.showerror("Decryption Error", f"Failed to decrypt data: {e}")
    #         return ""

    def decrypt_data(self, cipher_text):
        """
        Decrypts the given cipher text using the Fernet cipher.

        Args:
            cipher_text (str, optional): The encrypted text to be decrypted. It should be a string that is base64-encoded.
                                        If not a string, it will be converted to a string. If None, returns an empty string.

        Returns:
            str: The decrypted plain text. If decryption fails, returns an empty string.
        """
        # Handle None input by returning an empty string immediately
        if cipher_text is None:
            return ""

        # Ensure the input is a string, convert if necessary
        if not isinstance(cipher_text, str):
            cipher_text = str(cipher_text)

        try:
            # Decrypt the text and return the plaintext
            return self.cipher.decrypt(cipher_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            # If decryption fails, log the error and show a messagebox error
            messagebox.showerror("Decryption Error", f"Failed to decrypt data: {e}")
            return ""

    # Add data to the database
    # def add(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         if self.var_sup_invoice.get() == "":
    #             messagebox.showerror("Error", "Invoice must be required", parent=self.root)
    #         else:
    #             cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
    #             row = cur.fetchone()
    #             if row is not None:
    #                 messagebox.showerror("Error", "Invoice no already assigned, try different", parent=self.root)
    #             else:
    #                 cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?,?,?,?)",
    #                             (self.var_sup_invoice.get(), self.var_name.get(),
    #                              self.encrypt_data(self.var_contact.get()), self.txt_desc.get('1.0', END).strip()))
    #                 con.commit()
    #                 messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
    #                 self.show()
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def add(self):
        """
        Adds a new supplier record to the database. Ensures that the invoice number is unique
        and all required fields are provided before insertion.
        """
        # Establish a connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Check if the invoice number is provided
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
                return  # Exit the function if no invoice number is provided

            # Check if the invoice number already exists in the database
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Invoice no already assigned, try different", parent=self.root)
                return  # Exit the function if the invoice number is not unique

            # Insert the new supplier record into the database
            cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?,?,?,?)",
                        (self.var_sup_invoice.get(), self.var_name.get(),
                         self.encrypt_data(self.var_contact.get()), self.txt_desc.get('1.0', END).strip()))
            con.commit()  # Commit the transaction to the database
            messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
            self.show()  # Refresh the display to include the new supplier
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()  # Ensure the database connection is always closed

    # Show data in the Treeview
    # def show(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         cur.execute("SELECT * FROM supplier")
    #         rows = cur.fetchall()
    #         self.supplierTable.delete(*self.supplierTable.get_children())
    #         for row in rows:
    #             decrypted_row = list(row)  # Create a mutable copy of the row
    #             decrypted_contact = self.decrypt_data(row[2])  # Decrypt the contact number
    #             decrypted_row[2] = decrypted_contact  # Replace the encrypted contact with decrypted one
    #             self.supplierTable.insert('', END, values=decrypted_row)
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        """
        Fetches and displays all supplier records from the database. Decrypts sensitive information before display.
        Ensures database connections are closed after operation to avoid leaks.
        """
        # Establish a connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Execute the query to fetch all supplier records
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()

            # Clear existing entries in the table to ensure it reflects the current database state
            self.supplierTable.delete(*self.supplierTable.get_children())

            # Insert fetched rows into the table after decrypting sensitive data
            for row in rows:
                # Decrypt contact information in the third column (index 2)
                decrypted_contact = self.decrypt_data(row[2])
                # Replace the encrypted contact data with decrypted data
                decrypted_row = list(row)
                decrypted_row[2] = decrypted_contact
                # Insert the modified row into the table
                self.supplierTable.insert('', END, values=decrypted_row)

        except Exception as ex:
            # Display an error message if any exceptions occur during the operation
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Ensure the database connection is closed to avoid resource leaks
            con.close()

    # def show(self):
    #     """
    #     Fetches and displays all employee records from the database into the EmployeeTable.
    #     Sensitive data fields are decrypted before display to ensure confidentiality.
    #     """
    #     try:
    #         with sqlite3.connect(database=r'ims.db') as con:
    #             cur = con.cursor()
    #             cur.execute("SELECT * FROM supplier")
    #             rows = cur.fetchall()
    #
    #             # Clear existing data in the table to ensure it reflects the current database state
    #             self.supplierTable.delete(*self.supplierTable.get_children())
    #
    #             # Populate the EmployeeTable with decrypted data
    #             for row in rows:
    #                 decrypted_row = [
    #                     row[0],  # Invoice No
    #                     row[1],  # Name
    #                     self.decrypt_data(row[2]),  # Contact
    #                     row[3],  # Description
    #                 ]
    #                 self.supplierTable.insert('', END, values=decrypted_row)
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Get data from Treeview back to the form
    # def get_data(self, ev):
    #     f = self.supplierTable.focus()
    #     content = (self.supplierTable.item(f))
    #     row = content['values']
    #     if row:
    #         self.var_sup_invoice.set(row[0])
    #         self.var_name.set(row[1])
    #         self.var_contact.set(row[2])
    #         self.txt_desc.delete('1.0', END)
    #         self.txt_desc.insert(END, row[3])

    def get_data(self, ev):
        """
        Retrieves data from the selected row in the supplier table and updates the form fields.
        This allows for editing of supplier information.
        """
        # Get the identifier for the currently focused item in the supplier table
        focused_item = self.supplierTable.focus()

        # Retrieve the item's data dictionary from the focused row
        content = self.supplierTable.item(focused_item)

        # Extract the data values from the 'values' key of the dictionary
        row = content.get('values')

        # Check if the row is empty, which happens if no item is selected
        if not row:
            messagebox.showinfo("Selection Required", "Please select a row to load data.", parent=self.root)
            return  # Exit the function if no item is selected

        # Assign the extracted values to the respective variable holders for display in the entry fields
        self.var_sup_invoice.set(row[0])  # Set the Supplier Invoice
        self.var_name.set(row[1])  # Set the Supplier Name
        self.var_contact.set(row[2])  # Contact is already decrypted using show() function
        self.txt_desc.delete('1.0', END)  # Clear existing description
        self.txt_desc.insert(END, row[3])  # Insert the Supplier Description

    # def get_data(self, ev):
    #     """
    #     Retrieves and updates form fields with data from the selected row in the EmployeeTable.
    #     Enables editing of employee data directly from the selected table entry.
    #     """
    #     # Retrieve the currently focused item in the EmployeeTable
    #     focused_item = self.supplierTable.focus()
    #     content = self.supplierTable.item(focused_item)
    #     row = content['values']
    #
    #     # Only proceed if the row contains data
    #     if row:
    #         # Populate the form fields with the data from the selected row
    #         self.var_sup_invoice.set(row[0])  # Employee ID
    #         self.var_name.set(row[1])  # Name
    #
    #         self.var_contact.set(self.decrypt_data(row[2]))  # Decrypt and set the Supplier Contact
    #         self.txt_desc.delete('1.0', END)
    #         self.txt_desc.insert(END, row[3])



    # Update data in the database
    # def update(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         if self.var_sup_invoice.get() == "":
    #             messagebox.showerror("Error", "Invoice no Must be required", parent=self.root)
    #         else:
    #             cur.execute("UPDATE supplier set name=?, contact=?, desc=? WHERE invoice=?",
    #                         (self.var_name.get(), self.encrypt_data(self.var_contact.get()),
    #                          self.txt_desc.get('1.0', END).strip(), self.var_sup_invoice.get()))
    #             con.commit()
    #             messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
    #             self.show()
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def update(self):
        """
        Updates an existing supplier record in the database based on the provided invoice number.
        Ensures that all required fields are filled out before submitting the update.
        Handles exceptions and provides user feedback on operation success or failure.
        """
        # Establish connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Check if the invoice number is provided
            if not self.var_sup_invoice.get().strip():
                messagebox.showerror("Error", "Invoice number must be provided", parent=self.root)
                return  # Early exit if invoice number is missing

            # Execute the update query with parameterized SQL to avoid SQL injection risks
            cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
                        (self.var_name.get(),
                         self.encrypt_data(self.var_contact.get()),  # Encrypt the contact data before updating
                         self.txt_desc.get('1.0', END).strip(),  # Get and strip any leading/trailing whitespace
                         self.var_sup_invoice.get()))

            # Check if the update was successful
            if cur.rowcount == 0:
                messagebox.showerror("Error", "No record found with the specified invoice number", parent=self.root)
                return  # Early exit if no record was updated (invoice not found)

            con.commit()  # Commit changes to the database
            messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
            self.show()  # Refresh the display to show the updated data

        except Exception as ex:
            # Handle any exceptions that occur and show an error message
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Ensure the database connection is closed
            con.close()

    # Delete data from the database
    # def delete(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         if self.var_sup_invoice.get() == "":
    #             messagebox.showerror("Error", "Invoice no must be required", parent=self.root)
    #         else:
    #             cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
    #             row = cur.fetchone()
    #             if row is None:
    #                 messagebox.showerror("Error", "invalid Invoice No", parent=self.root)
    #             else:
    #                 op = messagebox.askyesno("Confirm", "Do you really want to delete")
    #                 if op:
    #                     cur.execute("delete from supplier where invoice=?", (self.var_sup_invoice.get(),))
    #                     con.commit()
    #                     messagebox.showinfo("Delete", "Supplier deleted Successfully", parent=self.root)
    #                     self.clear()
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        """
        Deletes a supplier record from the database using the provided invoice number.
        Checks for the existence of the invoice before deletion and seeks user confirmation.
        """
        # Establish connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Validate that an invoice number has been provided
            if not self.var_sup_invoice.get().strip():
                messagebox.showerror("Error", "Invoice number is required", parent=self.root)
                return  # Exit if no invoice number is provided

            # Check if the invoice exists in the database
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone() is None:
                messagebox.showerror("Error", "Invalid Invoice Number. Please check and try again.", parent=self.root)
                return  # Exit if the invoice does not exist

            # Ask for confirmation before deletion
            if messagebox.askyesno("Confirm", "Do you really want to delete this supplier?"):
                # Proceed with deletion if confirmed
                cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                con.commit()  # Commit the deletion
                messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                self.clear()  # Clear form fields after deletion
                self.show()  # Refresh the list to reflect the deletion

        except Exception as ex:
            # Handle any exceptions and show an error message
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Ensure the database connection is closed
            con.close()

    # Clear form fields
    # def clear(self):
    #     f = self.supplierTable.focus()
    #     content = (self.supplierTable.item(f))
    #     row = content['values']
    #     if row:
    #         self.var_sup_invoice.set("")
    #         self.var_name.set("")
    #         self.var_contact.set("")
    #         self.txt_desc.delete('1.0', END)
    #         self.var_searctxt.set("")
    #         self.show()

    def clear(self):
        """
        Clears all input fields in the supplier form to their default states. This method is used after
        operations such as add, update, or delete, or when the user wants to reset the form for new input.
        """
        # Check if there is a currently focused item in the supplier table
        focused_item = self.supplierTable.focus()
        if focused_item:
            # Clear all form fields
            self.var_sup_invoice.set("")  # Clear the invoice input
            self.var_name.set("")  # Clear the name input
            self.var_contact.set("")  # Clear the contact input
            self.txt_desc.delete('1.0', END)  # Clear the description text box

        # Optionally, clear any search text that might be present
        self.var_searctxt.set("")

        # Refresh the supplier table to reflect the latest data
        self.show()

    # Search for data in the database
    # def search(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         if self.var_searctxt.get() == "":
    #             messagebox.showerror("Error", "Invoice No should be required", parent=self.root)
    #         else:
    #             cur.execute("SELECT * FROM supplier where invoice=?", (self.var_searctxt.get(),))
    #             row = cur.fetchone()
    #             if row is not None:
    #                 self.supplierTable.delete(*self.supplierTable.get_children())
    #                 self.supplierTable.insert('', END, values=row)
    #             else:
    #                 messagebox.showerror("Error", "No record found", parent=self.root)
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        """
        Searches for a supplier record based on the provided invoice number and updates the UI with the result.
        Displays an error if the invoice number field is empty or no records are found.
        """
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Validate input
            if self.var_searctxt.get() == "":
                messagebox.showerror("Error", "Invoice No should be required", parent=self.root)
                return

            # Execute search
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searctxt.get(),))
            row = cur.fetchone()

            # Clear existing entries from the table
            self.supplierTable.delete(*self.supplierTable.get_children())

            if row:
                # Insert the found record into the table
                self.supplierTable.insert('', END, values=row)
            else:
                # Provide feedback if no record is found
                messagebox.showerror("Error", "No record found", parent=self.root)

        except Exception as ex:
            # Handle exceptions and show error messages
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Ensure the database connection is closed
            con.close()


# Entry point of the application
if __name__ == "__main__":
    root = Tk()
    obj = supplierclass(root)
    root.mainloop()
