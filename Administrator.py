import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_user_master(root):
    def init_db():
        conn = sqlite3.connect("courier_system.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_master (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                username TEXT,
                password TEXT,
                branch TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_user():
        code = code_entry.get()
        username = user_entry.get()
        password = password_entry.get()
        branch = branch_var.get()

        if not (code and username and password and branch) or branch == "Select Branch":
            messagebox.showwarning("Input Error", "All fields are required")
            return

        try:
            conn = sqlite3.connect("courier_system.db")
            c = conn.cursor()
            c.execute("INSERT INTO user_master (code, username, password, branch) VALUES (?, ?, ?, ?)",
                      (code, username, password, branch))
            conn.commit()
            conn.close()
            load_users()
            clear_fields()
            messagebox.showinfo("Success", "User saved successfully",parent=win)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Code already exists",parent=win)

    def load_users():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect("courier_system.db")
        c = conn.cursor()
        c.execute("SELECT code, username, branch FROM user_master")
        rows = c.fetchall()
        conn.close()

        for idx, row in enumerate(rows, start=1):
            tree.insert("", "end", values=(idx, row[0], row[1], row[2]))

    def clear_fields():
        code_entry.delete(0, tk.END)
        user_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        branch_var.set("Select Branch")

    def delete_user():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select User", "No user selected",parent=win)
            return
        item = tree.item(selected)
        code = item['values'][1]
        conn = sqlite3.connect("courier_system.db")
        c = conn.cursor()
        c.execute("DELETE FROM user_master WHERE code=?", (code,))
        conn.commit()
        conn.close()
        load_users()
        messagebox.showinfo("Deleted", "User deleted successfully",parent=win)

    # Setup Toplevel window
    win = tk.Toplevel(root)
    win.title("User Master")
    win.geometry("800x550")
    win.configure(bg="aliceblue")  # Aqua blue background

    # Center the window on the screen
    win.update_idletasks()  # Ensure window dimensions are calculated

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    window_width = 800
    window_height = 550

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # === Form Section ===
    tk.Label(win, text="Code", bg="aliceblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    code_entry = tk.Entry(win)
    code_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="User", bg="aliceblue").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    user_entry = tk.Entry(win)
    user_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="Password", bg="aliceblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(win, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="Branch", bg="aliceblue").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    branch_var = tk.StringVar()
    branch_menu = ttk.Combobox(win, textvariable=branch_var, state="readonly")
    branch_menu["values"] = (
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    )
    branch_menu.set("Select Branch")
    branch_menu.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

    # === Buttons ===
    tk.Button(win, text="Save", width=10, command=save_user, bg="lightgreen", fg="black").grid(row=2, column=0, pady=10)
    tk.Button(win, text="Delete", width=10, command=delete_user, bg="lightcoral", fg="white").grid(row=2, column=1, pady=10)
    tk.Button(win, text="Print", width=10, command=lambda: messagebox.showinfo("Print", "Print clicked"), bg="skyblue", fg="black").grid(row=2, column=2, pady=10)
    tk.Button(win, text="Exit", width=10, command=win.destroy, bg="orange", fg="black").grid(row=2, column=3, pady=10)


    # === Treeview ===
    columns = ("Sr.No", "Code", "User", "Branch")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")
    tree.grid(row=3, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

    # Grid row/column resizing
    for i in range(4):
        win.grid_columnconfigure(i, weight=1)
    win.grid_rowconfigure(3, weight=1)

    # Initialize DB and Load Data
    init_db()
    load_users()
