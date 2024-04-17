from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import os

from cryptography.fernet import Fernet


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Load the encryption key and initialize the cipher
        self.cipher = self.load_key_and_initialize_cipher()

        self.bill_list = []
        self.var_invoice = StringVar()

        # =====title========
        lab_title = Label(self.root, text="View Customer Bill", font=("goudy old style", 30), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50, y=100)

        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15),
                            bg="light yellow").place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search", command=self.search, font=("times new roman", 15, "bold"),
                            bg="#2196f3", fg="white",
                            cursor="hand2").place(x=360, y=100, width=120, height=28)

        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("times new roman", 15, "bold"), bg="lightgray",
                           cursor="hand2").place(x=490, y=100, width=120, height=28)

        # ====Bill List======
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # ====Bill Area======
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        # =====title2========
        lab_title2 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="orange",
                           ).pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # ===Image=====
        self.bill_photo = Image.open("images/cat2.jpg")
        self.bill_photo = self.bill_photo.resize((450, 300), Image.Resampling.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=700, y=110)

        self.show()

    # ======================================
    def show(self):
        self.Sales_List.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.Sales_List.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    # def get_data(self):
    #    row=self.Sales_List.curselection()
    #  file_name=self.Sales_List.get(index-)
    # print(file_name)

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

    # def get_data(self, ev):
    #     selected_indices = self.Sales_List.curselection()
    #     if selected_indices:  # Check if there is at least one item selected
    #         index = selected_indices[0]  # Get the index of the first selected item
    #         file_name = self.Sales_List.get(index)  # Retrieve the file name using the index
    #         self.bill_area.delete('1.0', END)  # Clear previous bill area contents
    #         with open(f'bill/{file_name}', 'r') as file:  # Ensuring the file is properly closed after reading
    #             content = file.read()  # Read the whole content of the file
    #             self.bill_area.insert(END, content)  # Insert content into the bill_area
    #     else:
    #         messagebox.showwarning("Warning", "Please select a bill from the list.", parent=self.root)

    def get_data(self, ev):
        selected_indices = self.Sales_List.curselection()
        if selected_indices:
            index = selected_indices[0]
            file_name = self.Sales_List.get(index)
            self.bill_area.delete('1.0', END)
            with open(f'bill/{file_name}', 'r') as file:
                encrypted_content = file.read()
                decrypted_content = self.decrypt_data(encrypted_content)
                self.bill_area.insert(END, decrypted_content)
        else:
            messagebox.showwarning("Warning", "Please select a bill from the list.", parent=self.root)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "invoice Number should be required", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "invalid invoice number", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)


# This block should be at the module level, not inside the class.
if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
