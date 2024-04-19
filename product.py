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
        self.var_searchby = StringVar()  # Variable for selecting search type
        self.var_searctxt = StringVar()  # Variable for entering search text

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
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)  # Position and size of the frame

        # Title label for the product management section
        title = Label(product_Frame, text="Manage Products Details", font=("Arial Rounded MT Bold", 18), bg="#0f4d7d",
                      fg="white")
        title.pack(side=TOP, fill=X)  # Display the title at the top of the frame, spanning the full width

        # Labels for product attributes in the first column of the product management frame
        lbl_category = Label(product_Frame, text="Category", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_category.place(x=30, y=60)  # Category label

        lbl_supplier = Label(product_Frame, text="Supplier", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_supplier.place(x=30, y=110)  # Supplier label

        lbl_name = Label(product_Frame, text="Name", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_name.place(x=30, y=160)  # Product name label

        lbl_price = Label(product_Frame, text="Price", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_price.place(x=30, y=210)  # Price label

        lbl_quantity = Label(product_Frame, text="Quantity", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_quantity.place(x=30, y=260)  # Quantity label

        lbl_status = Label(product_Frame, text="Status", font=("Arial Rounded MT Bold", 18), bg="white")
        lbl_status.place(x=30, y=310)  # Status label

        # Column 1 Buttons

        Button(product_Frame, text="Save", command=self.add, font=("Arial Rounded MT Bold", 15), bg="#2196f3",
               fg="white",
               cursor="hand2").place(x=10, y=400, width=100, height=40)

        Button(product_Frame, text="Update", command=self.update, font=("Arial Rounded MT Bold", 15), bg="#4caf50",
               fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)

        Button(product_Frame, text="Delete", command=self.delete, font=("Arial Rounded MT Bold", 15), bg="#f44336",
               fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)

        Button(product_Frame, text="Clear", command=self.clear, font=("Arial Rounded MT Bold", 15), bg="#607d8b",
               fg="white",
               cursor="hand2").place(x=340, y=400, width=100, height=40)

        # Column 1(Combo Box)

        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly',
                               justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly',
                               justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_sup.place(x=150, y=110, width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("Arial Rounded MT Bold", 15),
                         bg='lightyellow')
        txt_name.place(x=150, y=160, width=200)

        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("Arial Rounded MT Bold", 15),
                          bg='lightyellow')
        txt_price.place(x=150, y=210, width=200)

        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("Arial Rounded MT Bold", 15),
                        bg='lightyellow')
        txt_qty.place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"),
                                  state='readonly', justify=CENTER, font=("Arial Rounded MT Bold", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # # ====searchFrame====

        search_frame = LabelFrame(self.root, text="Search Products", bg="white",
                                  font=("Arial Rounded MT Bold", 12, "bold"),
                                  bd=2, relief=RIDGE)
        search_frame.place(x=480, y=10, width=600, height=80)

        # ===options====
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_searchby,
                                  values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER,
                                  font=("Arial Rounded MT Bold", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        Entry(search_frame, textvariable=self.var_searctxt, font=("Arial Rounded MT Bold", 15),
              bg="lightyellow").place(x=200, y=10, width=200)

        Button(search_frame, text="Search", command=self.search, font=("Arial Rounded MT Bold", 15), bg="#007BFF",
               fg="white",
               cursor="hand2").place(x=420, y=9, width=150, height=30)

        # ====Product Details======

        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=(
            "pid", "Supplier", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # =====================FETCH DATA=========================================================================

    def fetch_cat_sup(self):
        # Append 'Empty' as the first item in both cat_list and sup_list
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")

        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Fetch category names from the category table
            cur.execute("select name from category")
            cat = cur.fetchall()

            # If there are categories in the database, update cat_list
            if len(cat) > 0:
                # Clear existing category list and add 'Select' as the first item
                del self.cat_list[:]
                self.cat_list.append("Select")

                # Append fetched category names to cat_list
                for i in cat:
                    self.cat_list.append(i[0])

            # Fetch supplier names from the supplier table
            cur.execute("select name from supplier")
            sup = cur.fetchall()

            # If there are suppliers in the database, update sup_list
            if len(sup) > 0:
                # Clear existing supplier list and add 'Select' as the first item
                del self.sup_list[:]
                self.sup_list.append("Select")

                # Append fetched supplier names to sup_list
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            # Display error message if an exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection
            con.close()

    # =====================ADD DATA=========================================================================

    def add(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Check if all fields are filled out
            if (self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or
                    self.var_sup.get() == "Select" or self.var_sup.get() == "" or
                    self.var_name.get() == "" or self.var_price.get() == "" or
                    self.var_qty.get() == "" or self.var_status.get() == ""):
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                # Check if the product already exists
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Product already exists, try a different name", parent=self.root)
                else:
                    # Insert the product into the database
                    cur.execute(
                        "INSERT INTO product(Category, Supplier, name, price, qty, status) VALUES(?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)

                    # Refresh the product list
                    self.show()

        except Exception as ex:
            # Display error message if an exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection
            con.close()

    # =================SHOW DATA=================
    def show(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Execute SQL query to select all rows from the product table
            cur.execute("SELECT * FROM product")

            # Fetch all rows from the result set
            rows = cur.fetchall()

            # Clear existing data in the product table
            self.product_table.delete(*self.product_table.get_children())

            # Insert fetched rows into the product table
            for row in rows:
                self.product_table.insert('', END, values=row)

            # Center align the column headings and data in the product table
            for col in self.product_table["columns"]:
                self.product_table.heading(col, anchor=CENTER)
                self.product_table.column(col, anchor=CENTER)

        except Exception as ex:
            # Display error message if an exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            # Close the database connection
            con.close()

    # ====================== Get Data Back to Form =======================
    def get_data(self, ev):
        # Get the focused item in the product table
        f = self.product_table.focus()

        # Get the content of the focused item
        content = (self.product_table.item(f))

        # Extract the values from the content dictionary
        row = content['values']

        # Update the variables with the values from the selected row
        self.var_pid.set(row[0])  # Product ID
        self.var_cat.set(row[2])  # Category
        self.var_sup.set(row[1])  # Supplier
        self.var_name.set(row[3])  # Name
        self.var_price.set(row[4])  # Price
        self.var_qty.set(row[5])  # Quantity
        self.var_status.set(row[6])  # Status

    # ====================UPDATE DATA======================
    def update(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check if Product ID is provided
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                # Check if the selected Product ID exists in the database
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    # Show error if the Product ID is invalid
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    # Update the product details in the database
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))

                    # Commit the changes to the database
                    con.commit()

                    # Show success message
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)

                    # Update the product table display
                    self.show()
        except Exception as ex:
            # Show error if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check if Product ID is provided
            if self.var_pid.get() == "":
                # Show error if no Product ID is selected
                messagebox.showerror("Error", "Select product from the list", parent=self.root)
            else:
                # Check if the selected Product ID exists in the database
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    # Show error if the Product ID is invalid
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    # Ask for confirmation before deleting the product
                    op = messagebox.askyesno("Confirm", "Do you really want to delete")
                    if op:
                        # Delete the product from the database
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        # Show success message
                        messagebox.showinfo("Delete", "Product deleted Successfully", parent=self.root)
                        # Clear the input fields after deletion
                        self.clear()
        except Exception as ex:
            # Show error if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        # Reset all input fields to default values
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")

        # Reset search fields to default values
        self.var_searctxt.set("")
        self.var_searchby.set("Select")

        # Update the product table with default data
        self.show()

    def search(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check if search criteria and input are provided
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searctxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                # Execute the SQL query based on search criteria and input
                cur.execute(
                    "SELECT * FROM product where " + self.var_searchby.get() + " LIKE '%" + self.var_searctxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    # If records found, delete existing data in product table and insert new records
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Entry point of the program
if __name__ == "__main__":
    # Create a Tkinter root window
    root = Tk()

    # Create an instance of the product class with the root window as its parent
    obj = productclass(root)

    # Start the Tkinter event loop
    root.mainloop()

