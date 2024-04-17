from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
import subprocess
from cryptography.fernet import Fernet


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1370x700+0+0")
        self.root.title("Inventory management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # Load the encryption key and initialize the cipher
        self.cipher = self.load_key_and_initialize_cipher()

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

        # ====Product_frame==========
        # Create a frame for displaying all products
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        # Create a title label for the product frame with updated styling
        title_label = Label(ProductFrame1, text="All Products", font=("Arial", 20, "bold"), bg="#333", fg="white",
                            padx=10, pady=5)
        title_label.pack(side=TOP, fill=X)

        # ======Product Search Frame===============
        # Create a StringVar for search
        self.var_search = StringVar()

        # Create a frame for search options
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        # Label for search
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

        # ====Product_frame==========
        # Create a frame for displaying all products
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        # Create a title label for the product frame with updated styling
        title_label = Label(ProductFrame1, text="All Products", font=("Arial", 20, "bold"), bg="#333", fg="white",
                            padx=10, pady=5)
        title_label.pack(side=TOP, fill=X)

        # ======Product Search Frame===============
        # Create a StringVar for search
        self.var_search = StringVar()

        # Create a frame for search options
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        # Label for search
        lbl_search = Label(ProductFrame2, text="Search Product | By Name ", font=("Arial", 15, "bold"),
                           bg="white", fg="green")
        lbl_search.place(x=2, y=5)

        # Label and Entry for entering product name
        lbl_product_name = Label(ProductFrame2, text="Product", font=("Arial", 15, "bold"), bg="white")
        lbl_product_name.place(x=5, y=45)
        txt_product_name = Entry(ProductFrame2, textvariable=self.var_search, font=("Arial", 15), bg="light yellow")
        txt_product_name.place(x=128, y=47, width=150, height=22)

        # Buttons for search and show all products
        btn_search = Button(ProductFrame2, text="Lookup", command=self.search, font=("Arial", 12), bg="#2196f3",
                            fg="white", cursor="hand2")
        btn_search.place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("Arial", 12), bg="#083531",
                              fg="white", cursor="hand2")
        btn_show_all.place(x=285, y=10, width=100, height=25)

        # ======Product Details Frame===============
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        # Scrollbars for the product table
        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        # Create the treeview widget for product details
        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        # Set headings for columns
        self.product_Table.heading("pid", text="PID.")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")

        self.product_Table["show"] = "headings"

        # Set column widths
        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)

        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        # Note label
        lbl_note = Label(ProductFrame1, text="Note: 'Enter  0 Quantity to remove product from the cart' ",
                         font=("Arial", 12), anchor='w', bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)

        #========CustomerFrame==============
        # self.var_cname = StringVar()
        # self.var_contact = StringVar()
        #
        # CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        # CustomerFrame.place(x=420, y=110, width=530, height=70)
        #
        # cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray").pack(
        #     side=TOP, fill=X)
        # lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(
        #     x=5, y=35)
        # txt_name = Entry(CustomerFrame, textvariable=self.var_cname,
        #                  font=("times new roman", 13), bg="light yellow").place(
        #     x=80, y=35, width=180)
        #
        # lbl_contact = Label(CustomerFrame, text="Contact No", font=("times new roman", 15), bg="white").place(
        #     x=270, y=35)
        # txt_contact = Entry(CustomerFrame, textvariable=self.var_contact,
        #                     font=("times new roman", 13), bg="light yellow").place(
        #     x=380, y=35, width=140)

        # ========CustomerFrame==============
        # Customer frame styling and setup
        # Define StringVars for customer name and contact
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        # Create a frame for customer details
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        # Title label for the customer frame
        cTitle = Label(CustomerFrame, text="Customer Details", font=("Arial", 15), bg="lightgray")
        cTitle.pack(side=TOP, fill=X)

        # Labels and entry fields for customer name and contact
        lbl_name = Label(CustomerFrame, text="Name", font=("Arial", 12), bg="white")
        lbl_name.place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("Arial", 10), bg="light yellow")
        txt_name.place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact No", font=("Arial", 12), bg="white")
        lbl_contact.place(x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("Arial", 10), bg="light yellow")
        txt_contact.place(x=380, y=35, width=140)

        # ======Cal Cart Frame===============
        Cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_cart_Frame.place(x=420, y=190, width=530, height=360)

        # ======Calculator Frame===============
        # self.var_cal_input = StringVar()
        #
        # cal_Frame = Frame(Cal_cart_Frame, bd=9, relief=RIDGE, bg="white")
        # cal_Frame.place(x=5, y=10, width=268, height=340)
        #
        # txt_cal_input = Entry(cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=21, bd=10,
        #                       relief=GROOVE, state='readonly', justify=RIGHT)
        # txt_cal_input.grid(row=0, columnspan=4)
        #
        # btn_7 = Button(cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda: self.get_input(7), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(row=1, column=0)
        # btn_8 = Button(cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda: self.get_input(8), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=1, column=1)
        # btn_9 = Button(cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda: self.get_input(9), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=1, column=2)
        # btn_sum = Button(cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5,
        #                  width=4, pady=10, cursor='hand2').grid(
        #     row=1, column=3)
        #
        # btn_4 = Button(cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda: self.get_input(4), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=2, column=0)
        # btn_5 = Button(cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda: self.get_input(5), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=2, column=1)
        # btn_6 = Button(cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda: self.get_input(6), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=2, column=2)
        # btn_sub = Button(cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda: self.get_input('-'), bd=5,
        #                  width=4, pady=10, cursor='hand2').grid(
        #     row=2, column=3)
        #
        # btn_1 = Button(cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda: self.get_input(1), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=3, column=0)
        # btn_2 = Button(cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda: self.get_input(2), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=3, column=1)
        # btn_3 = Button(cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda: self.get_input(3), bd=5,
        #                width=4, pady=10, cursor='hand2').grid(
        #     row=3, column=2)
        # btn_mul = Button(cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda: self.get_input('*'), bd=5,
        #                  width=4, pady=10, cursor='hand2').grid(
        #     row=3, column=3)
        #
        # btn_0 = Button(cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda: self.get_input(0), bd=5,
        #                width=4, pady=15, cursor='hand2').grid(
        #     row=4, column=0)
        # btn_c = Button(cal_Frame, text='c', font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=15,
        #                cursor='hand2').grid(
        #     row=4, column=1)
        # btn_eq = Button(cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4,
        #                 pady=15, cursor='hand2').grid(
        #     row=4, column=2)
        # btn_div = Button(cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda: self.get_input('/'), bd=5,
        #                  width=4, pady=15, cursor='hand2').grid(
        #     row=4, column=3)

        # Calculator frame styling and function
        # Define StringVar for calculator input
        self.var_cal_input = StringVar()

        # Create a frame for the calculator
        cal_Frame = Frame(Cal_cart_Frame, bd=9, relief=RIDGE, bg="white")
        cal_Frame.place(x=5, y=10, width=268, height=340)

        # Entry field for calculator input
        txt_cal_input = Entry(cal_Frame, textvariable=self.var_cal_input, font=('Arial', 15, 'bold'), width=21, bd=10,
                              relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        # Define buttons for calculator operations
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('c', 4, 1), ('=', 4, 2), ('/', 4, 3)
        ]

        # Function to handle button clicks and update calculator input
        def button_click(value):
            current_input = self.var_cal_input.get()
            if value == 'c':
                self.var_cal_input.set('')
            elif value == '=':
                try:
                    result = eval(current_input)
                    self.var_cal_input.set(result)
                except:
                    self.var_cal_input.set("Error")
            else:
                self.var_cal_input.set(current_input + value)

        # Create buttons for calculator operations
        for (text, row, column) in buttons:
            # Set padding for all buttons in the last row to be the same
            pady_val = 15 if text in ('0', 'c', '=', '/') else 10
            Button(cal_Frame, text=text, font=('Arial', 15, 'bold'), command=lambda t=text: button_click(t), bd=5,
                   width=4, pady=pady_val, cursor='hand2').grid(row=row, column=column)

        # ======Cart Frame===============
        # cart_Frame = Frame(Cal_cart_Frame, bd=3, relief=RIDGE)
        # cart_Frame.place(x=280, y=8, width=245, height=342)
        #
        # self.cartTitle = Label(cart_Frame, text="Cart \t Total Product:[0]", font=("goudy old style", 15),
        #                        bg="lightgray")
        # self.cartTitle.pack(side=TOP, fill=X)
        #
        # scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        # scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)
        #
        # self.CartTable = ttk.Treeview(cart_Frame, columns=(
        #     "pid", "name", "price", "qty"),
        #                               yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        # scrollx.pack(side=BOTTOM, fill=X)
        # scrolly.pack(side=RIGHT, fill=Y)
        # scrollx.config(command=self.CartTable.xview)
        # scrolly.config(command=self.CartTable.yview)
        #
        # self.CartTable.heading("pid", text="PID.")
        # self.CartTable.heading("name", text="Name")
        # self.CartTable.heading("price", text="Price")
        # self.CartTable.heading("qty", text="QTY")
        #
        # self.CartTable["show"] = "headings"
        #
        # self.CartTable.column("pid", width=40)
        # self.CartTable.column("name", width=90)
        # self.CartTable.column("price", width=90)
        # self.CartTable.column("qty", width=40)
        #
        # self.CartTable.pack(fill=BOTH, expand=1)
        # self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # Cart frame styling and setup
        cart_Frame = Frame(Cal_cart_Frame, bd=3, relief=RIDGE, bg="white")
        cart_Frame.place(x=280, y=8, width=245, height=342)

        # Title label for the cart frame
        self.cartTitle = Label(cart_Frame, text="Cart \t Total Product:[0]", font=("Arial", 15), bg="#333", fg="white",
                               padx=10, pady=5)
        self.cartTitle.pack(side=TOP, fill=X)

        # Scrollbars for the cart table
        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        # Treeview for displaying cart items
        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        # Set headings for columns in the cart table
        self.CartTable.heading("pid", text="PID.")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")

        self.CartTable["show"] = "headings"

        # Set column widths for the cart table
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #======ADD Cart Widgets Frame===============
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_qty = StringVar()
        self.var_price = StringVar()
        self.var_stock = StringVar()

        # Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        # Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)
        #
        # lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(
        #     x=5, y=5)
        # txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
        #                    bg="lightyellow", state='readonly').place(x=5,
        #                                                              y=35, width=190, height=22)
        #
        # lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(
        #     x=230, y=5)
        # txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
        #                     bg="lightyellow", state='readonly').place(x=230,
        #                                                               y=35, width=150, height=22)
        #
        # lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(
        #     x=390, y=5)
        # txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
        #                   bg="lightyellow").place(x=390,
        #                                           y=35, width=120, height=22)
        #
        # self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        # self.lbl_inStock.place(x=5, y=70)
        #
        # btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart,
        #                         font=("times new roman", 15, "bold"),
        #                         bg="lightgray", cursor="hand2").place(x=180, y=70, width=150, height=30)
        # btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart,
        #                       font=("times new roman", 15, "bold"),
        #                       bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        # Initialize the frame for adding cart widgets
        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        # Label and entry widget for product name
        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("Arial", 15), bg="white")
        lbl_p_name.place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("Arial", 15),
                           bg="lightyellow", state='readonly')
        txt_p_name.place(x=5, y=35, width=190, height=22)

        # Label and entry widget for price per quantity
        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("Arial", 15), bg="white")
        lbl_p_price.place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("Arial", 15),
                            bg="lightyellow", state='readonly')
        txt_p_price.place(x=230, y=35, width=150, height=22)

        # Label and entry widget for quantity
        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("Arial", 15), bg="white")
        lbl_p_qty.place(x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("Arial", 15),
                          bg="lightyellow")
        txt_p_qty.place(x=390, y=35, width=120, height=22)

        # Label for displaying in stock quantity
        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("Arial", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        # Buttons for clearing cart and adding/updating cart
        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart,
                                font=("Arial", 15, "bold"), bg="lightgray", cursor="hand2")
        btn_clear_cart.place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart,
                              font=("Arial", 15, "bold"), bg="orange", cursor="hand2")
        btn_add_cart.place(x=340, y=70, width=180, height=30)

        #=============Billing Area==================

        # billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        # billFrame.place(x=953, y=110, width=410, height=410)
        #
        # bTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#f44336",
        #                fg="white").pack(side=TOP, fill=X)
        # scrolly = Scrollbar(billFrame, orient=VERTICAL)
        # scrolly.pack(side=RIGHT, fill=Y)
        #
        # self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        # self.txt_bill_area.pack(fill=BOTH, expand=1)
        # scrolly.config(command=self.txt_bill_area.yview)

        # Initialize the frame for the billing area
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=110, width=410, height=410)

        # Title label for the billing area
        bTitle = Label(billFrame, text="Customer Bill Area", font=("Arial", 20, "bold"), bg="#f44336",
                       fg="white")
        bTitle.pack(side=TOP, fill=X)

        # Scrollbar for the billing area
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        # Text widget for displaying the bill
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=====================billing buttons============
        # billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        # billMenuFrame.place(x=953, y=520, width=410, height=140)
        #
        # self.lbl_amt = Label(billMenuFrame, text='Bill Amount\n [0]', font=("goudy old style", 15, "bold"),
        #                      bg="#3f51b5", fg="white")
        # self.lbl_amt.place(x=2, y=5, width=120, height=70)
        #
        # self.lbl_discount = Label(billMenuFrame, text='Discount\n [5%]', font=("goudy old style", 15, "bold"),
        #                           bg="#8bc34a", fg="white")
        # self.lbl_discount.place(x=124, y=5, width=120, height=70)
        #
        # self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n [0]', font=("goudy old style", 15, "bold"),
        #                          bg="#607d8b", fg="white")
        # self.lbl_net_pay.place(x=246, y=5, width=160, height=70)
        #
        # btn_print = Button(billMenuFrame, text='Print', cursor='hand2', command=self.print_bill,
        #                    font=("goudy old style", 15, "bold"),
        #                    bg="lightgreen", fg="white")
        # btn_print.place(x=2, y=80, width=120, height=50)
        #
        # btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, cursor='hand2',
        #                        font=("goudy old style", 15, "bold"),
        #                        bg="gray", fg="white")
        # btn_clear_all.place(x=124, y=80, width=120, height=50)
        #
        # btn_generate = Button(billMenuFrame, text='Generate /Save Bill', command=self.generate_bill, cursor='hand2',
        #                       font=("goudy old style", 15, "bold"),
        #                       bg="#009688", fg="white")
        # btn_generate.place(x=246, y=80, width=160, height=50)

        # Initialize the frame for the billing menu
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        # Label for displaying bill amount
        self.lbl_amt = Label(billMenuFrame, text='Bill Amount\n [0]', font=("Arial", 15, "bold"),
                             bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        # Label for displaying discount
        self.lbl_discount = Label(billMenuFrame, text='Discount\n [5%]', font=("Arial", 15, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        # Label for displaying net pay
        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n [0]', font=("Arial", 15, "bold"),
                                 bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        # Button for printing the bill
        btn_print = Button(billMenuFrame, text='Print', cursor='hand2', command=self.print_bill,
                           font=("Arial", 15, "bold"),
                           bg="#4caf50", fg="white")  # Change button color here
        btn_print.place(x=2, y=80, width=120, height=50)

        # Button for clearing all bill details
        btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, cursor='hand2',
                               font=("Arial", 15, "bold"),
                               bg="#607d8b", fg="white")  # Change button color here
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        # Button for generating or saving the bill
        btn_generate = Button(billMenuFrame, text='Generate Bill', command=self.generate_bill, cursor='hand2',
                              font=("Arial", 15, "bold"),
                              bg="#009688", fg="white")  # Change button color here
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ==Footer==
        footer_text = "© 2024 IMS | Inventory Management System | Contact Support for Assistance"
        footer_bg = "#263238"  # Dark charcoal grey background for a professional look
        footer_fg = "#FFFFFF"  # White text for contrast
        footer_font = ("Roboto", 14)  # Modern font with a suitable size for readability

        Label(self.root, text=footer_text, font=footer_font, bg=footer_bg, fg=footer_fg).pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    # self.bill_top()

    # =======================All Functions==========================
    @staticmethod
    def load_key_and_initialize_cipher():
        """
        Load encryption key from file and initialize cipher.
        """
        key_path = 'secret.key'
        if not os.path.exists(key_path):
            # If key does not exist, handle it appropriately
            raise Exception("Encryption key file not found")
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
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        else:
            # price_cal = float(int(self.var_qty.get()) * float(self.var_price.get()))
            #pid, name, price, qty, status
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

            #===============update cart===========
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1

            if present == 'yes':
                op = messagebox.askyesno('Confirm',
                                         "Product already present\nDo you want to Update | Remove from the Cart List",
                                         parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3] = self.var_qty.get()  #quantity
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0

        for row in self.cart_list:
            self.bill_amt += (float(row[2]) * int(row[3]))  # Assuming row[2] contains the item price
        self.discount = (self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount  # Assuming you want to add 5% of the bill_amt to itself

        # Corrected lines below
        self.lbl_amt.config(text=f"Bill Amt.\n{str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")

    def show_cart(self):

        try:

            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add Product to the Cart!!!", parent=self.root)

        else:
            #=====Bill Top======
            self.bill_top()
            # =====Bill Middle======
            self.bill_middle()
            # =====Bill Bottom======
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.encrypt_data(self.txt_bill_area.get('1.0', END)))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/Save in Backend", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\tAriatech-Inventory
\t Phone Mo. 730573****, Ipswich-IP1 5RA
{str("=" * 47)}
 Customer Name: {self.var_cname.get()}
 Ph No. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=" * 47)}
 Product Name\t\t\tQTY\tPrice
{str("=" * 47)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("=" * 47)}
 Bill Amount\t\t\t\tGBP.{self.bill_amt}
 Discount\t\t\t\tGBP.{self.discount}
 Net Pay\t\t\t\tGBP.{self.net_pay}
{str("=" * 47)}\n          
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:

            for row in self.cart_list:

                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'

                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n " + name + "\t\t\t" + row[3] + "\tGBP. " + price)
                #====Update quantity in product table
                cur.execute('Update product set qty=?,status=? where pid=?', (
                    qty,
                    status,
                    pid

                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        # Fetch current date and time
        current_time = time.strftime("%I:%M:%S %p")  # Format time in 12-hour format with AM/PM
        current_date = time.strftime("%d-%m-%Y")  # Format date in Day-Month-Year format

        # Update the label text
        self.lbl_clock.config(
            text=f"Welcome To Inventory Management System\t\t Date: {current_date}\t\t Time: {current_time}")

        # Call this function again after 200 milliseconds
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror('Print', "Please generate bill to print the receipt", parent=self.root)

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "login.py"], check=True)


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
