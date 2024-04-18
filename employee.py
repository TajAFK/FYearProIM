import os  # Importing os module for file operations
import sqlite3  # Importing sqlite3 module for database operations
from tkinter import *
from tkinter import ttk, messagebox  # Importing required modules from tkinter

from cryptography.fernet import Fernet  # Importing Fernet for encryption


class EmployeeClass:
    def __init__(self, root):
        """
        Initialize the main application window with necessary GUI components and data handling setup.
        """
        # Basic window setup
        self.root = root
        self.root.geometry("1100x500+220+130")  # Set the size and position of the window
        self.root.title("Inventory Management System")  # Set the window title
        self.root.config(bg="white")  # Set the background color of the window
        self.root.focus_force()  # Set focus on the main window to capture all keyboard inputs

        # Encryption setup
        self.key = Fernet.generate_key()  # Generate a secure encryption key
        self.cipher = Fernet(self.key)  # Create a cipher object for encrypting and decrypting
        self.cipher = self.load_key_and_initialize_cipher()  # Load existing key if available, else generate new

        # Initialize tkinter string variables for form handling
        self.var_search = StringVar()  # Variable to handle search mode (by email, name, etc.)
        self.var_searctxt = StringVar()  # Variable to handle the search input text

        # Employee data variables
        self.var_emp_id = StringVar()  # Employee ID
        self.var_gender = StringVar()  # Gender
        self.var_contact = StringVar()  # Contact number
        self.var_name = StringVar()  # Employee name
        self.var_dob = StringVar()  # Date of birth
        self.var_doj = StringVar()  # Date of joining
        self.var_email = StringVar()  # Email address
        self.var_pass = StringVar()  # Password for login or system access
        self.var_utype = StringVar()  # User type (e.g., Admin, Employee)
        self.var_salary = StringVar()  # Salary

        # Search Frame
        # Initialize a LabelFrame widget for employee search operations. This frame is designed with a white background and
        # bold font, enhancing its visibility on the interface. It is positioned centrally with specific dimensions.
        SearchFrame = LabelFrame(self.root, text="Search Employee", bg="white", font=("goudy old style", 12, "bold"),
                                 bd=2, relief=RIDGE)
        SearchFrame.place(x=250, y=20, width=600, height=70)  # Set the frame's position and size on the main window.

        # Search Options
        # Initialize a Combobox within the SearchFrame to allow users to select the criterion for searching employees.
        # It is set to 'readonly' to prevent user-typed entries, ensuring they select from predefined options.
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_search,
                                  values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER,
                                  font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)  # Position the combobox within the SearchFrame.
        cmb_search.current(0)  # Set the default selection of the combobox to the first item ("Select").

        # Entry Field for Search Text
        # Set up an entry widget for users to input their search query, configured with a specific font and background color.
        # This widget captures the search text, which is used when the 'Search' button is clicked.
        Entry(SearchFrame, textvariable=self.var_searctxt, font=("goudy old style", 15),
              bg="lightyellow").place(x=200, y=10)  # Position the entry field within the SearchFrame.

        # Search Button
        # Create a button to initiate the search operation. The button is styled with a green background and white text.
        # Clicking this button triggers the 'search' method to perform the search based on the selected criteria and input text.
        Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=410, y=9, width=150, height=30)  # Position the button next to the entry field.

        # Title Label
        # Display a label at the top of the form to indicate the section for Employee Details, using a contrasting color scheme.
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(
            x=50, y=100, width=1000)  # Set the position and width to span across the window for visibility.

        # Content: Row 1 - Employee Information
        # Label and entry for Employee ID
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15),
                          bg="lightyellow").place(x=150, y=150, width=180)

        # Label and combobox for selecting Gender
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)  # Default to the first entry 'Select'

        # Label and entry for Contact Information
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15),
                            bg="lightyellow").place(x=850, y=150, width=180)

        # Content: Row 2 - Additional Employee Information
        # Label and entry for Employee Name
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=190, width=180)

        # Label and entry for Employee Date of Birth (D.O.B)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=190, width=180)

        # Label and entry for Employee Date of Joining (D.O.J)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(
            x=850, y=190, width=180)

        # Row 3
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly',
                                 justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        # Row 4
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)  # Corrected this line
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15),
                           bg="lightyellow").place(x=600, y=270, width=180)

        # Buttons
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white",
               cursor="hand2").place(
            x=740, y=305, width=110, height=28)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white",
               cursor="hand2").place(
            x=860, y=305, width=110, height=28)

        # Employee Details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=(
            "eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        # Set headings for the table
        self.EmployeeTable.heading("eid", text="Emp ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        # Set column widths
        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        # Show initial data in the table
        self.show()

    @staticmethod
    def load_key_and_initialize_cipher():
        key_path = 'secret.key'
        if not os.path.exists(key_path):
            # Generate a key and save it to a file
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
        else:
            # Load the key from the file
            with open(key_path, 'rb') as key_file:
                key = key_file.read()

        return Fernet(key)

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
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.var_emp_id.get(),
                            self.encrypt_data(self.var_name.get()),
                            self.encrypt_data(self.var_email.get()),
                            self.var_gender.get(),
                            self.encrypt_data(self.var_contact.get()),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.encrypt_data(self.var_pass.get()),
                            self.var_utype.get(),
                            self.encrypt_data(self.txt_address.get('1.0', END).strip()),
                            self.var_salary.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Show data in the table
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                decrypted_row = [row[0], self.decrypt_data(row[1]), self.decrypt_data(row[2]), row[3],
                                 self.decrypt_data(row[4]), row[5], row[6], self.decrypt_data(row[7]), row[8],
                                 self.decrypt_data(row[9]), row[10]]
                self.EmployeeTable.insert('', END, values=decrypted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Get data from the table and fill the form fields
    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']
        if row:
            self.var_emp_id.set(str(row[0]))
            self.var_name.set(str(row[1]))  # No decryption needed if already decrypted
            self.var_email.set(str(row[2]))
            self.var_gender.set(str(row[3]))
            self.var_contact.set(str(row[4]))
            self.var_dob.set(str(row[5]))
            self.var_doj.set(str(row[6]))
            self.var_pass.set(str(row[7]))
            self.var_utype.set(str(row[8]))
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, str(row[9]))  # Direct insertion
            self.var_salary.set(str(row[10]))

    # Update existing data in the database
    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute(
                    "UPDATE employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? WHERE eid=?",
                    (
                        self.encrypt_data(self.var_name.get()),
                        self.encrypt_data(self.var_email.get()),
                        self.var_gender.get(),
                        self.encrypt_data(self.var_contact.get()),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.encrypt_data(self.var_pass.get()),
                        self.var_utype.get(),
                        self.encrypt_data(self.txt_address.get('1.0', END).strip()),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                con.commit()
                messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Delete data from the database
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete")
                    if op:
                        cur.execute("delete from employee where eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Clear all form fields
    def clear(self):
        # Set all the variable fields to their default values
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.var_salary.set("")
        self.var_searctxt.set("")
        self.var_search.set("Select")

        # Clear the address Text field
        self.txt_address.delete('1.0', END)

        # Optionally clear and refresh the table to show all records or leave it as is
        # If there's a need to refresh the view after clearing, uncomment the next line:
        # self.show()

    # Search for data based on user input
    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searctxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                encrypted_search_input = self.encrypt_data(self.var_searctxt.get())
                query = f"SELECT * FROM employee WHERE {self.var_search.get()} = ?"  # Changed LIKE to = for exact match
                parameters = (encrypted_search_input,)
                cur.execute(query, parameters)
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        decrypted_row = [row[0], self.decrypt_data(row[1]), self.decrypt_data(row[2]), row[3],
                                         self.decrypt_data(row[4]), row[5], row[6], self.decrypt_data(row[7]), row[8],
                                         self.decrypt_data(row[9]), row[10]]
                        self.EmployeeTable.insert('', END, values=decrypted_row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
