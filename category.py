from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class categoryclass:
    def __init__(self, root):
        # Initialize the root window
        self.root = root

        # Set the geometry of the root window
        self.root.geometry("800x450+220+130")

        # Set the title of the root window
        self.root.title("Inventory Management System")

        # Set the background color of the root window
        self.root.config(bg="white")

        # Set the focus to the root window
        self.root.focus_force()

        # Initialize variables
        self.var_cat_id = StringVar()  # Variable for category ID
        self.var_name = StringVar()  # Variable for category name

        # ===== Title =====
        lab_title = Label(self.root, text="Manage Product Category", font=("Arial", 24, "bold"), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE)
        lab_title.pack(side=TOP, fill=X, padx=10, pady=20)

        # === Entry Field ===
        lab_name = Label(self.root, text="Enter Category Name", font=("Arial", 18), bg="white")
        lab_name.place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("Arial", 14), bg="lightyellow")
        txt_name.place(x=50, y=170, width=325)

        # === Buttons ===
        btn_add = Button(self.root, text="ADD", command=self.add, font=("Arial", 12), bg="#4caf50", fg="white",
                         cursor="hand2")
        btn_add.place(x=50, y=220, width=150, height=30)

        btn_delete = Button(self.root, text="DELETE", command=self.delete, font=("Arial", 12), bg="red", fg="white",
                            cursor="hand2")
        btn_delete.place(x=220, y=220, width=150, height=30)

        # Category Details

        # # Create the frame for category table
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=400, y=100, width=380, height=300)

        # Create vertical and horizontal scrollbars
        scroll_y = Scrollbar(cat_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cat_frame, orient=HORIZONTAL)

        # Create the treeview widget for category table
        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scroll_y.set,
                                           xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.category_table.xview)
        scroll_y.config(command=self.category_table.yview)

        # Set headings for columns
        self.category_table.heading("cid", text="C ID")
        self.category_table.heading("name", text="Name")

        # Show only the headings
        self.category_table["show"] = "headings"

        # Set column widths
        self.category_table.column("cid", width=90)
        self.category_table.column("name", width=100)

        # Pack the treeview widget
        self.category_table.pack(fill=BOTH, expand=1)

        # Bind the click event to get data
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        """
        Adds a new category to the database after verifying that the category name does not already exist.
        Displays appropriate messages for errors or success.
        """
        # Establish a connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Ensure a category name has been provided
            if not self.var_name.get():
                messagebox.showerror("Error", "Category name must be required", parent=self.root)
                return

            # Check if the category already exists to prevent duplicates
            cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Category already present, try a different name", parent=self.root)
                return

            # Insert the new category into the database
            cur.execute("INSERT INTO category(name) VALUES(?)", (self.var_name.get(),))
            con.commit()
            messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
            # Refresh the category table to show the newly added category
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection
            con.close()

    def show(self):
        """
        Fetches and displays all category records from the database into the category_table.
        Ensures the latest data is always shown, handles exceptions, and closes database connections properly
        to avoid resource leaks.
        """
        # Establish connection to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Retrieve all category records from the database
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()  # Fetch all rows from the executed query

            # Clear existing entries in the category table to ensure it reflects the current database state
            self.category_table.delete(*self.category_table.get_children())

            # Populate the category table with rows fetched from the database
            for row in rows:
                self.category_table.insert('', END, values=row)  # Insert each row into the table

            # Adjust column settings to center-align the column headers and their contents for better readability
            for col in self.category_table["columns"]:
                self.category_table.heading(col, anchor=CENTER)
                self.category_table.column(col, anchor=CENTER)

        except Exception as ex:
            # Handle any exceptions that occur during the fetch operation
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Ensure the database connection is closed to avoid leaking resources
            con.close()

    def get_data(self, ev):
        """
        Retrieves and populates the form fields with data from the selected row in the category table.
        This method is invoked when a row in the table is selected, allowing the user to view or edit the data.
        """
        # Get the identifier for the currently focused item in the category table
        focused_item = self.category_table.focus()

        # Retrieve the item's data dictionary from the focused row
        content = self.category_table.item(focused_item)

        # Extract the data values from the 'values' key of the dictionary
        row_values = content.get('values')

        # Check if the row is empty, which happens if no item is selected
        if row_values:
            # Assign the extracted values to the respective variable holders for display in the entry fields
            self.var_cat_id.set(row_values[0])  # Set the Category ID from the first column of the row
            self.var_name.set(row_values[1])  # Set the Category Name from the second column of the row
        else:
            # Clear the fields if no row is selected or if an empty part of the table is clicked
            self.var_cat_id.set("")
            self.var_name.set("")
            messagebox.showinfo("Selection", "Please select a valid row from the table.", parent=self.root)

    def delete(self):
        """
        Deletes a selected category from the database after user confirmation. It ensures that the
        category exists and prevents any action if no category is selected. This function uses parameterized
        queries to enhance security and avoid SQL injection.
        """
        # Verify that a category has been selected
        global con
        if not self.var_cat_id.get():
            messagebox.showerror("Error", "Please select a category from the list", parent=self.root)
            return

        # Establish a connection to the database
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()

            # Check for the existence of the category to ensure it can be safely deleted
            cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Selected category does not exist", parent=self.root)
                return

            # Confirm with the user before deletion
            if messagebox.askyesno("Confirm", "Do you really want to delete this category?"):
                # Execute the deletion if confirmed
                cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category deleted successfully", parent=self.root)
                self.show()  # Refresh the list to reflect the deletion

                # Reset the input fields
                self.var_cat_id.set("")
                self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Ensure the database connection is always closed
            con.close()


# Entry point of the program
if __name__ == "__main__":
    # Create the root window
    root = Tk()

    # Instantiate the category class object with the root window as parameter
    obj = categoryclass(root)

    # Start the Tkinter event loop
    root.mainloop()
