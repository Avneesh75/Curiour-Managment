import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


#================================Mode Section Start=============================
def open_mode_master_window(root):
    def init_db():
        conn = sqlite3.connect("mode_master.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS mode_master (
                code TEXT PRIMARY KEY,
                mode TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_data():
        code = code_entry.get().strip()
        mode = mode_entry.get().strip()
        if not code or not mode:
            messagebox.showwarning("Input Error", "Both fields are required")
            return
        try:
            conn = sqlite3.connect("mode_master.db")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO mode_master (code, mode) VALUES (?, ?)", (code, mode))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Modes Data saved successfully",parent=window)
            load_data()
            code_entry.delete(0, tk.END)
            mode_entry.delete(0, tk.END)
            code_entry.focus_set()
        except Exception as e:
            messagebox.showerror("Error", str(e),parent=window)

    def delete_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Delete Error", "Please select a record to delete",parent=window)
            return
        item = tree.item(selected[0])
        code = item['values'][1]
        conn = sqlite3.connect("mode_master.db")
        c = conn.cursor()
        c.execute("DELETE FROM mode_master WHERE code = ?", (code,))
        conn.commit()
        conn.close()
        load_data()

    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        conn = sqlite3.connect("mode_master.db")
        c = conn.cursor()
        c.execute("SELECT * FROM mode_master")
        rows = c.fetchall()
        conn.close()
        for i, row in enumerate(rows, start=1):
            tree.insert("", tk.END, values=(i, row[0], row[1]))  # Sr No, Code, Mode

    def exit_app():
        window.destroy()

    # Create new top-level window
    window = tk.Toplevel(root)
    window.title("Mode Master")
    window.geometry("400x460")
    window.resizable(False, False)
    window.configure(bg="aliceblue")

    # Center the window
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Entry Fields
    tk.Label(window, text="Code", bg="aliceblue").place(x=40, y=20)
    code_entry = tk.Entry(window)
    code_entry.place(x=120, y=20, width=200)

    tk.Label(window, text="Mode", bg="aliceblue").place(x=40, y=60)
    mode_entry = tk.Entry(window)
    mode_entry.place(x=120, y=60, width=200)

    # Buttons
    tk.Button(window, text="Save", width=10, command=save_data, bg="lightgreen").place(x=40, y=100)
    tk.Button(window, text="Delete", width=10, command=delete_data, bg="lightcoral").place(x=150, y=100)
    tk.Button(window, text="Exit", width=10, command=exit_app).place(x=260, y=100)

    # Notebook
    notebook = ttk.Notebook(window)
    notebook.place(x=10, y=150, width=380, height=280)

    frame_list = tk.Frame(notebook)
    notebook.add(frame_list, text="List View")

    # Treeview
    tree = ttk.Treeview(frame_list, columns=("SrNo", "Code", "Mode"), show="headings", height=10)
    tree.heading("SrNo", text="Sr No.")
    tree.heading("Code", text="Code")
    tree.heading("Mode", text="Mode")
    tree.column("SrNo", width=50, anchor="center")
    tree.column("Code", width=100, anchor="center")
    tree.column("Mode", width=200, anchor="center")
    tree.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Initialize
    init_db()
    load_data()
#================================Mode Section End=============================

