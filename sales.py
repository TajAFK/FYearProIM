# Standard library imports
import os
import sqlite3
import subprocess  # If you are using subprocess.run in your code

# Third-party library imports
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

# Tkinter imports for GUI components
from tkinter import (Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, Text,
                     messagebox, StringVar, END, TOP, BOTH, RIGHT, LEFT, X, Y, RIDGE, VERTICAL)


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

        # # =====title========
        # lab_title = Label(self.root, text="View Customer Bill", font=("goudy old style", 30), bg="#184a45",
        #                   fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)
        #
        # lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white").place(x=50, y=100)
        #
        # txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15),
        #                     bg="light yellow").place(x=160, y=100, width=180, height=28)
        #
        # btn_search = Button(self.root, text="Search", command=self.search, font=("times new roman", 15, "bold"),
        #                     bg="#2196f3", fg="white",
        #                     cursor="hand2").place(x=360, y=100, width=120, height=28)
        #
        # btn_clear = Button(self.root, text="Clear",command=self.clear, font=("times new roman", 15, "bold"), bg="lightgray",
        #                    cursor="hand2").place(x=490, y=100, width=120, height=28)

        # Import necessary tkinter modules for GUI development

        # # ==================== GUI Layout and Styling ====================
        # # Title Label - Serves as the main title for the application window.
        # # Uses a bold and large font for prominence with a dark green background and white text for high contrast.
        # lab_title = Label(self.root, text="View Customer Bill", font=("Helvetica", 30, "bold"), bg="#184a45",
        #                   fg="white", bd=3, relief="ridge")
        # lab_title.pack(side=TOP, fill=X, padx=10, pady=20)  # Fill across the top of the window with padding.
        #
        # # Invoice Number Label - Indicates where users should look or enter the invoice number.
        # lbl_invoice = Label(self.root, text="Invoice No.", font=("Arial", 15), bg="white")
        # lbl_invoice.place(x=50, y=100)  # Position near the top but below the title.
        #
        # # Invoice Number Entry - Allows for entry of invoice numbers with a light yellow background to draw attention.
        # txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("Arial", 15), bg="light yellow")
        # txt_invoice.place(x=160, y=100, width=180, height=28)  # Adequate width and height for entry comfort.
        #
        # # Search Button - Initiates a search based on the invoice number entered. Styled with a blue background and white text.
        # btn_search = Button(self.root, text="Search", command=self.search, font=("Arial", 15, "bold"), bg="#2196f3",
        #                     fg="white", cursor="hand2")
        # btn_search.place(x=360, y=100, width=120, height=28)  # Placed next to the entry field for easy access.
        #
        # # Clear Button - Clears the current entries and results. Light gray background denotes a secondary action.
        # btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Arial", 15, "bold"), bg="lightgray",
        #                    cursor="hand2")
        # btn_clear.place(x=490, y=100, width=120, height=28)  # Placed further away from the search button.

        # ============ GUI Layout and Styling ============
        # Main title for the application window.
        lab_title = Label(self.root, text="View Customer Bill", font=("Helvetica", 30, "bold"), bg="#184a45",
                          fg="white", bd=3, relief="ridge")
        lab_title.pack(side=TOP, fill=X, padx=10, pady=20)  # Positioned at the top, spans across the window.

        # Label for invoice number input.
        lbl_invoice = Label(self.root, text="Invoice No.", font=("Arial", 15), bg="white")
        lbl_invoice.place(x=50, y=100)  # Positioned below the title for easy access.

        # Entry field for invoice number.
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("Arial", 15), bg="light yellow")
        txt_invoice.place(x=160, y=100, width=180, height=28)  # Highlighted for visibility and ease of use.

        # Button to trigger invoice search.
        btn_search = Button(self.root, text="Search", command=self.search, font=("Arial", 15, "bold"), bg="#2196f3",
                            fg="white", cursor="hand2")
        btn_search.place(x=360, y=100, width=120, height=28)  # Adjacent to invoice entry for quick actions.

        # Button to clear form and results.
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Arial", 15, "bold"), bg="lightgray",
                           cursor="hand2")
        btn_clear.place(x=490, y=100, width=120, height=28)  # Set apart from search to avoid accidental presses.

        # ==============================================================

        # # ====Bill List======
        # sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        # sales_Frame.place(x=50, y=140, width=200, height=330)
        #
        # scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        # self.Sales_List = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        # scrolly.pack(side=RIGHT, fill=Y)
        # scrolly.config(command=self.Sales_List.yview)
        # self.Sales_List.pack(fill=BOTH, expand=1)
        # self.Sales_List.bind("<ButtonRelease-1>", self.get_data)
        #
        # # ====Bill Area======
        # bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        # bill_Frame.place(x=280, y=140, width=410, height=330)
        #
        # # =====title2========
        # lab_title2 = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="orange",
        #                    ).pack(side=TOP, fill=X)
        #
        # scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        # self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        # scrolly2.pack(side=RIGHT, fill=Y)
        # scrolly2.config(command=self.bill_area.yview)
        # self.bill_area.pack(fill=BOTH, expand=1)
        #
        # # ===Image=====
        # self.bill_photo = Image.open("images/cat2.jpg")
        # self.bill_photo = self.bill_photo.resize((450, 300), Image.Resampling.LANCZOS)
        # self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        #
        # lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        # lbl_image.place(x=700, y=110)
        #
        # self.show()

        # # ==================== Bill List Section ====================
        # # Frame for displaying the list of bills, with a bordered and raised design for emphasis.
        # sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        # sales_Frame.place(x=50, y=140, width=200, height=330)
        #
        # # Scrollbar for the bill list, allowing vertical scrolling.
        # scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        # # Listbox for displaying sales entries, linked to the scrollbar.
        # self.Sales_List = Listbox(sales_Frame, font=("Arial", 15), bg="white", yscrollcommand=scrolly.set)
        # scrolly.pack(side=RIGHT, fill=Y)
        # scrolly.config(command=self.Sales_List.yview)
        # self.Sales_List.pack(fill=BOTH, expand=1)
        # self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # ============ Bill List Section ============
        # Frame for displaying bills with a prominent bordered design.
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)  # Positioned to fit within the main window.

        # Vertical scrollbar to navigate through the list of bills.
        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)

        # Listbox to display sales entries, enabled with vertical scrolling.
        self.Sales_List = Listbox(sales_Frame, font=("Arial", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)  # Align scrollbar to the right of the Listbox.
        scrolly.config(command=self.Sales_List.yview)  # Connect the scrollbar to the Listbox.
        self.Sales_List.pack(fill=BOTH, expand=1)  # Allow the Listbox to expand and fill the frame.

        # Bind the Listbox to an event handler for selection.
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)  # Trigger 'get_data' on item selection.

        # # ==================== Bill Display Area ====================
        # # Frame for displaying the detailed customer bill, also with a bordered and raised design.
        # bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        # bill_Frame.place(x=280, y=140, width=410, height=330)
        #
        # # Title label for the customer bill area, using an orange background to distinguish this section.
        # lab_title2 = Label(bill_Frame, text="Customer Bill Area", font=("Arial", 20, "bold"), bg="orange")
        # lab_title2.pack(side=TOP, fill=X)
        #
        # # Scrollbar for the bill text area to allow vertical scrolling.
        # scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        # # Text area for displaying the bill details, linked to the scrollbar.
        # self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        # scrolly2.pack(side=RIGHT, fill=Y)
        # scrolly2.config(command=self.bill_area.yview)
        # self.bill_area.pack(fill=BOTH, expand=1)

        # ============ Bill Display Area ============
        # Frame for showing detailed customer bills, designed with borders and a raised layout.
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)  # Set dimensions and position on the window.

        # Label for the bill area, styled with an orange background to stand out.
        lab_title2 = Label(bill_Frame, text="Customer Bill Area", font=("Arial", 20, "bold"), bg="orange")
        lab_title2.pack(side=TOP, fill=X)  # Attach to the top of the frame and fill horizontally.

        # Scrollbar to navigate through the bill text area.
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)

        # Text area for displaying bill details, set with a light yellow background for visibility.
        self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)  # Position the scrollbar on the right side, filling vertically.
        scrolly2.config(command=self.bill_area.yview)  # Connect the text area scrolling to the scrollbar.
        self.bill_area.pack(fill=BOTH, expand=1)  # Allow the text area to expand fully within its frame.

        # # ==================== Decorative Image ====================
        # # Load and display an image, resized appropriately, to enhance the GUI's aesthetic appeal.
        # self.bill_photo = Image.open("images/cat2.jpg").resize((450, 300), Image.Resampling.LANCZOS)
        # self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        # lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        # lbl_image.place(x=700, y=110)
        #
        # # Ensure that the initial display is refreshed to show any data.
        # self.show()

        # ============ Decorative Image ============
        # Load and configure an image to enhance the visual appeal of the GUI.
        self.bill_photo = Image.open("images/cat2.jpg").resize((450, 300),
                                                               Image.Resampling.LANCZOS)  # Resize for optimal fit.
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)  # Convert to a format suitable for Tkinter to handle.

        # Label to hold the image, set without a border for a seamless look.
        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=700, y=110)  # Position the image within the root window.

        # Initial display refresh to ensure the image and other data are shown when the program starts.
        self.show()

    # ======================================
    # def show(self):
    #     self.Sales_List.delete(0, END)
    #     for i in os.listdir('bill'):
    #         if i.split('.')[-1] == 'txt':
    #             self.Sales_List.insert(END, i)
    #             self.bill_list.append(i.split('.')[0])

    # def get_data(self):
    #    row=self.Sales_List.curselection()
    #  file_name=self.Sales_List.get(index-)
    # print(file_name)

    # def show(self):
    #     """
    #     Populates the Sales_List widget with .txt files from the 'bill' directory.
    #     Each file represents a bill document, and only the names of text files are added to the list.
    #     This method also updates the bill_list with the base names of these files.
    #     """
    #     # Clear the existing entries in the Sales_List widget
    #     self.Sales_List.delete(0, END)
    #
    #     # Navigate through all files in the 'bill' directory
    #     for filename in os.listdir('bill'):
    #         # Check if the file is a text file based on its extension
    #         if filename.endswith('.txt'):
    #             # Insert the file name into the Sales_List widget
    #             self.Sales_List.insert(END, filename)
    #             # Append the base name of the file (without extension) to the bill_list for later use
    #             self.bill_list.append(filename.rsplit('.', 1)[0])

    def show(self):
        """
        Refreshes the Sales_List widget by listing .txt files from the 'bill' directory.
        Files represent bill documents, and their names are displayed in the list.
        """
        # Empty the Sales_List to prepare for updated entries
        self.Sales_List.delete(0, END)
        self.bill_list = []  # Clear previous list to avoid duplicates

        # Populate Sales_List with text file names from the 'bill' directory
        for filename in os.listdir('bill'):
            if filename.endswith('.txt'):  # Confirm it's a text file
                # Display the file name in the Sales_List widget
                self.Sales_List.insert(END, filename)
                # Store the base name (without extension) in bill_list for reference
                self.bill_list.append(os.path.splitext(filename)[0])

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

    # def get_data(self, ev):
    #     selected_indices = self.Sales_List.curselection()
    #     if selected_indices:
    #         index = selected_indices[0]
    #         file_name = self.Sales_List.get(index)
    #         self.bill_area.delete('1.0', END)
    #         with open(f'bill/{file_name}', 'r') as file:
    #             encrypted_content = file.read()
    #             decrypted_content = self.decrypt_data(encrypted_content)
    #             self.bill_area.insert(END, decrypted_content)
    #     else:
    #         messagebox.showwarning("Warning", "Please select a bill from the list.", parent=self.root)

    # def get_data(self, ev):
    #     """
    #     Fetches and displays the content of the selected bill file.
    #     The content is first decrypted before being displayed in the bill_area widget.
    #     If no file is selected, a warning message is displayed.
    #     """
    #     # Retrieve the current selection from the Sales_List
    #     selected_indices = self.Sales_List.curselection()
    #
    #     if selected_indices:
    #         # Get the index of the first item in the selection
    #         index = selected_indices[0]
    #         # Retrieve the file name from the Sales_List based on the selected index
    #         file_name = self.Sales_List.get(index)
    #
    #         # Clear the existing content in the bill area
    #         self.bill_area.delete('1.0', END)
    #
    #         # Open the selected bill file and read its content
    #         try:
    #             with open(f'bill/{file_name}', 'r') as file:
    #                 encrypted_content = file.read()
    #                 # Decrypt the content read from the file
    #                 decrypted_content = self.decrypt_data(encrypted_content)
    #                 # Insert the decrypted content into the bill area
    #                 self.bill_area.insert(END, decrypted_content)
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Failed to read or decrypt the file: {str(e)}", parent=self.root)
    #     else:
    #         # Display a warning message if no file is selected
    #         messagebox.showwarning("Warning", "Please select a bill from the list.", parent=self.root)

    def get_data(self, ev):
        """
        Retrieves and displays the decrypted content of the selected bill file in the bill_area widget.
        Shows a warning if no file is selected.
        """
        # Retrieve the current selection from the Sales_List
        selected_indices = self.Sales_List.curselection()

        if selected_indices:
            # Get the index of the first item in the selection
            index = selected_indices[0]
            # Retrieve the file name from the Sales_List based on the selected index
            file_name = self.Sales_List.get(index)

            # Attempt to open and decrypt the selected bill file
            try:
                with open(f'bill/{file_name}', 'r') as file:
                    encrypted_content = file.read()
                    # Decrypt the content read from the file
                    decrypted_content = self.decrypt_data(encrypted_content)
                    # Display the decrypted content in the bill_area
                    self.bill_area.delete('1.0', END)
                    self.bill_area.insert(END, decrypted_content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read or decrypt the file: {str(e)}", parent=self.root)
        else:
            # Notify user if no bill is selected
            messagebox.showwarning("Warning", "Please select a bill from the list.", parent=self.root)

    # def search(self):
    #     if self.var_invoice.get() == "":
    #         messagebox.showerror("Error", "invoice Number should be required", parent=self.root)
    #     else:
    #         if self.var_invoice.get() in self.bill_list:
    #             fp = open(f'bill/{self.var_invoice.get()}.txt', 'r')
    #             self.bill_area.delete('1.0', END)
    #             for i in fp:
    #                 self.bill_area.insert(END, i)
    #             fp.close()
    #         else:
    #             messagebox.showerror("Error", "invalid invoice number", parent=self.root)

    # def search(self):
    #     """
    #     Searches for a bill file based on the user-entered invoice number and displays its content.
    #     If the invoice number is empty or the file does not exist, shows an appropriate error message.
    #     """
    #     invoice_number = self.var_invoice.get().strip()  # Remove any leading/trailing whitespace
    #
    #     if not invoice_number:
    #         # Show error if the invoice number field is empty
    #         messagebox.showerror("Error", "Invoice number is required", parent=self.root)
    #         return
    #
    #     # Construct the file path using the invoice number
    #     file_path = f'bill/{invoice_number}.txt'
    #
    #     # Check if the invoice number is in the bill list and the file exists
    #     if invoice_number in self.bill_list and os.path.exists(file_path):
    #         # Open the file and display its contents
    #         try:
    #             with open(file_path, 'r') as file:
    #                 self.bill_area.delete('1.0', END)  # Clear previous contents
    #                 self.bill_area.insert(END, file.read())  # Read the entire file and insert its content
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Failed to read the file: {str(e)}", parent=self.root)
    #     else:
    #         # Show error if the invoice number is not valid or the file does not exist
    #         messagebox.showerror("Error", "Invalid invoice number", parent=self.root)

    def search(self):
        """
        Searches for a bill file based on the user-entered invoice number and displays its decrypted content.
        If the invoice number is empty or the file does not exist, an appropriate error message is displayed.
        """
        invoice_number = self.var_invoice.get().strip()  # Trim whitespace from the input

        if not invoice_number:
            # Alert the user if the invoice field is empty
            messagebox.showerror("Error", "Invoice number is required", parent=self.root)
            return

        # Construct the expected file path using the invoice number
        file_path = f'bill/{invoice_number}.txt'

        # Verify the existence of the file before attempting to open it
        if os.path.exists(file_path):
            try:
                # Open the file, decrypt its contents, and display them
                with open(file_path, 'r') as file:
                    encrypted_content = file.read()
                    decrypted_content = self.decrypt_data(encrypted_content)
                    self.bill_area.delete('1.0', END)  # Clear any existing content
                    self.bill_area.insert(END, decrypted_content)  # Display the decrypted content
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read or decrypt the file: {str(e)}", parent=self.root)
        else:
            # Notify the user if the file does not exist
            messagebox.showerror("Error", "Invalid invoice number or the file does not exist", parent=self.root)

    # def clear(self):
    #     self.show()
    #     self.bill_area.delete('1.0', END)

    # def clear(self):
    #     """
    #     Clears data displayed in the bill area and refreshes the display components.
    #     This function is typically called to reset the state of the bill display area, possibly after a transaction is completed
    #     or when starting a new billing process.
    #     """
    #     # Refresh the list or other related display components by calling show(),
    #     # which might update lists or other UI elements based on current data.
    #     self.show()
    #
    #     # Clear all text from the bill area starting from the first character ('1.0') to the end ('END').
    #     # This effectively resets the bill display area for new input or messages.
    #     self.bill_area.delete('1.0', END)

    def clear(self):
        """
        Clears the bill display area and refreshes any related UI components necessary for initiating new transactions.
        """
        # Reset the display components that list or show data, ensuring they reflect the current state or empty states as needed.
        self.show()

        # Remove all existing content from the bill area to prepare for new data input or other interactions.
        self.bill_area.delete('1.0', END)  # Clears the text from the start ('1.0') to the end ('END').


if __name__ == "__main__":
    # Create the main window (root window) for the application
    root = Tk()

    # Create an instance of the 'salesClass', passing the root window as an argument.
    # The 'salesClass' is assumed to be a class that initializes the GUI and binds event handlers.
    obj = salesClass(root)

    # Start the Tkinter event loop.
    # This call is blocking and will wait for all GUI events such as button clicks,
    # window resizing, etc., until the window is closed.
    root.mainloop()
