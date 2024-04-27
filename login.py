# Import essential libraries for system operations, UI, security, and email handling
import json  # For loading and parsing JSON files
import os
import smtplib  # For sending emails via SMTP
import sqlite3  # For database interactions
import subprocess  # For executing external processes
from random import randint  # For generating random numbers, useful for OTPs
from tkinter import *  # For GUI creation
from tkinter import messagebox  # For displaying messages
from tkinter.ttk import Style  # For displaying styling the GUI
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

        self.forget_win = None  # Placeholder for the forgot password window
        self.crypto_manager = CryptoManagerClass()

        # Variable initialization for password reset functionality
        self.var_otp = StringVar()  # OTP input by the user
        self.var_new_pass = StringVar()  # New password input
        self.var_conf_pass = StringVar()  # Confirm new password input

        self.initialize_db()

    def initialize_db(self):
        """Check for the database file and initialize it if not present, then check for admin presence."""
        db_path = 'ims.db'
        if not os.path.exists(db_path):
            create_db()  # Create the database and tables
            messagebox.showinfo("Database Setup", "Database initialized successfully!")
        self.check_admin_user()

    def check_admin_user(self):
        """Check for admin presence and either proceed to login or setup admin."""
        if not self.admin_exists():
            self.create_admin_window()
        else:
            self.setup_login_ui()  # Initialize and display login UI if admin exists

    @staticmethod
    def admin_exists():
        """Determine if an admin user exists in the database."""
        try:
            with sqlite3.connect('ims.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE utype='Admin'")
                return cur.fetchone() is not None
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error checking admin user: {str(ex)}")
            return False

    # def create_admin_window(self):
    #     """Create a window for admin registration if no admin exists."""
    #     admin_win = Toplevel(self.root)
    #     admin_win.title("Initial Setup - Create Admin")
    #     admin_win.geometry("300x300+400+200")
    #
    #     Label(admin_win, text="Set Admin Credentials", font=("Arial", 12, "bold")).pack(pady=10)
    #     Label(admin_win, text="Employee ID:").pack()
    #     username = Entry(admin_win)
    #     username.pack(pady=5)
    #
    #     Label(admin_win, text="Password:").pack()
    #     password = Entry(admin_win, show="*")
    #     password.pack(pady=5)
    #
    #     Button(admin_win, text="Submit",
    #            command=lambda: self.submit_admin(username.get(), password.get(), admin_win)).pack(pady=20)

    def create_admin_window(self):
        """Create a window for admin registration if no admin exists."""
        admin_win = Toplevel(self.root)
        admin_win.title("Initial Setup - Create Admin")
        admin_win.geometry("300x300+400+200")

        Label(admin_win, text="Set Admin Credentials", font=("Arial", 12, "bold")).pack(pady=10)
        Label(admin_win, text="Employee ID [0-9]:").pack()

        # Using StringVar to track changes in the entry widget
        username_var = StringVar()

        # Validation command
        def validate_digit(input):
            if input.isdigit() or input == "":
                return True
            return False

        validate_command = admin_win.register(validate_digit)

        username = Entry(admin_win, textvariable=username_var, validate="key", validatecommand=(validate_command, '%P'))
        username.pack(pady=5)

        Label(admin_win, text="Password:").pack()
        password = Entry(admin_win, show="*")
        password.pack(pady=5)

        Button(admin_win, text="Submit",
               command=lambda: self.submit_admin(username.get(), password.get(), admin_win)).pack(pady=20)

    def submit_admin(self, username, password, window):
        """Submit new admin credentials to the database and close the setup window."""
        encrypted_pass = self.crypto_manager.encrypt_data(password)
        try:
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO employee (eid, name, pass, utype) VALUES (?, ?, ?, 'Admin')",
                            (username, username, encrypted_pass))
                con.commit()
                messagebox.showinfo("Setup Complete", "Admin created successfully!")
                window.destroy()
                self.setup_login_ui()  # Initialize the login UI after admin is created
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to create admin: {str(ex)}")

    def setup_login_ui(self):
        """Set up and display the login UI components."""
        # This method initializes and displays the login UI elements.
        # This includes loading images, setting up the login frame, and other visual elements.

        # GUI components
        self.mobile_image = PhotoImage(file="images/mobile.png")  # Load phone image
        Label(self.root, image=self.mobile_image, bd=0).place(x=200, y=50)  # Place phone image on the window

        # ====Login Frame======
        # Initialize StringVars for holding login credentials
        self.employee_id = StringVar()
        self.password = StringVar()

        # Create a frame for the login section
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        # Title label for the login form
        title = Label(login_frame, text="Login", font=("Arial Rounded MT Bold", 30), bg="white", fg="#00759E")
        title.pack(fill=X,
                   pady=(30, 20))

        # Label and entry for Username
        Label(login_frame, text="User ID", font=("Andlus", 15, "bold"), bg="white", fg="#343A40").place(x=50, y=100)
        Entry(login_frame, textvariable=self.employee_id, font=("Andlus", 15), bg="#FFFFFF", fg="#343A40").place(x=50,
                                                                                                                 y=140,
                                                                                                                 width=250)

        # Label and entry for Password
        Label(login_frame, text="Password", font=("Andlus", 15, "bold"), bg="white", fg="#343A40").place(x=50, y=200)
        Entry(login_frame, textvariable=self.password, show="*", font=("Andlus", 15), bg="white", fg="#343A40").place(
            x=50, y=240, width=250)

        # Login button
        # Define a function to handle hover effect
        def on_enter(event):
            sign_btn.config(bg="#00597A")  # Change background color to a darker shade of blue

        # Define a function to handle hover end
        def on_leave(event):
            sign_btn.config(bg="#007BFF")  # Revert back to the default background color

        # Define a function to handle button press
        def on_click(event):
            sign_btn.config(bg="#003D52")  # Darken the background color when pressed

        # Define a function to handle button release
        def on_release(event):
            sign_btn.config(bg="#007BFF")  # Revert back to the default background color

        # Create the button
        sign_btn = Button(login_frame, text="Sign In", command=self.login, font=("Arial Rounded MT Bold", 15),
                          bg="#007BFF", fg="white", bd=0, relief=FLAT, cursor="hand2")

        # Bind events for hover and pressed effects
        sign_btn.bind("<Enter>", on_enter)
        sign_btn.bind("<Leave>", on_leave)
        sign_btn.bind("<ButtonPress-1>", on_click)
        sign_btn.bind("<ButtonRelease-1>", on_release)

        # Place the button in the frame
        sign_btn.place(x=50, y=300, width=250, height=35)

        # Horizontal line and 'OR' text
        Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150,
                                                                                                              y=355)

        # Forget Password Button
        forget_btn = Button(login_frame, text="Forget Password?", command=self.forget_window,
                            font=("Arial Rounded MT Bold", 13),
                            bg="#00759E", fg="white", bd=0, relief=FLAT, activeforeground="white",
                            activebackground="#00759E", cursor="hand2")

        # Check if login_frame is properly defined

        # Apply gradient background
        style = Style()
        style.theme_use("clam")  # Use 'clam' theme for gradient effect
        style.map("TButton",
                  background=[("active", "#00597A")])

        # Configure hover effects
        forget_btn.bind("<Enter>", lambda e: forget_btn.config(bg="#00597A"))
        forget_btn.bind("<Leave>", lambda e: forget_btn.config(bg="#00759E"))

        # Adjust padding and width
        forget_btn.place(x=50, y=390, width=250, height=35)

        # ====Frame 2===========
        # Create a frame for registration or promotional actions
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        # Shadow label for the promotional text
        Label(register_frame, text="Join Our Community - Stay Updated!",
              font=("Arial", 13, "bold"),
              fg="#CCCCCC",  # Light grey for shadow effect
              bg="white").place(x=1, y=22, relwidth=1)

        # Main promotional text
        Label(register_frame, text="Join Our Community - Stay Updated!",
              font=("Arial", 13, "bold"),
              fg="#00759E",  # Pleasant blue
              bg="white").place(x=0, y=20, relwidth=1)

        # ======Animation Images=====
        # Initialize the image list and index
        self.images = [PhotoImage(file="images/fade1.png"), PhotoImage(file="images/fade2.png"),
                       PhotoImage(file="images/fade3.png")]
        self.image_index = 0

        # Set up the label to display images
        self.lbl_change_image = Label(self.root, image=self.images[self.image_index], bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)

        # Start the animation
        self.animate()

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
                #decrypted_password = self.decrypt_data(user[1].encode()).decode()
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

    def forget_window(self):
        """
        Handles the password reset process for users who have forgotten their password. The process includes verifying
        the employee ID, sending an OTP to the registered email, and allowing the user to reset their password.
        """
        try:
            # Check for empty Employee ID field
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
                return
            # Establish database connection to retrieve the encrypted email
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
            email_encrypted = cur.fetchone()  # This will fetch the encrypted email
            con.close()  # Close the database connection promptly

            # Handle case where the Employee ID is not found
            if email_encrypted is None:
                messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                return

            # Decrypt the email before sending OTP
            email = self.crypto_manager.decrypt_data(email_encrypted[0])  # Decrypting the email

            # =========Forget Window=============
            # Call send_email_function
            # Send OTP to the registered email address
            if not self.send_email(email):
                messagebox.showerror("Error", "Failed to send email. Please check your connection and try again.",
                                     parent=self.root)
                return
            # Setup the password reset window after successful email sending
            self.forget_win = Toplevel(self.root)
            self.forget_win.title("Reset Password")
            self.forget_win.geometry("400x400")
            self.forget_win.config(bg="#f0f0f0")

            # Define UI elements for password reset
            Label(self.forget_win, text='Reset Password', font=('Arial', 20, 'bold'), bg="#3f51b5",
                  fg="white", padx=10, pady=5).pack(side=TOP, fill=X)

            # Enter OTP Label and Entry
            Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("Arial", 14)).place(x=20, y=60)
            self.var_otp = StringVar()
            txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("Arial", 14), bg='lightyellow',
                              bd=2, relief=GROOVE)
            txt_reset.place(x=20, y=100, width=250, height=30)

            # Submit Button
            self.btn_reset = Button(self.forget_win, text="SUBMIT", command=self.validate_otp,
                                    font=('Arial', 14), bg="#4caf50", fg="white", bd=2, relief=RAISED,
                                    cursor="hand2")
            self.btn_reset.place(x=280, y=100, width=100, height=30)

            # New Password Label and Entry
            Label(self.forget_win, text="New Password", font=("Arial", 14)).place(x=20, y=160)
            self.var_new_pass = StringVar()
            txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("Arial", 14),
                                 bg='lightyellow', show="*", bd=2, relief=GROOVE)
            txt_new_pass.place(x=20, y=190, width=250, height=30)

            # Confirm Password Label and Entry
            Label(self.forget_win, text="Confirm Password", font=("Arial", 14)).place(x=20, y=225)
            self.var_conf_pass = StringVar()
            txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("Arial", 14),
                               bg='lightyellow', show="*", bd=2, relief=GROOVE)
            txt_c_pass.place(x=20, y=255, width=250, height=30)

            # Update Button
            self.btn_update = Button(self.forget_win, text="Update", command=self.update_password, state=DISABLED,
                                     font=('Arial', 14), bg="#2196f3", fg="white", bd=2, relief=RAISED,
                                     cursor="hand2")
            self.btn_update.place(x=150, y=300, width=100, height=30)

        except Exception as ex:
            # Handle exceptions and show an error message
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

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
        except Exception as ex:
            # Handle exceptions that may occur during database operations
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def validate_otp(self):
        """
        Validates the OTP entered by the user against a pre-stored value. Enables the update button if valid,
        otherwise notifies the user of an invalid OTP.
        """
        try:
            # Convert user input and stored OTP to integers for comparison
            user_otp = int(self.var_otp.get())
            stored_otp = int(self.otp)

            # Check if the OTP entered matches the expected OTP
            if user_otp == stored_otp:
                # Enable the update password button and disable the submit button
                self.btn_update.config(state=NORMAL)
                self.btn_reset.config(state=DISABLED)
            else:
                # Notify user of invalid OTP
                messagebox.showerror("Error", "Invalid OTP, please try again", parent=self.forget_win)
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
