from tkinter import *
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import supplierclass
from category import categoryclass
from product import productclass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time
import subprocess


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory management System")
        self.root.config(bg="white")

        # Title Bar
        self.icon_title = PhotoImage(file="images/logo1.png")
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
        self.MenuLogo = Image.open("images/4998752.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        # Menu Background
        LeftMenu = Frame(self.root, bd=3, relief=RIDGE, bg="#005662")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        # Menu Logo
        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo, bg="#005662")
        lbl_menuLogo.pack(side=TOP, fill=X)

        # Menu Title
        self.icon_side = PhotoImage(file="images/side.png")
        Label(LeftMenu, text="Menu", font=("times new roman", 20, "bold"), bg="#007580", fg="white").pack(side=TOP,
                                                                                                          fill=X)

        # Menu Buttons

        menu_font = ("times new roman", 18, "bold")
        button_bg = "#eeeeee"
        button_fg = "#005662"

        # Define a common style for all buttons
        def create_menu_button(parent, text, command, icon):
            Button(parent, text=text, command=command, image=icon, compound=LEFT, padx=10, pady=10, anchor="w",
                   font=menu_font, bg=button_bg, fg=button_fg, bd=2, relief=RIDGE, cursor="hand2").pack(side=TOP,
                                                                                                        fill=X)

        create_menu_button(LeftMenu, "Employee", self.employee, self.icon_side)
        create_menu_button(LeftMenu, "Supplier", self.supplier, self.icon_side)
        create_menu_button(LeftMenu, "Category", self.category, self.icon_side)
        create_menu_button(LeftMenu, "Product", self.product, self.icon_side)
        create_menu_button(LeftMenu, "Sales", self.sales, self.icon_side)

        # New Label

        self.lbl_employee = Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE,
                                  bg="#34aeeb", fg="white", font=("Roboto", 20, "bold"),
                                  padx=10, pady=10)
        self.lbl_employee.place(x=300, y=120, height=150, width=300)
        self.lbl_employee.config(font=("Roboto", 24, "bold"))  # Making the numbers larger and bolder

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#ff7043", fg="white",
                                  font=("Roboto", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)
        self.lbl_supplier.config(font=("Roboto", 24, "bold"))  # Making the numbers larger and bolder

        self.lbl_category = Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#00bfa5", fg="white",
                                  font=("Roboto", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)
        self.lbl_category.config(font=("Roboto", 24, "bold"))  # Making the numbers larger and bolder

        self.lbl_product = Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#78909c", fg="white",
                                 font=("Roboto", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)
        self.lbl_product.config(font=("Roboto", 24, "bold"))  # Making the numbers larger and bolder

        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#ffca28", fg="white",
                               font=("Roboto", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
        self.lbl_sales.config(font=("Roboto", 24, "bold"))  # Making the numbers larger and bolder

        # ==Footer==
        footer_text = "© 2024 IMS | Inventory Management System | Contact Support for Assistance"
        footer_bg = "#263238"  # Dark charcoal grey background for a professional look
        footer_fg = "#FFFFFF"  # White text for contrast
        footer_font = ("Roboto", 14)  # Modern font with a suitable size for readability

        Label(self.root, text=footer_text, font=footer_font, bg=footer_bg, fg=footer_fg).pack(side=BOTTOM, fill=X)
        self.update_content()  # Ensuring the content update method is still called

    # =========================================================================

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierclass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryclass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productclass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[{str(len(supplier))}]')

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Total Categories\n[{str(len(category))}]')

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[{str(len(employee))}]')

            self.lbl_sales.config(text=f'Total Sales\n[{str(len(os.listdir('bill')))}]')

            # Fetch current date and time
            current_time = time.strftime("%I:%M:%S %p")  # Format time in 12-hour format with AM/PM
            current_date = time.strftime("%d-%m-%Y")  # Format date in Day-Month-Year format

            # Update the label text
            self.lbl_clock.config(
                text=f"Welcome To Inventory Management System\t\t Date: {current_date}\t\t Time: {current_time}")

            # Call this function again after 200 milliseconds
            self.lbl_clock.after(200, self.update_content)

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
