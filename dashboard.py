# Standard imports for GUI development using tkinter.
from tkinter import *
from tkinter import messagebox  # Import for easy GUI dialogs like error messages.

# PIL for handling images within the GUI.
from PIL import Image, ImageTk

# Application-specific modules for different sections of the system.
from employee import EmployeeClass  # Handles employee management functionalities.
from supplier import supplierclass  # Manages supplier-related information.
from category import categoryclass  # Manages product categories.
from product import productclass  # Handles product information management.
from billing import BillClass  # Handles billing information management.
from sales import salesClass  # Manages sales transactions.

# SQLite3 for database operations to store and retrieve application data.
import sqlite3

# Time module for handling operations that involve time computations.
import time

# Subprocess module to handle processes like opening files or other programs from the application.
import subprocess


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x750+0+0")
        self.root.title("Inventory management System")
        self.root.config(bg="white")

        # Title Bar
        self.icon_title = PhotoImage(file="images/cart.png")
        Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
              font=("Elephant", 40, "bold"), bg="#02457A", fg="white", anchor="w", padx=20).place(x=0, y=0,
                                                                                                  relwidth=1,
                                                                                                  height=70)

        # Logout Button
        Button(self.root, text="Logout", command=self.logout, font=("Elephant", 15, "bold"), bg="#D32F2F", fg="white",
               cursor="hand2", relief='raised', borderwidth=2,
               highlightthickness=0).place(x=1150, y=10, height=50, width=150)

        # Clock
        self.lbl_clock = Label(self.root,
                               text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS",
                               font=("Elephant", 15,), bg="#34515e", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        '''
        ### Menu Image 4998752 Attribution
        Image by "https://www.freepik.com/free-vector/gradient-accounting-logo-template_12418648.htm#query=account%20logo&position=6&from_view=keyword&track=ais&uuid=a7fde1a3-569a-48a5-a14c-ea7663b3b358"
        
        '''

        # ====left Menu==
        self.Menu_Logo = Image.open("images/accounting.png")
        self.Menu_Logo = self.Menu_Logo.resize((200, 200), Image.Resampling.LANCZOS)
        self.Menu_Logo = ImageTk.PhotoImage(self.Menu_Logo)

        # Menu Background
        left_menu = Frame(self.root, bd=3, relief=RIDGE, bg="#005662")
        left_menu.place(x=0, y=102, width=200, height=665)

        # Menu Logo
        lbl_menu_logo = Label(left_menu, image=self.Menu_Logo, bg="#005662")
        lbl_menu_logo.pack(side=TOP, fill=X)

        # Menu Title
        self.icon_side = PhotoImage(file="images/arrow.png")
        Label(left_menu, text="Menu", font=("times new roman", 20, "bold"), bg="#007580", fg="white").pack(side=TOP,
                                                                                                          fill=X)

        # Menu Buttons

        menu_font = ("times new roman", 18, "bold")
        button_bg = "#eeeeee"
        button_fg = "#005662"

        # Define a common style for all buttons
        def create_menu_button(parent, text, command, icon):
            """
            Create and pack a button with text, icon, and a command in the parent widget.
            """
            Button(parent, text=text, command=command, image=icon, compound=LEFT, padx=10, pady=10, anchor="w",
                   font=menu_font, bg=button_bg, fg=button_fg, bd=2, relief=RIDGE, cursor="hand2").pack(side=TOP,
                                                                                                        fill=X)

        # Creating navigation buttons on the sidebar for various application modules
        create_menu_button(left_menu, "Employee", self.employee, self.icon_side)  # Employee management
        create_menu_button(left_menu, "Supplier", self.supplier, self.icon_side)  # Supplier management
        create_menu_button(left_menu, "Category", self.category, self.icon_side)  # Category management
        create_menu_button(left_menu, "Product", self.product, self.icon_side)  # Product management
        create_menu_button(left_menu, "Billing", self.billing, self.icon_side)  # Billing management
        create_menu_button(left_menu, "Sales", self.sales, self.icon_side)  # Sales records

        # Label for displaying the total number of employees.
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE,
                                  bg="#34aeeb", fg="white", font=("Roboto", 20, "bold"),
                                  padx=10, pady=10)
        self.lbl_employee.place(x=300, y=120, height=150, width=300)
        self.lbl_employee.config(font=("Roboto", 24, "bold"))

        # Label for displaying the total number of suppliers.
        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#ff7043", fg="white",
                                  font=("Roboto", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)
        self.lbl_supplier.config(font=("Roboto", 24, "bold"))

        # Label for displaying the total number of categories.
        self.lbl_category = Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#00bfa5", fg="white",
                                  font=("Roboto", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)
        self.lbl_category.config(font=("Roboto", 24, "bold"))

        # Label for displaying the total number of products.
        self.lbl_product = Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#78909c", fg="white",
                                 font=("Roboto", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)
        self.lbl_product.config(font=("Roboto", 24, "bold"))

        # Label for displaying the total sales count.
        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#ffca28", fg="white",
                               font=("Roboto", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
        self.lbl_sales.config(font=("Roboto", 24, "bold"))

        # ==Footer==
        # Define footer text and styling parameters.
        footer_text = "© 2024 IMS | Inventory Management System | Contact Support for Assistance"
        footer_bg = "#263238"  # Background color for the footer
        footer_fg = "#FFFFFF"  # Text color for the footer
        footer_font = ("Roboto", 14)  # Font settings for the footer

        # Create a label widget for the footer using predefined styling parameters and pack it at the bottom of the window.
        # The footer is stretched horizontally to span the entire width of the window.
        Label(self.root, text=footer_text, font=footer_font, bg=footer_bg, fg=footer_fg).pack(side=BOTTOM, fill=X)

        # Call the update_content function to handle any dynamic updates or initializations after creating the footer.
        self.update_content()

    def employee(self):
        """
        Opens a new window for managing employee data by instantiating the EmployeeClass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = EmployeeClass(self.new_win)  # Instantiate the EmployeeClass in the new window

    def supplier(self):
        """
        Opens a new window for managing supplier information by instantiating the supplierclass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = supplierclass(self.new_win)  # Instantiate the supplierclass in the new window

    def category(self):
        """
        Opens a new window for managing product categories by instantiating the categoryclass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = categoryclass(self.new_win)  # Instantiate the categoryclass in the new window

    def product(self):
        """
        Opens a new window for managing product details by instantiating the productclass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = productclass(self.new_win)  # Instantiate the productclass in the new window

    def billing(self):
        """
        Opens a new window for managing product details by instantiating the productclass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = BillClass(self.new_win)  # Instantiate the Billing Class in the new window

    def sales(self):
        """
        Opens a new window for managing sales transactions by instantiating the salesClass.
        """
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = salesClass(self.new_win)  # Instantiate the salesClass in the new window

    def update_content(self):
        """
        Dynamically updates dashboard metrics and the current date/time display. Fetches and displays counts
        for products, suppliers, categories, employees, and sales from the database.
        """
        try:
            # Connect to the SQLite database and create a cursor object
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()

                # Fetch and update product count
                cur.execute("SELECT COUNT(*) FROM product")
                product_count = cur.fetchone()[0]
                self.lbl_product.config(text=f'Total Product\n[{product_count}]')

                # Fetch and update supplier count
                cur.execute("SELECT COUNT(*) FROM supplier")
                supplier_count = cur.fetchone()[0]
                self.lbl_supplier.config(text=f'Total Suppliers\n[{supplier_count}]')

                # Fetch and update category count
                cur.execute("SELECT COUNT(*) FROM category")
                category_count = cur.fetchone()[0]
                self.lbl_category.config(text=f'Total Categories\n[{category_count}]')

                # Fetch and update employee count
                cur.execute("SELECT COUNT(*) FROM employee")
                employee_count = cur.fetchone()[0]
                self.lbl_employee.config(text=f'Total Employees\n[{employee_count}]')

                # Fetch and update sales count from bill files in the 'bill' directory
                # if to count text bills in folder
                # sales_count = len([f for f in os.listdir('bill') if f.endswith('.txt')])
                # self.lbl_sales.config(text=f'Total Sales\n[{sales_count}]')

                cur.execute("SELECT COUNT(*) FROM bills")
                bills_count = cur.fetchone()[0]
                self.lbl_sales.config(text=f'Total Sales\n[{bills_count}]')

            # Update current time and date display
            current_time = time.strftime("%I:%M:%S %p")
            current_date = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome To Inventory Management System\t\t Date: {current_date}\t\t Time: {current_time}")

            # Schedule the update_content function to run again after 10 seconds
            self.lbl_clock.after(10000, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

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
    obj = IMS(root)
    root.mainloop()
