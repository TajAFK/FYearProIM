from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory management System")
        self.root.config(bg="white")
        self.cart_list = []

        # ==title====
        self.icon_title = PhotoImage(file="images/logo1.png")
        Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
              font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0,
                                                                                                         relwidth=1,
                                                                                                         height=70)

        # --button logout====
        Button(self.root, text="Logout", font=("times new roman", 15, "bold"), bg="yellow",
               cursor="hand2").place(x=1150, y=10, height=50, width=150)

        # ==clock==
        self.lbl_clock = Label(self.root,
                               text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ====Product_frame==========

        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)

        # ======Product Search Frame===============
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name ", font=("times new roman", 15, "bold"),
                           bg="white", fg="green").place(x=2, y=5)

        txt_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(
            x=5, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search,
                           font=("times new roman", 15), bg="light yellow").place(
            x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=("goudy old style", 15),
                            bg="#2196f3", fg="white",
                            cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15),
                              bg="#083531", fg="white",
                              cursor="hand2").place(x=285, y=10, width=100, height=25)

        # ======Product Details Frame===============
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=(
            "pid", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="PID.")
        self.product_Table.heading("name", text="Name")

        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")

        self.product_Table["show"] = "headings"

        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)

        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        lbl_note = Label(ProductFrame1, text="Note: 'Enter  0 Quantity to remove product from the cart' ",
                         font=("goudy old style", 12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        #========CustomerFrame==============
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray").pack(
            side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(
            x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname,
                         font=("times new roman", 13), bg="light yellow").place(
            x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact No", font=("times new roman", 15), bg="white").place(
            x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact,
                            font=("times new roman", 13), bg="light yellow").place(
            x=380, y=35, width=140)

        # ======Cal Cart Frame===============
        Cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_cart_Frame.place(x=420, y=190, width=530, height=360)

        # ======Calculator Frame===============
        self.var_cal_input = StringVar()

        cal_Frame = Frame(Cal_cart_Frame, bd=9, relief=RIDGE, bg="white")
        cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10,
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda: self.get_input(7), bd=5,
                       width=4, pady=10, cursor='hand2').grid(row=1, column=0)
        btn_8 = Button(cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda: self.get_input(8), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=1, column=1)
        btn_9 = Button(cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda: self.get_input(9), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=1, column=2)
        btn_sum = Button(cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5,
                         width=4, pady=10, cursor='hand2').grid(
            row=1, column=3)

        btn_4 = Button(cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda: self.get_input(4), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=2, column=0)
        btn_5 = Button(cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda: self.get_input(5), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=2, column=1)
        btn_6 = Button(cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda: self.get_input(6), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=2, column=2)
        btn_sub = Button(cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda: self.get_input('-'), bd=5,
                         width=4, pady=10, cursor='hand2').grid(
            row=2, column=3)

        btn_1 = Button(cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda: self.get_input(1), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=3, column=0)
        btn_2 = Button(cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda: self.get_input(2), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=3, column=1)
        btn_3 = Button(cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda: self.get_input(3), bd=5,
                       width=4, pady=10, cursor='hand2').grid(
            row=3, column=2)
        btn_mul = Button(cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda: self.get_input('*'), bd=5,
                         width=4, pady=10, cursor='hand2').grid(
            row=3, column=3)

        btn_0 = Button(cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda: self.get_input(0), bd=5,
                       width=4, pady=15, cursor='hand2').grid(
            row=4, column=0)
        btn_c = Button(cal_Frame, text='c', font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=15,
                       cursor='hand2').grid(
            row=4, column=1)
        btn_eq = Button(cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4,
                        pady=15, cursor='hand2').grid(
            row=4, column=2)
        btn_div = Button(cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda: self.get_input('/'), bd=5,
                         width=4, pady=15, cursor='hand2').grid(
            row=4, column=3)

        # ======Cart Frame===============
        cart_Frame = Frame(Cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)

        self.cartTitle = Label(cart_Frame, text="Cart \t Total Product:[0]", font=("goudy old style", 15),bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=(
            "pid", "name", "price", "qty", "status"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="PID.")
        self.CartTable.heading("name", text="Name")

        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable.heading("status", text="Status")

        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.column("status", width=90)

        self.CartTable.pack(fill=BOTH, expand=1)
        # self.CartTable.bind("<ButtonRelease-1>", self.get_data)

        #======ADD Cart Widgets Frame===============
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_qty = StringVar()
        self.var_price = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(
            x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
                           bg="lightyellow", state='readonly').place(x=5,
                                                                     y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(
            x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
                            bg="lightyellow", state='readonly').place(x=230,
                                                                      y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(
            x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
                          bg="lightyellow").place(x=390,
                                                  y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", font=("times new roman", 15, "bold"),
                                bg="lightgray", cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart,
                              font=("times new roman", 15, "bold"),
                              bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        #=============Billing Area==================

        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=110, width=410, height=410)

        bTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#f44336",
                       fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=====================billing buttons============
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amt = Label(billMenuFrame, text='Bill Amount\n [0]', font=("goudy old style", 15, "bold"),
                             bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text='Discount\n [5%]', font=("goudy old style", 15, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n [0]', font=("goudy old style", 15, "bold"),
                                 bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text='Print', cursor='hand2', font=("goudy old style", 15, "bold"),
                           bg="lightgreen", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text='Clear All', cursor='hand2', font=("goudy old style", 15, "bold"),
                               bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text='Generate /Save Bill', cursor='hand2',
                              font=("goudy old style", 15, "bold"),
                              bg="#009688", fg="white")
        btn_generate.place(x=246, y=80, width=160, height=50)

        #================Footer====================
        footer = Label(self.root, text="Ariatech Inventory Management System | Developed by Rangesh\n For any queries ",
                       font=("times new roman", 11), bg="#4d636d", fg="white", bd=0, cursor="hand2").pack(side=BOTTOM,
                                                                                                          fill=X)

        self.show()

    # =======================All Functions==========================
    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:

            cur.execute("SELECT pid, name, price, qty, status FROM product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:

            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute(
                    "SELECT pid, name, price, qty, status FROM product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])

        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")

    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
        else:
            price_cal = float(int(self.var_qty.get()) * float(self.var_price.get()))
            #pid, name, price, qty, status
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get()]

            #===============update cart===========
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1

            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update | Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #quantity
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        bill_amt = 0
        net_pay = 0

        for row in self.cart_list:
            bill_amt += float(row[2])  # Assuming row[2] contains the item price

        net_pay = bill_amt-((bill_amt * 5) / 100)  # Assuming you want to add 5% of the bill_amt to itself

        # Corrected lines below
        self.lbl_amt.config(text=f"Bill Amt.\n{str(bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")

    def show_cart(self):

        try:

            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
