from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from tkinter import font


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
        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        # Create the treeview widget for category table
        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set,
                                           xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

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

        # =====images===========

        # self.im1 = Image.open("images/cat.jpg")
        # self.im1 = self.im1.resize((500, 250), Image.Resampling.LANCZOS)
        # self.im1 = ImageTk.PhotoImage(self.im1)
        #
        # self.lbl_im1 = Label(self.root, image=self.im1,bd=2,relief=RAISED)
        # self.lbl_im1.place(x=50, y=220)
        #
        # self.im2 = Image.open("images/category.jpg")
        # self.im2 = self.im2.resize((500, 250), Image.Resampling.LANCZOS)
        # self.im2 = ImageTk.PhotoImage(self.im2)
        #
        # self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        # self.lbl_im2.place(x=580, y=220)

        self.show()

        #=============Functions=====================

    # def add(self):
    #     con = sqlite3.connect(database=r'ims.db')
    #     cur = con.cursor()
    #     try:
    #         if self.var_name.get() == "":
    #             messagebox.showerror("Error", "Category name must be required", parent=self.root)
    #         else:
    #             cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
    #             row = cur.fetchone()
    #             if row is not None:
    #                 messagebox.showerror("Error", "Category already present, try different", parent=self.root)
    #             else:
    #                 cur.execute(
    #                     "INSERT INTO category(name) VALUES(?)",
    #                     (
    #                         self.var_name.get(),
    #                     ))
    #                 con.commit()
    #                 messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
    #                 self.show()
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def add(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check if the category name is provided
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category name must be required", parent=self.root)
            else:
                # Check if the category already exists
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already present, try different", parent=self.root)
                else:
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

        # =================SHOW DATA=================

    def show(self):
        # Connect to the SQLite database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Execute the SQL query to fetch all data from the category table
            cur.execute("SELECT * FROM category")

            # Fetch all rows
            rows = cur.fetchall()

            # Delete any existing data in the treeview widget
            self.category_table.delete(*self.category_table.get_children())

            # Insert the fetched rows into the treeview widget
            for row in rows:
                self.category_table.insert('', END, values=row)

            # Center align the data in the cells
            for col in self.category_table["columns"]:
                self.category_table.heading(col, anchor=CENTER)
                self.category_table.column(col, anchor=CENTER)
        except Exception as ex:
            # Display an error message if an exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        # ====================== Get Data Back to Form =======================

    def get_data(self, ev):
        # Get the focused item in the category table
        focused_item = self.category_table.focus()

        # Get the content of the focused item
        content = self.category_table.item(focused_item)

        # Extract the row values from the content
        row_values = content['values']

        # If row values are found
        if row_values:
            # Set the category ID variable
            self.var_cat_id.set(row_values[0])

            # Set the category name variable
            self.var_name.set(row_values[1])

    def delete(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        try:
            # Check if category ID is empty
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select category from the list", parent=self.root)
            else:
                # Check if the category exists
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()

                # If category does not exist
                if row is None:
                    messagebox.showerror("Error", "Error, Please try again", parent=self.root)
                else:
                    # Confirm deletion
                    op = messagebox.askyesno("Confirm", "Do you really want to delete")
                    if op:
                        # Delete category from database
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()

                        # Show success message
                        messagebox.showinfo("Delete", "Category deleted Successfully", parent=self.root)

                        # Refresh category table
                        self.show()

                        # Reset category ID and name variables
                        self.var_cat_id.set("")
                        self.var_name.set("")  # Reset the var_name variable to an empty string

        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Entry point of the program
if __name__ == "__main__":
    # Create the root window
    root = Tk()

    # Instantiate the category class object with the root window as parameter
    obj = categoryclass(root)

    # Start the Tkinter event loop
    root.mainloop()
