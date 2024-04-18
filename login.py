# Import necessary modules
import json
import os
import smtplib
import sqlite3
import subprocess
from random import randint
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Style

from cryptography.fernet import Fernet


# Define the main class for the login system
class LoginSystem:
    def __init__(self, root):
        # Initialize variables and GUI settings
        self.forget_win = None
        self.btn_reset = None
        self.root = root
        self.root.title("Inventory Management System | Ariatech")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp = ''

        self.var_otp = StringVar()
        self.var_new_pass = StringVar()
        self.var_conf_pass = StringVar()

        # Load encryption key and initialize cipher
        self.cipher = self.load_key_and_initialize_cipher()

        # ====images====
        self.phone_image = PhotoImage(file="images/phone.png")
        Label(self.root, image=self.phone_image, bd=0).place(x=200, y=50)

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
        self.images = [PhotoImage(file="images/im1.png"), PhotoImage(file="images/im2.png"),
                       PhotoImage(file="images/im3.png")]
        self.image_index = 0

        # Set up the label to display images
        self.lbl_change_image = Label(self.root, image=self.images[self.image_index], bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)

        # Start the animation
        self.animate()

    # All Functions

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
        Handles the login functionality:
        - Connects to the database to retrieve user details.
        - Validates user credentials.
        - Redirects the user based on their role.
        """
        try:
            # Connect to the database
            with sqlite3.connect(database=r'ims.db') as con:
                cur = con.cursor()

                # Check if the employee ID or password fields are empty
                if not self.employee_id.get() or not self.password.get():
                    messagebox.showerror("Error", "All fields are required", parent=self.root)
                    return

                # Retrieve user type and encrypted password from the database
                cur.execute("SELECT utype, pass FROM employee WHERE eid=?", (self.employee_id.get(),))
                user = cur.fetchone()

                # Handle invalid login credentials
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                    return

                # Decrypt the stored password
                decrypted_password = self.cipher.decrypt(user[1].encode()).decode()

                # Validate the decrypted password with the user input
                if decrypted_password == self.password.get():
                    # Navigate to the appropriate dashboard based on the user type
                    self.root.destroy()
                    if user[0] == "Admin":
                        subprocess.run(["python", "dashboard.py"], check=True)
                    else:
                        subprocess.run(["python", "billing.py"], check=True)
                else:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def forget_window(self):
        """
        Handles forget password functionality.
        """
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
                return

            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("select email from employee where eid=?", (self.employee_id.get(),))
            email_encrypted = cur.fetchone()  # This will fetch the encrypted email
            con.close()  # Close the connection early
            if email_encrypted is None:
                messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                return

            # Decrypt the email before sending it
            email = self.cipher.decrypt(email_encrypted[0].encode()).decode()  # Decrypting the email

            # =========Forget Window=============
            # Call send_email_function
            result = self.send_email(email)
            if result != 's':  # Assuming 's' means success, based on your send_email method
                messagebox.showerror("Error", "Failed to send email. Please check your connection and try again.",
                                     parent=self.root)
                return

            self.forget_win = Toplevel(self.root)
            self.forget_win.title("Reset Password")
            self.forget_win.geometry("400x400")
            self.forget_win.config(bg="#f0f0f0")

            # Title Label
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
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def update_password(self):
        """
        Updates the password in the database after validation.
        """
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "Password is required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "Password must be same", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                # Encrypt the new password before updating it in the database
                encrypted_password = self.cipher.encrypt(self.var_new_pass.get().encode()).decode()
                cur.execute("Update employee SET pass=? where eid=?", (encrypted_password, self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def validate_otp(self):
        """
        Validates the OTP entered by the user.
        """
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error", "Invalid OTP, Try again", parent=self.forget_win)

    def load_credentials(self):
        """
        Loads email credentials from a configuration file.
        """
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config['email'], config['password']

    def send_email(self, to_):
        """
        Sends an email with a randomly generated OTP to the provided email address.
        """
        # Load credentials from a JSON file
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
            email_ = config['email']
            pass_ = config['password']
        except IOError:
            print("Failed to read configuration file")
            return 'f'
        except KeyError:
            print("Invalid configuration settings")
            return 'f'

        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            s = smtplib.SMTP(smtp_server, smtp_port)
            s.starttls()
            s.login(email_, pass_)

            # Generate a six-digit OTP
            self.otp = randint(100000, 999999)

            subj = 'IMS-Reset Password OTP'
            msg = f'Dear Sir/Madam,\n\nYour Reset OTP is {self.otp}.\n\nWith Regards,\nIMS Team'
            msg = f"Subject:{subj}\n\n{msg}"
            s.sendmail(email_, to_, msg)
            s.quit()
            return 's'
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return 'f'


root = Tk()
obj = LoginSystem(root)
root.mainloop()
