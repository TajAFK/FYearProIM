import os
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from cryptography.fernet import Fernet


class supplierclass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # All variables
        self.var_searchby = StringVar()
        self.var_searctxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # Load the encryption key and initialize the cipher
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
        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=700, y=80)

        lbl_search = Label(search_frame, text="Invoice No", bg="white", font=("Arial Rounded MT Bold", 14))
        lbl_search.grid(row=0, column=0, padx=(0, 10))

        entry_search = Entry(search_frame, textvariable=self.var_searctxt, font=("Arial", 14), bg="lightyellow", bd=1,
                             relief="solid",width=15)
        entry_search.grid(row=0, column=1, padx=(0, 10))

        search_button = Button(search_frame, text="Search", command=self.search, font=("Arial Rounded MT Bold", 12),
                               bg="#4caf50", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
        search_button.grid(row=0, column=2, padx=(0, 10))

        # # Title
        # title = Label(self.root, text="Supplier Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d",
        #               fg="white").place(x=50, y=10, width=1000, height=40)

        # Title
        title_frame = Frame(self.root, bg="#0f4d7d")
        title_frame.place(x=50, y=10, width=1030, height=40)

        title_label = Label(title_frame, text="Supplier Details", font=("Arial Rounded MT Bold", 24), bg="#0f4d7d",
                            fg="white")
        title_label.pack(fill="both", expand=True)

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

        # Content
        lbl_supplier_invoice = Label(self.root, text="Invoice No", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_supplier_invoice.place(x=50, y=80)

        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("Arial", 14), bg="lightyellow")
        txt_supplier_invoice.place(x=180, y=80, width=180)

        lbl_name = Label(self.root, text="Name", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_name.place(x=50, y=120)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 14), bg="lightyellow")
        txt_name.place(x=180, y=120, width=180)

        lbl_contact = Label(self.root, text="Contact", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_contact.place(x=50, y=160)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Arial", 14), bg="lightyellow")
        txt_contact.place(x=180, y=160, width=180)

        lbl_desc = Label(self.root, text="Description", font=("Arial Rounded MT Bold", 15), bg="white")
        lbl_desc.place(x=50, y=200)

        self.txt_desc = Text(self.root, font=("Arial", 14), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # Buttons
        Button(self.root, text="Save", command=self.add, font=("Arial Rounded MT Bold", 14), bg="#007BFF", fg="white",
               cursor="hand2", activebackground="#00B0F0", activeforeground="white").place(x=180, y=370, width=110,
                                                                                           height=35)
        Button(self.root, text="Update", command=self.update, font=("Arial Rounded MT Bold", 14), bg="#28A745",
               fg="white", cursor="hand2", activebackground="#34D058", activeforeground="white").place(x=300, y=370,
                                                                                                       width=110,
                                                                                                       height=35)
        Button(self.root, text="Delete", command=self.delete, font=("Arial Rounded MT Bold", 14), bg="#DC3545",
               fg="white", cursor="hand2", activebackground="#FF383F", activeforeground="white").place(x=420, y=370,
                                                                                                       width=110,
                                                                                                       height=35)
        Button(self.root, text="Clear", command=self.clear, font=("Arial Rounded MT Bold", 14), bg="#6C757D",
               fg="white", cursor="hand2", activebackground="#808B94", activeforeground="white").place(x=540, y=370,
                                                                                                       width=110,
                                                                                                       height=35)

        # Employee Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
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
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # Load encryption key from file and initialize cipher
    @staticmethod
    def load_key_and_initialize_cipher():
        """
        Load encryption key from file and initialize cipher.
        """
        key_path = 'secret.key'
        if not os.path.exists(key_path):
            raise Exception("Encryption key file not found")
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        return Fernet(key)

    # Encrypt data using the initialized cipher
    def encrypt_data(self, plain_text):
        if plain_text is None:
            return ""
        if not isinstance(plain_text, str):
            plain_text = str(plain_text)
        try:
            return self.cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt data: {e}")
            return ""

    # Decrypt data using the initialized cipher
    def decrypt_data(self, cipher_text):
        if cipher_text is None:
            return ""
        if not isinstance(cipher_text, str):
            cipher_text = str(cipher_text)
        try:
            return self.cipher.decrypt(cipher_text.encode('utf-8')).decode('utf-8')
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt data: {e}")
            return ""

    # Add data to the database
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice no already assigned, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?,?,?,?)",
                                (self.var_sup_invoice.get(), self.var_name.get(),
                                 self.encrypt_data(self.var_contact.get()), self.txt_desc.get('1.0', END).strip()))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Show data in the Treeview
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                decrypted_row = list(row)  # Create a mutable copy of the row
                decrypted_contact = self.decrypt_data(row[2])  # Decrypt the contact number
                decrypted_row[2] = decrypted_contact  # Replace the encrypted contact with decrypted one
                self.supplierTable.insert('', END, values=decrypted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Get data from Treeview back to the form
    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        if row:
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert(END, row[3])

    # Update data in the database
    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no Must be required", parent=self.root)
            else:
                cur.execute("UPDATE supplier set name=?, contact=?, desc=? WHERE invoice=?",
                            (self.var_name.get(), self.encrypt_data(self.var_contact.get()),
                             self.txt_desc.get('1.0', END).strip(), self.var_sup_invoice.get()))
                con.commit()
                messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Delete data from the database
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "invalid Invoice No", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete")
                    if op:
                        cur.execute("delete from supplier where invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Clear form fields
    def clear(self):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        if row:
            self.var_sup_invoice.set("")
            self.var_name.set("")
            self.var_contact.set("")
            self.txt_desc.delete('1.0', END)
            self.var_searctxt.set("")
            self.show()

    # Search for data in the database
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searctxt.get() == "":
                messagebox.showerror("Error", "Invoice No should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier where invoice=?", (self.var_searctxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Entry point of the application
if __name__ == "__main__":
    root = Tk()
    obj = supplierclass(root)
    root.mainloop()
