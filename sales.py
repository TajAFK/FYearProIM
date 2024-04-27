# Standard library imports
import os

# Third-party library imports
from PIL import Image, ImageTk

from CryptoManager import CryptoManagerClass  # Manage Encryption Decryption of text

# Tkinter imports for GUI components
from tkinter import (Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, Text,
                     messagebox, StringVar, END, TOP, BOTH, RIGHT, X, Y, RIDGE, VERTICAL)


class SalesClass:
    def __init__(self, roots):
        self.root = roots
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Instantiate the CryptoManager for encryption and decryption tasks
        self.crypto_manager = CryptoManagerClass()

        self.bill_list = []
        self.var_invoice = StringVar()

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

        # ============ Bill List Section ============
        # Frame for displaying bills with a prominent bordered design.
        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=330)  # Positioned to fit within the main window.

        # Vertical scrollbar to navigate through the list of bills.
        scrolly = Scrollbar(sales_frame, orient=VERTICAL)

        # Listbox to display sales entries, enabled with vertical scrolling.
        self.Sales_List = Listbox(sales_frame, font=("Arial", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)  # Align scrollbar to the right of the Listbox.
        scrolly.config(command=self.Sales_List.yview)  # Connect the scrollbar to the Listbox.
        self.Sales_List.pack(fill=BOTH, expand=1)  # Allow the Listbox to expand and fill the frame.

        # Bind the Listbox to an event handler for selection.
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)  # Trigger 'get_data' on item selection.

        # ============ Bill Display Area ============
        # Frame for showing detailed customer bills, designed with borders and a raised layout.
        bill_frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=421, height=330)  # Set dimensions and position on the window.

        # Label for the bill area, styled with an orange background to stand out.
        lab_title2 = Label(bill_frame, text="Customer Bill Area", font=("Arial", 20, "bold"), bg="orange")
        lab_title2.pack(side=TOP, fill=X)  # Attach to the top of the frame and fill horizontally.

        # Scrollbar to navigate through the bill text area.
        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)

        # Text area for displaying bill details, set with a light yellow background for visibility.
        self.bill_area = Text(bill_frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)  # Position the scrollbar on the right side, filling vertically.
        scrolly2.config(command=self.bill_area.yview)  # Connect the text area scrolling to the scrollbar.
        self.bill_area.pack(fill=BOTH, expand=1)  # Allow the text area to expand fully within its frame.

        # ============ Decorative Image ============
        # Load and configure an image to enhance the visual appeal of the GUI.
        self.bill_photo = Image.open("images/boxes.jpg").resize((450, 300),
                                                                Image.Resampling.LANCZOS)  # Resize for optimal fit.
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)  # Convert to a format suitable for Tkinter to handle.

        # Label to hold the image, set without a border for a seamless look.
        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=700, y=110)  # Position the image within the root window.

        # Initial display refresh to ensure the image and other data are shown when the program starts.
        self.show()

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

    def encrypt_data(self, data):
        """
        Encrypts data using the cryptographic manager's encrypt method.
        """
        return self.crypto_manager.encrypt_data(data)

    def decrypt_data(self, data):
        """
        Decrypts data using the cryptographic manager's decrypt method.
        """
        return self.crypto_manager.decrypt_data(data)

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

    def clear(self):
        """
        Clears the bill display area and refreshes any related UI components necessary for initiating new transactions.
        """
        # Reset the display components that list or show data, ensuring they reflect the current state or empty
        # states as needed.
        self.show()

        # Remove all existing content from the bill area to prepare for new data input or other interactions.
        self.bill_area.delete('1.0', END)  # Clears the text from the start ('1.0') to the end ('END').


if __name__ == "__main__":
    # Create the main window (root window) for the application
    root = Tk()

    # Create an instance of the 'salesClass', passing the root window as an argument.
    # The 'salesClass' is assumed to be a class that initializes the GUI and binds event handlers.
    obj = SalesClass(root)

    # Start the Tkinter event loop.
    # This call is blocking and will wait for all GUI events such as button clicks,
    # window resizing, etc., until the window is closed.
    root.mainloop()
