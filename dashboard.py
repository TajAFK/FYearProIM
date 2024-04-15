from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
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

        # ==title====
        self.icon_title = PhotoImage(file="images/logo1.png")
        Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
              font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0,
                                                                                                         relwidth=1,
                                                                                                         height=70)

        # --button logout====
        Button(self.root, text="Logout",command=self.logout, font=("times new roman", 15, "bold"), bg="yellow",
               cursor="hand2").place(x=1150, y=10, height=50, width=150)

        # ==clock==
        self.lbl_clock = Label(self.root,
                               text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ====left Menu==
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="images/side.png")
        Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)

        Button(LeftMenu, text="Employee", command=self.employee, image=self.icon_side, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3,
               cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Supplier", command=self.supplier, image=self.icon_side, compound=LEFT, padx=5,
               anchor="w",
               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP,
                                                                                            fill=X)
        Button(LeftMenu, text="Category", command=self.category, image=self.icon_side, compound=LEFT, padx=5, anchor="w",
               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP,
                                                                                            fill=X)
        Button(LeftMenu, text="Product",command=self.product, image=self.icon_side, compound=LEFT, padx=5, anchor="w",
               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP,
                                                                                            fill=X)
        Button(LeftMenu, text="Sales",command=self.sales, image=self.icon_side, compound=LEFT, padx=5, anchor="w",
               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP,
                                                                                            fill=X)
        Button(LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=5, anchor="w",
               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # ===content===
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#ff5722", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total category\n[0]", bd=5, relief=RIDGE, bg="#009688", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#607d8b", fg="white",
                                 font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#ffc107", fg="white",
                               font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # ==footer==
        Label(self.root, text="IMS-Inventory Management System\nFor any Technical issue",
              font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        self.update_content()
    # =========================================================================

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

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
        self.root.destroy()
        subprocess.run(["python", "login.py"], check=True)


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