#================================Origin & Destignation========================
def origin_system():
    # Database setup
    conn = sqlite3.connect('city_master.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_code TEXT,
            city TEXT,
            state_code TEXT,
            state TEXT,
            country TEXT
        )
    ''')
    conn.commit()

    def save_entry(*args):
        entry = (
            city_code.get().strip(),
            city_name.get().strip(),
            state_code.get().strip(),
            state_name.get().strip(),
            country_name.get().strip()
        )

        if not all(entry):
            messagebox.showwarning("Validation Error", "All fields are required.",parent=root)
            return

        # Save to DB
        cursor.execute('''
            INSERT INTO city_master (city_code, city, state_code, state, country)
            VALUES (?, ?, ?, ?, ?)
        ''', entry)
        conn.commit()

        tree.insert('', 'end', values=entry)
        clear_fields()

    def clear_fields():
        city_code.delete(0, tk.END)
        city_name.delete(0, tk.END)
        state_code.delete(0, tk.END)
        state_name.delete(0, tk.END)
        country_name.delete(0, tk.END)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Delete Entry", "No entry selected.",parent=root)
            return
        for item in selected:
            tree.delete(item)

    def edit_selected():
        selected = tree.selection()
        if len(selected) != 1:
            messagebox.showinfo("Edit Entry", "Please select one row to edit.",parent=root)
            return

        values = tree.item(selected[0])['values']
        city_code.delete(0, tk.END)
        city_code.insert(0, values[0])

        city_name.delete(0, tk.END)
        city_name.insert(0, values[1])

        state_code.delete(0, tk.END)
        state_code.insert(0, values[2])

        state_name.delete(0, tk.END)
        state_name.insert(0, values[3])

        country_name.delete(0, tk.END)
        country_name.insert(0, values[4])

        tree.delete(selected[0])

    # GUI Layout
    root = tk.Tk()
    root.title("City Master Entry")
    root.geometry("700x500")
    root.configure(bg="aliceblue")
    root.resizable(False, False)

    # --- Center the window ---
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (700 // 2)
    y = (root.winfo_screenheight() // 2) - (500 // 2)
    root.geometry(f"700x500+{x}+{y}")

    main_frame = tk.Frame(root, bg="aliceblue")
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="City Master Entry", font=("Arial", 14, "bold"), bg="aliceblue").pack(pady=10)

    # Entry Form
    form_frame = tk.Frame(main_frame, bg="aliceblue")
    form_frame.pack(pady=10)

    def add_field(label, row):
        tk.Label(form_frame, text=label, bg="aliceblue", anchor="e").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(form_frame, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        return entry

    city_code = add_field("City Code", 0)
    city_name = add_field("City", 1)
    state_code = add_field("State Code", 2)
    state_name = add_field("State", 3)
    country_name = add_field("Country", 4)

    # Buttons
    button_frame = tk.Frame(main_frame, bg="aliceblue")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Save", command=save_entry, width=10, bg="lightgreen", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Edit", command=edit_selected, width=10, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_selected, width=10, bg="lightcoral", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_fields, width=10, bg="#FFC107", fg="white").grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Exit", command=root.destroy, width=10, bg="gray", fg="white").grid(row=0, column=4, padx=5)

    # Treeview
    tree_frame = tk.LabelFrame(main_frame, text="Saved Cities", padx=5, pady=5)
    tree_frame.pack(padx=10, pady=10, fill="x")

    columns = ("City Code", "City", "State Code", "State", "Country")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(side="top", fill="x", padx=10, pady=5)

    # Load existing records
    cursor.execute('SELECT city_code, city, state_code, state, country FROM city_master')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

    root.mainloop()

#==========================================origin & Destignation End=============================


#==========================================Consigner Window =====================================
def open_consigner_master():
    def init_db():
        conn = sqlite3.connect("consigners.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consigners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def fetch_consigners():
        conn = sqlite3.connect("consigners.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consigners")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert_consigner(code, name, mobile, address):
        conn = sqlite3.connect("consigners.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consigners (code, name, mobile, address) VALUES (?, ?, ?, ?)",
                       (code, name, mobile, address))
        conn.commit()
        conn.close()

    def update_consigner(id_, code, name, mobile, address):
        conn = sqlite3.connect("consigners.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE consigners SET code=?, name=?, mobile=?, address=? WHERE id=?",
                       (code, name, mobile, address, id_))
        conn.commit()
        conn.close()

    def delete_consigner(id_):
        conn = sqlite3.connect("consigners.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consigners WHERE id=?", (id_,))
        conn.commit()
        conn.close()

    def save_consigner():
        code = code_var.get()
        name = name_var.get()
        mobile = mobile_var.get()
        address = address_text.get("1.0", tk.END).strip()

        if not (code and name and mobile and address):
            messagebox.showwarning("Validation", "All fields are required.",parent=win)
            return
        else:
            insert_consigner(code, name, mobile, address)

        clear_fields()
        load_table()

    def load_table():
        for row in consigner_table.get_children():
            consigner_table.delete(row)

        data = fetch_consigners()
        for idx, (id_, code, name, mobile, address) in enumerate(data, start=1):
            consigner_table.insert("", "end", iid=id_, values=(idx, code, name, mobile, address))

    def clear_fields():
        code_var.set("")
        name_var.set("")
        mobile_var.set("")
        address_text.delete("1.0", tk.END)
        selected_item_id = None

    def delete_selected():
        selected = consigner_table.selection()
        if selected:
            id_ = selected[0]
            delete_consigner(id_)
            load_table()
        else:
            messagebox.showinfo("Delete", "Please select a record to delete.",parent=win)

    def edit_selected():
        selected = consigner_table.selection()
        if selected:
            selected_item_id = selected[0]
            values = consigner_table.item(selected_item_id, "values")
            code_var.set(values[1])
            name_var.set(values[2])
            mobile_var.set(values[3])
            address_text.delete("1.0", tk.END)
            address_text.insert("1.0", values[4])
        else:
            messagebox.showinfo("Edit", "Please select a record to edit.",parent=win)

    # --- GUI Setup ---
    win = tk.Toplevel()
    win.title("Consigner Master")
    win.geometry("850x550")
    win.configure(bg="aliceblue")

    #======window in Center========================
    win.update_idletasks()
    window_width = win.winfo_width()
    window_height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    code_var = tk.StringVar()
    name_var = tk.StringVar()
    mobile_var = tk.StringVar()

    form_frame = tk.LabelFrame(win, text="Consigner Details", bg="aliceblue", font=("Arial", 10, "bold"), padx=10, pady=10)
    form_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(form_frame, text="Code:", bg="aliceblue").grid(row=0, column=0, sticky="w")
    tk.Entry(form_frame, textvariable=code_var, width=20).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Name:", bg="aliceblue").grid(row=0, column=2, sticky="w")
    tk.Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Mobile:", bg="aliceblue").grid(row=1, column=0, sticky="w")
    tk.Entry(form_frame, textvariable=mobile_var, width=20).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Address:", bg="aliceblue").grid(row=1, column=2, sticky="nw")
    address_text = tk.Text(form_frame, width=30, height=3)
    address_text.grid(row=1, column=3, padx=5, pady=5)

    btn_frame = tk.Frame(win, bg="aliceblue")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Save", command=save_consigner, width=10, bg="lightgreen").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Edit", command=edit_selected, width=10, bg="khaki").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_selected, width=10, bg="lightcoral").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear", command=clear_fields, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Exit", command=win.destroy, width=10).pack(side="left", padx=5)

    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Sr No", "Code", "Name", "Mobile", "Address")
    consigner_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        consigner_table.heading(col, text=col)
        consigner_table.column(col, anchor="center", width=120 if col != "Address" else 200)
    consigner_table.pack(fill="both", expand=True)

    init_db()
    load_table()

#=======================================Consigner window End============================================

