# Import essential libraries for system operations, UI, security, and email handling
import datetime
import json  # For loading and parsing JSON files
import os
import smtplib  # For sending emails via SMTP
import sqlite3  # For database interactions
import subprocess  # For executing external processes
from random import randint  # For generating random numbers, useful for OTPs
from tkinter import *  # For GUI creation
from tkinter import messagebox, ttk  # For displaying messages

from CryptoManager import CryptoManagerClass  # Manage Encryption Decryption of text
from create_db import create_db


# Define the main class for the login system

class LoginSystem:
    def __init__(self, roots):
        """Initialize the application with basic window configuration and cryptographic setup."""
        self.root = roots
        self.root.title("Inventory Management System | Ariatech")
        self.root.geometry("1050x700+0+0")
        self.root.config(bg="#fafafa")

        # Immediately withdraw the root window on application start
        self.root.withdraw()

        # Setup cryptographic manager for secure operations.
        self.crypto_manager = CryptoManagerClass()  # Instantiate the cryptographic manager class.

        # Load or generate a cryptographic key, and prepare the cipher for use.
        self.crypto_manager.cipher = self.crypto_manager.load_key_and_initialize_cipher()
        # This method will either load an existing cryptographic key from a file or generate a new one if it doesn't
        # exist. It then initializes a cipher object with this key to encrypt and decrypt data throughout the
        # application.

        # Setup variables for managing user input in password reset functionality.
        self.var_otp = StringVar()  # OTP input by the user
        self.var_new_pass = StringVar()  # New password input
        self.var_conf_pass = StringVar()  # Confirm new password input

        # Initialize StringVars for holding login credentials
        self.employee_id = StringVar()
        self.password = StringVar()

        # Initialize the database and check for admin presence.
        self.initialize_db()

    def initialize_db(self):
        """Check for the database file and initialize it if not present, then check for admin presence."""
        db_path = 'ims.db'
        if not os.path.exists(db_path):
            create_db()  # Create the database if it doesn't exist
            messagebox.showinfo("Database Setup", "Database initialized successfully!")
        self.check_admin_user()

    def check_admin_user(self):
        """Check for admin presence and either proceed to login or initiate admin setup."""
        if not self.admin_exists():
            self.create_admin_window()
        else:
            self.root.deiconify()  # Show the main window
            self.login_ui()  # Setup login UI if an admin exists

    @staticmethod
    def admin_exists():
        """
        Checks if an admin user exists in the database by querying the employee table.
        Returns True if an admin exists, otherwise False.
        """
        try:
            with sqlite3.connect('ims.db') as con:  # Establish a connection to the database.
                cur = con.cursor()  # Create a cursor object to execute SQL commands.
                cur.execute("SELECT * FROM employee WHERE utype='Admin'")  # Execute SQL command to find admin users.
                return cur.fetchone() is not None  # Return True if an admin record is found, else False.
        except Exception as ex:
            messagebox.showerror("Database Error",
                                 f"Error checking for admin user: {str(ex)}")  # Display error if exception occurs.
            return False  # Return False if there was an error during execution.

    def create_admin_window(self):
        self.admin_win = Toplevel(self.root)
        self.admin_win.title("Initial Setup - Create Admin")
        self.admin_win.geometry("1100x300+220+130")
        self.admin_win.config(bg="white")

        self.var_emp_id = StringVar()  # Employee ID
        self.var_gender = StringVar()  # Gender
        self.var_contact = StringVar()  # Contact number
        self.var_name = StringVar()  # Employee name
        self.var_dob = StringVar()  # Date of birth
        self.var_doj = StringVar()  # Date of joining
        self.var_email = StringVar()  # Email address
        self.var_pass = StringVar()  # Password for login or system access
        self.var_utype = StringVar()  # User type (e.g., Admin, Employee)
        self.var_salary = StringVar()  # Salary

        # Title Label
        # Display a label at the top of the form to indicate the section for Employee Details
        Label(self.admin_win, text="Create Admin Account", font=("goudy old style", 15), bg="#0f4d7d",
              fg="white").place(
            x=50, y=25, width=1000)

        # Content: Row 1 - Employee Information
        # Label and entry for Employee ID
        validate_command = self.admin_win.register(lambda input: input.isdigit() or input == "")
        Label(self.admin_win, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=75)
        username = Entry(self.admin_win, textvariable=self.var_emp_id, validate="key",
                         validatecommand=(validate_command, '%P'),
                         font=("goudy old style", 15),
                         bg="lightyellow")
        username.place(x=150, y=75, width=180)

        # Label and combobox for selecting Gender
        Label(self.admin_win, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=75)
        cmb_gender = ttk.Combobox(self.admin_win, textvariable=self.var_gender,
                                  values=("Select", "Male", "Female", "Other"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=75, width=180)
        cmb_gender.current(0)  # Default to the first entry 'Select'

        # Label and entry for Contact Information
        Label(self.admin_win, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=75)
        validate_contact = self.admin_win.register(lambda input: input.isdigit() or input in " -")
        Entry(self.admin_win, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow",
              validate="key", validatecommand=(validate_contact, '%P')).place(x=850, y=75, width=180)

        # Content: Row 2 - Additional Employee Information
        # Label and entry for Employee Name
        Label(self.admin_win, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=115)
        Entry(self.admin_win, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=115, width=180)

        # Label and entry for Employee Date of Birth (D.O.B)
        Label(self.admin_win, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=115)
        Entry(self.admin_win, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=115, width=180)

        # Label and entry for Employee Date of Joining (D.O.J)
        Label(self.admin_win, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=115)
        Entry(self.admin_win, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(
            x=850, y=115, width=180)

        # Row 3
        Label(self.admin_win, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=155)
        Label(self.admin_win, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=155)
        Label(self.admin_win, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=155)
        Entry(self.admin_win, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(
            x=150, y=155, width=180)
        Entry(self.admin_win, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(
            x=500, y=155, width=180)

        # User type is fixed to 'Admin',
        self.var_utype.set('Admin')  # Set the user type variable to 'Admin'
        Label(self.admin_win, text="Admin", font=("goudy old style", 15), bg="lightyellow").place(x=850, y=155,
                                                                                                  width=180)

        # Row 4

        Label(self.admin_win, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=195)
        Label(self.admin_win, text="Salary", font=("goudy old style", 15), bg="white").place(x=750, y=195)
        self.txt_address = Text(self.admin_win, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=195, width=530, height=30)  # Corrected this line

        validate_salary = self.admin_win.register(lambda input: input.replace('.', '', 1).isdigit() or input == "")
        Entry(self.admin_win, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow",
              validate="key", validatecommand=(validate_salary, '%P')).place(x=850, y=195, width=180)

        # Buttons
        Button(self.admin_win, text="SUBMIT", command=self.submit_admin, font=("goudy old style", 15), bg="#2196f3",
               fg="white",
               cursor="hand2").place(x=500, y=250, width=110, height=28)

    def submit_admin(self):
        """
        Adds a new employee record to the database after validating that the employee ID is unique.
        Ensures all required fields are filled and the employee ID does not already exist in the database.
        """
        missing_fields = []  # List to hold the names of missing fields

        # Check each field and add the field name to the list if it's empty
        if not self.var_emp_id.get().strip():
            missing_fields.append("Employee ID")
        if not self.var_name.get().strip():
            missing_fields.append("Name")
        if not self.var_email.get().strip():
            missing_fields.append("Email")
        if not self.var_gender.get() or self.var_gender.get() == "Select":
            missing_fields.append("Gender")
        if not self.var_contact.get().strip():
            missing_fields.append("Contact")
        if not self.var_dob.get().strip():
            missing_fields.append("D.O.B")
        if not self.var_doj.get().strip():
            missing_fields.append("D.O.J")
        if not self.var_pass.get().strip():
            missing_fields.append("Password")
        if not self.var_utype.get().strip():
            missing_fields.append("User Type")
        if not self.txt_address.get('1.0', END).strip():
            missing_fields.append("Address")
        if not self.var_salary.get().strip():
            missing_fields.append("Salary")

        # If there are any missing fields, show an error message and return
        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)  # Convert list to comma-separated string
            messagebox.showerror("Error", f"Missing fields: {missing_fields_str}", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Check if the employee ID already exists in the database
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                    return

                # Insert the new admin record into the database
                cur.execute(
                    "INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        self.var_emp_id.get(),
                        self.encrypt_data(self.var_name.get()),
                        self.encrypt_data(self.var_email.get()),
                        self.var_gender.get(),
                        self.encrypt_data(self.var_contact.get()),
                        self.encrypt_data(self.var_dob.get()),
                        self.var_doj.get(),
                        self.encrypt_data(self.var_pass.get()),
                        self.var_utype.get(),
                        self.encrypt_data(self.txt_address.get('1.0', END).strip()),
                        self.var_salary.get(),
                    ))
                # Commit changes to the database
                con.commit()
                messagebox.showinfo("Setup Complete", "Admin created successfully!")
                self.admin_win.destroy()  # Close the admin window
                self.root.deiconify()  # Make the root window visible
                self.login_ui()  # Prompt the login UI setup after admin creation
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def login_ui(self):
        """Setup the login interface with user ID and password fields, and controls for authentication."""

        # Display mobile image at the specific position.
        self.mobile_image = PhotoImage(file="images/mobile.png")
        Label(self.root, image=self.mobile_image, bd=0).place(x=200, y=50)

        # Initialize the login frame.
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        # Login title.
        Label(login_frame, text="Login", font=("Arial Rounded MT Bold", 30), bg="white", fg="#00759E").pack(fill=X,
                                                                                                            pady=(
                                                                                                            30, 20))

        # User ID entry with validation.
        Label(login_frame, text="User ID", font=("Andlus", 15, "bold"), bg="white", fg="#343A40").place(x=50, y=100)
        validate_command = login_frame.register(lambda input: input.isdigit() or input == "")
        Entry(login_frame, textvariable=self.employee_id, validate="key", validatecommand=(validate_command, '%P'),
              font=("Andlus", 15), bg="#FFFFFF", fg="#343A40").place(x=50, y=140, width=250)

        # Password entry field.
        Label(login_frame, text="Password", font=("Andlus", 15, "bold"), bg="white", fg="#343A40").place(x=50, y=200)
        Entry(login_frame, textvariable=self.password, show="*", font=("Andlus", 15), bg="white", fg="#343A40").place(
            x=50, y=240, width=250)

        # Sign-in button with visual feedback on events.
        sign_btn = Button(login_frame, text="Sign In", command=self.login, font=("Arial Rounded MT Bold", 15),
                          bg="#007BFF", fg="white", bd=0, relief=FLAT, cursor="hand2")
        sign_btn.place(x=50, y=300, width=250, height=35)
        sign_btn.bind("<Enter>", lambda e: sign_btn.config(bg="#00597A"))
        sign_btn.bind("<Leave>", lambda e: sign_btn.config(bg="#007BFF"))
        sign_btn.bind("<ButtonPress-1>", lambda e: sign_btn.config(bg="#003D52"))
        sign_btn.bind("<ButtonRelease-1>", lambda e: sign_btn.config(bg="#007BFF"))

        # 'Forget Password?' link setup.
        forget_btn = Button(login_frame, text="Forget Password?", command=self.emp_id_check,
                            font=("Arial Rounded MT Bold", 13), bg="#00759E", fg="white", bd=0, relief=FLAT,
                            activeforeground="white", activebackground="#00759E", cursor="hand2")
        forget_btn.place(x=50, y=390, width=250, height=35)
        forget_btn.bind("<Enter>", lambda e: forget_btn.config(bg="#00597A"))
        forget_btn.bind("<Leave>", lambda e: forget_btn.config(bg="#00759E"))

        # Promotional message setup.
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)
        Label(register_frame, text="Join Our Community - Stay Updated!", font=("Arial", 13, "bold"), fg="#00759E",
              bg="white").place(x=0, y=20, relwidth=1)

        # Initialize image animation in the interface.
        self.images = [PhotoImage(file=f"images/fade{i}.png") for i in range(1, 4)]
        self.image_index = 0
        self.lbl_change_image = Label(self.root, image=self.images[self.image_index], bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)
        self.animate()

    def animate(self):
        """
        Cycles through a list of images to create an animation effect.
        """
        # Update the image displayed by the label
        self.lbl_change_image.config(image=self.images[self.image_index])

        # Move to the next image in the list, wrapping around at the end
        self.image_index = (self.image_index + 1) % len(self.images)

        # Schedule the next call to animate
        self.lbl_change_image.after(2000, self.animate)


    def forget_ui(self):
        """Set up the password reset interface for user interaction."""

        # Initialize the password reset window.
        self.forget_win = Toplevel(self.root)
        self.forget_win.title("Reset Password")
        self.forget_win.geometry("400x400")
        self.forget_win.config(bg="#f0f0f0")

        # Header label for the reset password window.
        Label(self.forget_win, text='Reset Password', font=('Arial', 20, 'bold'), bg="#3f51b5", fg="white").pack(
            side=TOP, fill=X)

        # Label and entry for OTP input.
        Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("Arial", 14)).place(x=20, y=60)
        self.var_otp = StringVar()
        validate_command = self.forget_win.register(lambda input: input.isdigit() or input == "")
        Entry(self.forget_win, textvariable=self.var_otp, validate="key", validatecommand=(validate_command, '%P'),
              font=("Arial", 14), bg='lightyellow', bd=2, relief=GROOVE).place(x=20, y=100, width=250, height=30)

        # Button to submit OTP.
        self.submit_otp = Button(self.forget_win, text="SUBMIT", command=self.validate_otp, font=('Arial', 14),
                                 bg="#4caf50", fg="white", bd=2, relief=RAISED, cursor="hand2")
        self.submit_otp.place(x=20, y=140, width=100, height=30)

        # Button to request OTP resend.
        self.generate_otp = Button(self.forget_win, text="REQUEST OTP", command=self.password_reset, font=('Arial', 14),
                                   bg="#4caf50", fg="white", bd=2, relief=RAISED, cursor="hand2")
        self.generate_otp.place(x=130, y=140, width=140, height=30)

        # Labels and entries for new password and confirmation.
        Label(self.forget_win, text="New Password", font=("Arial", 14)).place(x=20, y=200)
        self.var_new_pass = StringVar()
        Entry(self.forget_win, textvariable=self.var_new_pass, font=("Arial", 14), bg='lightyellow', show="*",
              bd=2, relief=GROOVE).place(x=20, y=230, width=250, height=30)

        Label(self.forget_win, text="Confirm Password", font=("Arial", 14)).place(x=20, y=265)
        self.var_conf_pass = StringVar()
        Entry(self.forget_win, textvariable=self.var_conf_pass, font=("Arial", 14), bg='lightyellow', show="*",
              bd=2, relief=GROOVE).place(x=20, y=295, width=250, height=30)

        # Button to update the password.
        self.btn_update = Button(self.forget_win, text="Update", command=self.update_password, state=DISABLED,
                                 font=('Arial', 14), bg="#2196f3", fg="white", bd=2, relief=RAISED, cursor="hand2")
        self.btn_update.place(x=150, y=340, width=100, height=30)

    def emp_id_check(self):
        """
        Validates the presence of an employee ID before proceeding.
        This is a preliminary check before launching the password reset UI.
        """
        # Check if the employee ID field is empty
        if not self.employee_id.get():
            # Display an error message if the employee ID is missing
            messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            return

        # Proceed to open the password reset UI if the employee ID is provided
        self.root.withdraw()
        self.forget_ui()

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

    def login(self):
        """
        Handles user login by verifying credentials against the database.
        Redirects the user to appropriate dashboards based on their role if login is successful.
        "Encryption was chosen over hashing for password storage in this project to facilitate secure password recovery
        capabilities, which is a requirement for administrative users in the scenario simulated by this system.
        Additionally, using encryption allows for reversible transformation, which is aligned with specific legacy
        system integration requirements that necessitate access to the original password data for authentication
        processes."
        """
        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()

                # Validate non-empty credentials input
                if not self.employee_id.get() or not self.password.get():
                    messagebox.showerror("Error", "All fields are required", parent=self.root)
                    return

                # Execute query to fetch user type and password for the given employee ID
                cur.execute("SELECT utype, pass FROM employee WHERE eid=?", (self.employee_id.get(),))
                user = cur.fetchone()

                # Validate existence of user record
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                    return

                # Decrypt the password retrieved from the database
                decrypted_password = self.crypto_manager.decrypt_data(user[1])

                # Check if decrypted password matches the input password
                if decrypted_password == self.password.get():
                    # Successful login, proceed based on user type
                    self.root.destroy()
                    if user[0] == "Admin":
                        subprocess.run(["python", "dashboard.py"], check=True)
                    else:
                        subprocess.run(["python", "billing.py"], check=True)
                else:
                    # Password does not match
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)

        except Exception as ex:
            # Log or handle any exceptions raised during the login process
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    import sqlite3
    from tkinter import messagebox, DISABLED, NORMAL

    def password_reset(self):
        """
        Process to reset the password for users who have forgotten it. Retrieves the registered email,
        sends an OTP, and prepares the UI for password update.
        """
        try:
            # Establish database connection to retrieve the encrypted email
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
            email_encrypted = cur.fetchone()
            con.close()

            if not email_encrypted:
                messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                return

            # Decrypt the email before sending OTP
            email = self.crypto_manager.decrypt_data(email_encrypted[0])
            if not self.send_email(email):
                messagebox.showerror("Error", "Failed to send email. Check your connection and try again.",
                                     parent=self.root)
                return

            # Disable the OTP button to prevent re-sending immediately and re-enable after 60 seconds
            self.generate_otp.config(state=DISABLED)
            self.countdown(60)  # Start countdown for 60 seconds

        except Exception as ex:
            # Handle any exceptions and show an error message
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def countdown(self, remaining=None):
        """Updates the button text with the time left and re-enables the button when the countdown finishes."""
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.generate_otp.config(text="REQUEST OTP")
            self.generate_otp.config(state=NORMAL)
        else:
            self.generate_otp.config(text=f"Please wait {self.remaining}s")
            self.remaining = self.remaining - 1
            # Schedule the countdown function to be called after 1 second
            self.root.after(1000, lambda: self.countdown())

    def update_password(self):
        """
        Validates and updates the user's password in the database. Ensures that the new password is confirmed correctly
        before updating to prevent errors.
        """
        # Validate password fields are not empty
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
            return

        # Check if the new password and confirmation password match
        if self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "Passwords do not match", parent=self.forget_win)
            return

        try:
            # Establish a connection to the database
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                # Encrypt the new password using the CryptoManager's encrypt_data method
                encrypted_password = self.crypto_manager.encrypt_data(self.var_new_pass.get())
                # Update the password in the database
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (encrypted_password, self.employee_id.get()))
                con.commit()  # Commit changes to ensure data is saved
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()  # Close the reset window upon success
                self.root.deiconify()  # Make the root window visible
        except Exception as ex:
            # Handle exceptions that may occur during database operations
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def validate_otp(self):
        """
        Validates the OTP entered by the user against a pre-stored value and checks if the OTP is still within a valid timeframe.
        """
        try:
            user_otp = int(self.var_otp.get())
            current_time = datetime.datetime.now()

            # Check if the OTP is within the validity period (e.g., 5 minutes)
            if self.otp_time and (current_time - self.otp_time <= datetime.timedelta(minutes=1)):
                if user_otp == self.otp:
                    # OTP is correct and within the time limit
                    self.btn_update.config(state="normal")
                    self.submit_otp.config(state="disabled")
                    print("OTP Valid and within time.")  # Debug
                else:
                    # OTP is incorrect
                    messagebox.showerror("Error", "Invalid OTP, please try again", parent=self.forget_win)
            else:
                # OTP is expired
                messagebox.showerror("Error", "OTP has expired, please request a new one", parent=self.forget_win)

        except ValueError:
            # Handle non-integer input gracefully
            messagebox.showerror("Error", "OTP should be a numeric value", parent=self.forget_win)
        except Exception as ex:
            # Catch any other unexpected errors
            messagebox.showerror("Error", f"An error occurred: {str(ex)}", parent=self.forget_win)

    @staticmethod
    def load_credentials():
        """
        Loads email credentials from a configuration file.
        """
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config['email'], config['password']

    def send_email(self, to_):
        """
        Sends an email with a randomly generated OTP to the provided email address.
        Uses SMTP to connect to the Gmail server and handles potential errors gracefully.
        """
        # Attempt to load email credentials from a JSON configuration file
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            email_ = config['email']
            pass_ = config['password']
        except FileNotFoundError:
            print("Configuration file not found.")
            return 'f'
        except KeyError:
            print("Essential email configuration data is missing.")
            return 'f'
        except json.JSONDecodeError:
            print("Configuration file is not in valid JSON format.")
            return 'f'

        # Attempt to send an email with the generated OTP
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade the connection to secure
            server.login(email_, pass_)

            # Generate a six-digit OTP
            self.otp = randint(100000, 999999)
            self.otp_time = datetime.datetime.now()

            # Prepare the email message
            subj = 'IMS-Reset Password OTP'
            msg = f'Dear Sir/Madam,\n\nYour Reset OTP is {self.otp}.\n\nWith Regards,\nIMS Team'
            msg = f"Subject:{subj}\n\n{msg}"

            # Send the email
            server.sendmail(email_, to_, msg)
        except smtplib.SMTPException as e:
            print(f"Failed to send email due to SMTP error: {str(e)}")
            return 'f'
        finally:
            server.quit()  # Ensure the connection to the server is closed

        # Return 's' for success if the email has been sent
        return 's'


# Main script execution
if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
