from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Correct this import


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed BY")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        #====images====
        self.phone_image = PhotoImage(file="images/phone.png")
        self.lbl_Phone_image = Label(self.root, image=self.phone_image, bd=0).place(x=200, y=50)

        #====Login Frame======
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30,
                                                                                                         relwidth=1)

        lbl_user = Label(login_frame, text="Username", font=("Andlus", 15), bg="white", fg="#767171").place(x=50, y=100)
        self.username = StringVar()
        self.password = StringVar()
        txt_username = Entry(login_frame, textvariable=self.username, font=("times new roman", 15), bg="#ECECEC").place(
            x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andlus", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15),
                         bg="#ECECEC").place(x=50, y=240, width=250)

        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15),
                           bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white",
                           cursor="hand2").place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)

        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(
            x=150, y=355)

        btn_forget = Button(login_frame, text="Forget Password?", font=("times new roman", 13), bg="white",
                            fg="#00759E", bd=0, activeforeground="#00759E", activebackground="white").place(x=100,
                                                                                                            y=390)

        #====Frame 2===========
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        lvl_reg = Label(register_frame, text="Dont have an account?", font=("times new roman", 13), bg="white").place(
            x=40, y=20)

        btn_signup = Button(register_frame, text="Sign Up", font=("times new roman", 13, "bold"), bg="white",
                            fg="#00759E", bd=0, activeforeground="#00759E", activebackground="white").place(x=200,
                                                                                                            y=17)
        #======Animation Images=====
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)
    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.username.get() != "Rangesh" or self.password.get() != "123456":
            messagebox.showerror("Error", "Invalid Username or Password\nTry again with correct credentials")
        else:
            messagebox.showinfo("Information",
                                f"Welcome : {self.username.get()}\nYour Password : {self.password.get()}")


root = Tk()
obj = Login_System(root)
root.mainloop()
