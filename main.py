from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from Transaction import main_dashboard  # ✅ Import from your external file

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x850+0+0")

        # Background image
        self.bg_image = Image.open("images/background.jpeg")
        self.bg = ImageTk.PhotoImage(self.bg_image)
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Login Frame
        frame = Frame(self.root, bg="gray")
        frame.place(x=600, y=200, width=400, height=400)

        # Logo
        img1 = Image.open("images/log.png")
        img1 = img1.resize((100, 100), Image.Resampling.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lbl_img1 = Label(image=self.photoimage1, bg="gray", borderwidth=0)
        lbl_img1.place(x=730, y=200, width=150, height=100)

        # Heading
        get_str = Label(frame, text="Login", font=("times new roman", 20, "bold"), fg="white", bg="gray")
        get_str.place(x=160, y=100)

        # Username
        Label(frame, text="Username :", font=("times new roman", 15, "bold"), fg="white", bg="gray").place(x=50, y=145)
        self.txtuser = Entry(frame, font=("times new roman", 12, "bold"))
        self.txtuser.place(x=200, y=150)

        # Password
        Label(frame, text="Password  :", font=("times new roman", 15, "bold"), fg="white", bg="gray").place(x=50, y=195)
        self.txtpass = Entry(frame, font=("times new roman", 12, "bold"), show="*")
        self.txtpass.place(x=200, y=200)

        # Branch Code
        Label(frame, text="Branch Code :", font=("times new roman", 15, "bold"), fg="white", bg="gray").place(x=50, y=250)
        self.branch_code = Entry(frame, font=("times new roman", 12, "bold"))
        self.branch_code.place(x=200, y=255)

        # Login Button
        loginbtn = Button(frame, command=self.login, text="Login", font=("times new roman", 15, "bold"),
                          bd=3, relief=RIDGE, fg="white", bg="Teal")
        loginbtn.place(x=50, y=320, width=300, height=35)

    def login(self):
        username = self.txtuser.get()
        password = self.txtpass.get()
        branch_code = self.branch_code.get()

        if not username or not password or not branch_code:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = sqlite3.connect("courier_system.db")
            c = conn.cursor()

            # Step 1: Check if username and password are valid
            c.execute("SELECT code FROM user_master WHERE username=? AND password=?", (username, password))
            result = c.fetchone()

            if result:
                db_branch_code = result[0]
                if db_branch_code == branch_code:
                    messagebox.showinfo("Success", f"Login Successful\nWelcome: {username}")
                    self.root.destroy()  # Close the login window
                    main_dashboard(username, branch_code)  # ✅ Call the external function
                else:
                    messagebox.showerror("Error", "Invalid branch code. Please check and try again.")
            else:
                messagebox.showerror("Error", "Invalid username or password.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))



if __name__ == "__main__":
    root = Tk()
    app = Login_window(root)
    root.mainloop()
