import os  # Importing os module for file operations
import sqlite3  # Importing sqlite3 module for database operations
from tkinter import *
from tkinter import ttk, messagebox  # Importing required modules from tkinter
from CryptoManager import CryptoManagerClass  # Manage Encryption Decryption of text


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

        # Instantiate the CryptoManager for encryption and decryption tasks
        self.crypto_manager = CryptoManagerClass()

        # Initialize tkinter string variables for form handling
        self.var_search = StringVar()  # Variable to handle search mode (by email, name, etc.)
        self.var_search_txt = StringVar()  # Variable to handle the search input text

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

        # Debugging to check if encrypt decrypt working perfectly
        #self.test_encryption_consistency()

        # Search Frame Initialize a LabelFrame widget for employee search operations.
        search_frame = LabelFrame(self.root, text="Search Employee", bg="white", font=("goudy old style", 12, "bold"),
                                  bd=2, relief=RIDGE)
        search_frame.place(x=250, y=20, width=600, height=70)  # Set the frame's position and size on the main window.

        # Search Options
        # Initialize a Combobox within the SearchFrame to allow users to select the criterion for searching employees.
        # It is set to 'readonly' to prevent user-typed entries, ensuring they select from predefined options.
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search,
                                  values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER,
                                  font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)  # Position the combobox within the SearchFrame.
        cmb_search.current(0)  # Set the default selection of the combobox to the first item ("Select").

        # Entry Field for Search Text
        # Set up an entry widget for users to input their search query, configured with a specific font and background color.
        # This widget captures the search text, which is used when the 'Search' button is clicked.
        Entry(search_frame, textvariable=self.var_search_txt, font=("goudy old style", 15),
              bg="lightyellow").place(x=200, y=10)  # Position the entry field within the SearchFrame.

        # Search Button
        # Create a button to initiate the search operation.
        # Clicking this button triggers the 'search' method to perform the search based on the selected criteria and input text.
        Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=410, y=9, width=150, height=30)  # Position the button next to the entry field.

        # Title Label
        # Display a label at the top of the form to indicate the section for Employee Details
        Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(
            x=50, y=100, width=1000)

        # Content: Row 1 - Employee Information
        # Label and entry for Employee ID

        Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        validate_command = self.root.register(lambda input: input.isdigit() or input == "")
        validate_emp_id = Entry(self.root, textvariable=self.var_emp_id, validate="key",
                       validatecommand=(validate_command, '%P'), font=("goudy old style", 15),
                       bg="lightyellow")
        validate_emp_id.place(x=150, y=150, width=180)

        # Label and combobox for selecting Gender
        Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)  # Default to the first entry 'Select'

        # Label and entry for Contact Information

        Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)
        validate_contact = self.root.register(lambda input: input.isdigit() or input in " -")
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15),
              bg="lightyellow",validate="key", validatecommand=(validate_contact, '%P')).place(x=850, y=150, width=180)

        # Content: Row 2 - Additional Employee Information
        # Label and entry for Employee Name
        Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=190, width=180)

        # Label and entry for Employee Date of Birth (D.O.B)
        Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=190, width=180)

        # Label and entry for Employee Date of Joining (D.O.J)
        Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)
        Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(
            x=850, y=190, width=180)

        # Row 3
        Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=230, width=180)
        Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly',
                                 justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        # Row 4
        Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)  # Corrected this line
        validate_salary = self.root.register(lambda input: input.replace('.', '', 1).isdigit() or input == "")
        Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15),
              bg="lightyellow",validate="key", validatecommand=(validate_salary, '%P')).place(x=600, y=270, width=180)

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

    def encrypt_data(self, data):
        """
        Encrypts data using the cryptographic manager's encrypt method.
        """
        return self.crypto_manager.encrypt_data(data)

    def decrypt_data(self, data):
        """
        Decrypts data using the cryptographic manager's decrypt method.
        """
        return self.crypto_manager.decrypt_data(data)

    '''
    Debug function to verify if encrypt decrypt works as it should    
    def test_encryption_consistency(self):
        test_input = "Example Name"
        encrypted_test = self.encrypt_data(test_input)
        decrypted_test = self.decrypt_data(encrypted_test)

        print(f"Original: {test_input}, Encrypted: {encrypted_test}, Decrypted: {decrypted_test}")
    '''

    def add(self):
        """
        Adds a new employee record to the database after validating that the employee ID is unique.
        Ensures all required fields are filled and the employee ID does not already exist in the database.
        """
        missing_fields = []  # List to hold the names of missing fields

        # Check each field and add the field name to the list if it's empty
        if not self.var_emp_id.get().strip():
            missing_fields.append("Employee ID")
        if not self.var_name.get().strip():
            missing_fields.append("Name")
        if not self.var_email.get().strip():
            missing_fields.append("Email")
        if not self.var_gender.get() or self.var_gender.get() == "Select":
            missing_fields.append("Gender")
        if not self.var_contact.get().strip():
            missing_fields.append("Contact")
        if not self.var_dob.get().strip():
            missing_fields.append("D.O.B")
        if not self.var_doj.get().strip():
            missing_fields.append("D.O.J")
        if not self.var_pass.get().strip():
            missing_fields.append("Password")
        if not self.var_utype.get().strip():
            missing_fields.append("User Type")
        if not self.txt_address.get('1.0', END).strip():
            missing_fields.append("Address")
        if not self.var_salary.get().strip():
            missing_fields.append("Salary")

        # If there are any missing fields, show an error message and return
        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)  # Convert list to comma-separated string
            messagebox.showerror("Error", f"Missing fields: {missing_fields_str}", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Check if the employee ID already exists in the database
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                    return

                # Insert the new employee record into the database
                cur.execute(
                    "INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, "
                    "salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        self.var_emp_id.get(),
                        self.encrypt_data(self.var_name.get()),
                        self.encrypt_data(self.var_email.get()),
                        self.var_gender.get(),
                        self.encrypt_data(self.var_contact.get()),
                        self.encrypt_data(self.var_dob.get()),
                        self.var_doj.get(),
                        self.encrypt_data(self.var_pass.get()),
                        self.var_utype.get(),
                        self.encrypt_data(self.txt_address.get('1.0', END).strip()),
                        self.var_salary.get(),
                    ))
                # Commit changes to the database
                con.commit()
                messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                self.show()  # Refresh the display to show the new record
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        """
        Fetches and displays all employee records from the database into the EmployeeTable.
        Sensitive data fields are decrypted before display to ensure confidentiality.
        """
        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM employee")
                rows = cur.fetchall()

                # Clear existing data in the table to ensure it reflects the current database state
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())

                # Populate the EmployeeTable with decrypted data
                for row in rows:
                    decrypted_row = [
                        row[0],  # Employee ID
                        self.decrypt_data(row[1]),  # Name
                        self.decrypt_data(row[2]),  # Email
                        row[3],  # Gender
                        self.decrypt_data(row[4]),  # Contact
                        self.decrypt_data(row[5]),  # Date of Birth
                        row[6],  # Date of Joining
                        self.decrypt_data(row[7]),  # Password
                        row[8],  # User Type
                        self.decrypt_data(row[9]),  # Address
                        row[10]  # Salary
                    ]
                    self.EmployeeTable.insert('', END, values=decrypted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        """
        Retrieves and updates form fields with data from the selected row in the EmployeeTable.
        Enables editing of employee data directly from the selected table entry.
        """
        # Retrieve the currently focused item in the EmployeeTable
        focused_item = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(focused_item)
        row = content['values']

        # Only proceed if the row contains data
        if row:
            # Populate the form fields with the data from the selected row
            self.var_emp_id.set(row[0])  # Employee ID
            self.var_name.set(row[1])  # Name
            self.var_email.set(row[2])  # Email
            self.var_gender.set(row[3])  # Gender
            self.var_contact.set(row[4])  # Contact
            self.var_dob.set(row[5])  # Date of Birth
            self.var_doj.set(row[6])  # Date of Joining
            self.var_pass.set(row[7])  # Password
            self.var_utype.set(row[8])  # User Type
            self.txt_address.delete('1.0', END)  # Clear existing address text
            self.txt_address.insert(END, row[9])  # New Address
            self.var_salary.set(row[10])  # Salary

    def update(self):
        """
        Updates the details of an existing employee in the database based on the provided employee ID.
        It encrypts sensitive data before updating to maintain security.
        """
        if not self.var_emp_id.get():  # Check if the Employee ID field is empty
            messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'ims.db') as con:  # Context manager to handle database connection
                cur = con.cursor()
                # Prepare data for update
                data = (
                    self.encrypt_data(self.var_name.get()),  # Encrypt and update name
                    self.encrypt_data(self.var_email.get()),  # Encrypt and update email
                    self.var_gender.get(),  # Update gender
                    self.encrypt_data(self.var_contact.get()),  # Encrypt and update contact
                    self.var_dob.get(),  # Update date of birth
                    self.var_doj.get(),  # Update date of joining
                    self.encrypt_data(self.var_pass.get()),  # Encrypt and update password
                    self.var_utype.get(),  # Update user type
                    self.encrypt_data(self.txt_address.get('1.0', END).strip()),  # Encrypt and update address
                    self.var_salary.get(),  # Update salary
                    self.var_emp_id.get(),  # Employee ID for the WHERE clause
                )

                # Execute the SQL command to update the employee details in the database
                cur.execute(
                    "UPDATE employee SET name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, "
                    "address=?, salary=? WHERE eid=?",
                    data)
                con.commit()  # Commit changes to the database
                messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                self.show()  # Refresh the displayed data

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        """
        Deletes an employee record from the database after confirming that the employee ID exists and the user
        confirms the action. Provides feedback on the outcome of the operation.
        """
        if not self.var_emp_id.get():  # Ensure an employee ID is provided
            messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'ims.db') as con:  # Manage the database connection
                cur = con.cursor()
                # Verify the existence of the employee before attempting deletion
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                if not cur.fetchone():
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                    return

                # Ask for confirmation before deletion
                if messagebox.askyesno("Confirm", "Do you really want to delete this employee?", parent=self.root):
                    # Proceed with deleting the employee record
                    cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                    self.clear()  # Clear form fields after deletion
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        """
        Resets all form fields to their default or initial values after operations such as add, update, or delete.
        This prepares the form for new entries or ensures clean slate operations.
        """
        # Reset variables to default values
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")  # Default for dropdown
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")  # Default user type
        self.var_salary.set("")
        self.var_search_txt.set("")
        self.var_search.set("Select")  # Default for search dropdown

        # Clear address field
        self.txt_address.delete('1.0', END)  # Remove all content from the address text field

    # Search for data based on user input
    @staticmethod
    def search():

        """
            Searches for employee records based on a specified field and input value using encrypted fields.
            Currently, this function is not operational due to the complexity involved with searching encrypted data.

            Current Limitations:
            - The function attempts to perform searches on encrypted fields using Fernet encryption which is not working
              as expected so it has been left in current development.

            Future Enhancements:
            - Investigate alternative approaches such as deterministic encryption or additional searchable encrypted
              or hashed fields specifically designed for search operations. This would enable efficient and secure searching.
            - Implement parameterized queries to prevent SQL injection vulnerabilities.
            - Optimize the function to handle large datasets more efficiently, ensuring that search operations do not
              degrade the performance of the database system.

            Note:
            - This function will be carefully redesigned to ensure both operational effectiveness and security compliance.
            - Future development will focus on addressing the current limitations and testing extensively with different
              scenarios and datasets.

            TODO:
            - Reevaluate the encryption strategy and possibly integrate a more suitable method for searchable encrypted data.
            - Redesign the search interface to accommodate new search methodologies and enhance user interaction.
            """
        messagebox.showinfo("Information",
                            "Search function is currently under development and will be available in future updates.")
        # # Establish a database connection
        # con = sqlite3.connect(database=r'ims.db')
        # cur = con.cursor()
        #
        # try:
        #     # Validate that a search category has been selected
        #     if self.var_search.get() == "Select":
        #         messagebox.showerror("Error", "Select Search By option", parent=self.root)
        #         return
        #     # Ensure that search text has been entered
        #     elif self.var_searctxt.get() == "":
        #         messagebox.showerror("Error", "Search input should be required", parent=self.root)
        #         return
        #
        #     # Encrypt the search input to match encrypted data in the database
        #     encrypted_search_input = self.encrypt_data(self.var_searctxt.get())
        #     # Prepare SQL query with encrypted data
        #     query = f"SELECT * FROM employee WHERE {self.var_search.get()} = ?"
        #     parameters = (encrypted_search_input,)
        #
        #     print(f"Executing query: {query} with parameters {parameters}")  # Debugging output
        #     cur.execute(query, parameters)
        #     rows = cur.fetchall()
        #     print(f"Number of rows returned: {len(rows)}")  # Debugging output
        #
        #     # Check if any results were found
        #     if len(rows) != 0:
        #         # Clear the existing table entries
        #         self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        #         # Insert each found row into the table after decrypting relevant fields
        #         for row in rows:
        #             decrypted_row = [
        #                 row[0], self.decrypt_data(row[1]), self.decrypt_data(row[2]), row[3],
        #                 self.decrypt_data(row[4]), row[5], row[6], self.decrypt_data(row[7]), row[8],
        #                 self.decrypt_data(row[9]), row[10]
        #             ]
        #             self.EmployeeTable.insert('', END, values=decrypted_row)
        #     else:
        #         # Inform user if no records are found
        #         messagebox.showerror("Error", "No record found", parent=self.root)
        # except Exception as ex:
        #     # Handle any exceptions during the search operation
        #     print(f"Error during database operation: {ex}")  # Debugging output
        #     messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
