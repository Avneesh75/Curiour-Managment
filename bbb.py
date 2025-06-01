import tkinter as tk
from tkinter import ttk, messagebox, Menu
from datetime import datetime
from PIL import Image, ImageTk
import sqlite3
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import BooleanVar, Checkbutton
import re


# import files and link 
from reports import create_checklist_gui
from Administrator import open_user_master
from Master import open_mode_master_window,open_consigner_master,origin_system

def main_dashboard(username):
    root = tk.Tk()
    root.title("Python (System of Courier Operation)")
    root.geometry("1800x1000")
    root.resizable(True, True)

    # =================== MENU BAR ====================
    menubar = Menu(root)

    def open_booking():
        build_booking_gui()

    def open_checklist():
        create_checklist_gui(root)

    def open_master_user():
        open_user_master(root)

    def open_dispatch():
        build_manifest_gui()

    def open_receving():
        ReceivingWindow(root)



    # Transaction Module
    transaction_menu = Menu(menubar, tearoff=0)
    transaction_menu.add_command(label="Booking", command=open_booking)
    transaction_menu.add_command(label="Dispatch", command=open_dispatch)
    transaction_menu.add_command(label="Receiving", command=open_receving)
    menubar.add_cascade(label="Transaction", menu=transaction_menu)

    # Reports Module
    report_menu = Menu(menubar, tearoff=0)
    report_menu.add_command(label="Checklist", command=open_checklist)
    menubar.add_cascade(label="Reports", menu=report_menu)

    #Administrator Module
    report_menu = Menu(menubar, tearoff=0)
    report_menu.add_command(label="User Create", command=open_master_user)
    menubar.add_cascade(label="Administrator", menu=report_menu)

    #===========Master Module ================

    def open_origin():
        origin_system()

    def open_mode():
        open_mode_master_window(root)

    def open_consiger():
        open_consigner_master()
        

    master_menu = Menu(menubar, tearoff=0)
    # Add "Mode" item with function binding
    master_menu.add_command(label="Mode", command=open_mode)
    master_menu.add_command(label="Destination & Origin", command=open_origin)
    master_menu.add_command(label="Client", command=open_consiger)


    # Add other items (excluding "Mode")
    for item in ["Zone", "Network", "Gateway & Forwarder", "Branch", "Location","GST/Service Tax", "Employee", "Supplier", "Consignee", "Delivery Boy/Agent Master", "Currency",
                "Add on Expenses", "Fuel Charges", "Calc", "Product", "Category", "Status Master", "Type",
                "General Master"]:
        master_menu.add_command(label=item)

    menubar.add_cascade(label="Master", menu=master_menu)

    # for label in ["Maintenance", "Administrator", "Reports", "Invoice System",
    #               "Customer Support System", "M.I.S.", "Change Password", "Calculator"]:
    #     menubar.add_cascade(label=label)

    root.config(menu=menubar)

    # =================== TOP BAR ====================
    top_frame = tk.Frame(root, height=30, bg="aliceblue")
    top_frame.pack(fill=tk.X, side=tk.TOP)

    date_label = tk.Label(top_frame, text=datetime.now().strftime("%d/%m/%Y"), bg="aliceblue")
    date_label.pack(side=tk.LEFT, padx=10)

    user_label = tk.Label(top_frame, text=f"{username}", bg="aliceblue", font=('Arial', 10, 'bold'), fg='purple')
    user_label.pack(side=tk.RIGHT, padx=20)

    # =================== BACKGROUND IMAGE ====================
    image = Image.open("images/background.jpeg")
    image = image.resize((1550, 850), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_img)
    bg_label.image = bg_img  # keep a reference
    bg_label.place(x=0, y=30)
    root.mainloop()

# =================== Booking Window ====================
def build_booking_gui():
    def connect_db():
        conn = sqlite3.connect("Booking.db")
        conn.execute("PRAGMA foreign_keys = ON")
        c = conn.cursor()

        # Booking Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS booking (
                awb_no TEXT PRIMARY KEY,
                branch TEXT,
                client TEXT,
                date TEXT,
                origin TEXT,
                zip TEXT,
                destination TEXT,
                network TEXT,
                mode TEXT,
                pickup_by TEXT,
                commodity TEXT,
                consignor_name TEXT,
                consignor_mobile TEXT,
                consignor_address1 TEXT,
                consignor_address2 TEXT,
                consignee_name TEXT,
                consignee_mobile TEXT,
                consignee_address1 TEXT,
                consignee_address2 TEXT,
                description TEXT,
                remarks TEXT
                  
            )
        """)

        # Invoice Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS invoice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                awb_no TEXT,
                inv_no TEXT,
                value TEXT,
                eway TEXT,
                FOREIGN KEY (awb_no) REFERENCES booking(awb_no) ON DELETE CASCADE
            )
        """)

        # Dimensions Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS dimensions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                awb_no TEXT,
                pkg TEXT,
                length TEXT,
                width TEXT,
                height TEXT,
                actual_weight TEXT,
                vol_weight TEXT,
                FOREIGN KEY (awb_no) REFERENCES booking(awb_no) ON DELETE CASCADE
            )
        """)
        conn.commit()
        return conn, c

    # Assuming you're calling this early
    conn, cur = connect_db()

    def save_entry():
        try:
            # Collect entry values from 'entries' dictionary
            data = {label: entries[label].get().strip() for label in entries}

            # Check mandatory fields
            required_fields = {
                "Awb No.": data.get("Awb No."),
                "Branch": data.get("Branch"),
                "Date": data.get("Date"),
                "Mode": entries["Mode"].get().strip(),  # from dropdown or combobox
                "Pickup By": data.get("Pickup By"),
                "Client":data.get("Client")
            }

            # Check consignor manually (not in entries dict)
            consignor_required = {
                "Consignor Name": name_entry.get().strip(),
                "Consignor Mobile": mobile_entry.get().strip(),
                "Consignor Address 1": address1_entry.get().strip()
            }

            # Combine all required fields
            all_required_fields = {**required_fields, **consignor_required}

            # Find missing fields
            missing_fields = [field for field, value in all_required_fields.items() if not value]

            if missing_fields:
                status_label.config(
                    text=f"❌ Required fields : {', '.join(missing_fields)}", fg="red"
                )
                return

            # Build the booking_values tuple (21 fields)
            booking_values = (
                data["Awb No."], data["Branch"], data["Client"], data["Date"],
                data["Origin"], data["Zip Code"], data["Destination"], data["Network"],
                entries["Mode"].get().strip(), data["Pickup By"], data["Commodity"],
                name_entry.get().strip(), mobile_entry.get().strip(), address1_entry.get().strip(),
                address2_entry.get().strip(), consignee_name_entry.get().strip(),
                consignee_mobile_entry.get().strip(), consignee_address_entry.get().strip(),
                consignee_address2_entry.get().strip(), description_entry.get().strip(),
                remarks_entry.get().strip()
            )

            if len(booking_values) != 21:
                status_label.config(text="❌ Incomplete booking form. Please check all fields.", fg="red")
                return

            # Insert into booking table
            cur.execute("""
                INSERT INTO booking (
                    awb_no, branch, client, date, origin, zip, destination,
                    network, mode, pickup_by, commodity,
                    consignor_name, consignor_mobile, consignor_address1, consignor_address2,
                    consignee_name, consignee_mobile, consignee_address1, consignee_address2,
                    description, remarks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, booking_values)

            # Insert dimensions
            for row in tree.get_children():
                dim_values = tree.item(row, "values")
                if len(dim_values) != 6:
                    continue
                cur.execute("""
                    INSERT INTO dimensions (
                        awb_no, pkg, length, width, height, actual_weight, vol_weight
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["Awb No."],
                    dim_values[0], dim_values[1], dim_values[2], dim_values[3],
                    dim_values[4], dim_values[5]
                ))

            # Insert invoices
            for row in invoice_tree.get_children():
                invoice_values = invoice_tree.item(row, "values")
                if len(invoice_values) < 4:
                    continue
                cur.execute("""
                    INSERT INTO invoice (
                        awb_no, inv_no, value, eway
                    ) VALUES (?, ?, ?, ?)
                """, (
                    data["Awb No."],
                    invoice_values[1], invoice_values[2], invoice_values[3]
                ))

            conn.commit()
            messagebox.showinfo("Success", "✅ Your booking has been saved successfully.", parent=root)


            # Clear all entries in the 'entries' dictionary
            for key, entry in entries.items():
                # Handle readonly entries: temporarily enable, clear, and restore
                if isinstance(entry, tk.Entry) and str(entry.cget("state")) == "readonly":
                    entry.config(state="normal")
                    entry.delete(0, 'end')
                    entry.config(state="readonly")
                else:
                    entry.delete(0, 'end')

            # Reset checkboxes (set to 0/unchecked)
            freeze_consignee_var.set(0)
            # Add other checkbox vars here if any (e.g., freeze_dimension_var.set(0))

            # Clear other text fields conditionally
            if not freeze_consignee_var.get():
                consignee_name_entry.delete(0, 'end')
                consignee_mobile_entry.delete(0, 'end')
                consignee_address_entry.delete(0, 'end')
                consignee_address2_entry.delete(0, 'end')
                description_entry.delete(0, 'end')
                remarks_entry.delete(0, 'end')

            # Always clear consignor fields
            name_entry.delete(0, 'end')
            mobile_entry.delete(0, 'end')
            address1_entry.delete(0, 'end')
            address2_entry.delete(0, 'end')

            # Clear consignee fields again to ensure no residuals
            consignee_name_entry.delete(0, 'end')
            consignee_mobile_entry.delete(0, 'end')
            consignee_address_entry.delete(0, 'end')
            consignee_address2_entry.delete(0, 'end')
            description_entry.delete(0, 'end')
            remarks_entry.delete(0, 'end')

            # Clear dimension and invoice tables
            for item in tree.get_children():
                tree.delete(item)
            for item in invoice_tree.get_children():
                invoice_tree.delete(item)


                # Clear tree views
                for row in tree.get_children():
                    tree.delete(row)
                for row in invoice_tree.get_children():
                    invoice_tree.delete(row)

                # Auto-clear success message
                status_label.after(3000, lambda: status_label.config(text=""))

        except sqlite3.IntegrityError:
            status_label.config(text="❌ AWB No. already exists. Please enter a unique AWB number.", fg="red")
        except KeyError as ke:
            status_label.config(text=f"❌ Missing or incorrect field: {ke}", fg="red")
        except Exception as e:
            status_label.config(text=f"❌ Unexpected error: {str(e)}", fg="red")


    def delete_entry():
        awb_no = entries["Awb No."].get().strip()
        if awb_no:
            # Check if AWB exists
            cur.execute("SELECT 1 FROM booking WHERE awb_no=?", (awb_no,))
            if cur.fetchone() is None:
                messagebox.showinfo("Info", f"AWB No. {awb_no} not found.",parent=root)
                return

            # Delete related records
            cur.execute("DELETE FROM dimensions WHERE awb_no=?", (awb_no,))
            cur.execute("DELETE FROM invoice WHERE awb_no=?", (awb_no,))
            cur.execute("DELETE FROM booking WHERE awb_no=?", (awb_no,))

            conn.commit()
            messagebox.showinfo("Deleted", f"Booking with AWB No. {awb_no} has been deleted.",parent=root)
        else:
            messagebox.showwarning("Missing", "Enter AWB No. to delete.",parent=root)


    root = tk.Tk()
    root.title("Courier Booking")
    root.geometry("1380x720")
    root.configure(bg='lightgrey')
    
    #======window in Center========================
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")



    #==============for consignor data fetch variables====================
    global name_entry, mobile_entry, address1_entry, address2_entry
    name_entry = tk.Entry(root, width=35)
    mobile_entry = tk.Entry(root, width=20)
    address1_entry = tk.Entry(root, width=65)
    address2_entry = tk.Entry(root, width=65)


    style = ttk.Style()
    style.configure("Treeview", rowheight=22, font=('Segoe UI', 9))

    top_frame = tk.Frame(root, bg="black", height=25)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Modified by", bg="black", fg="aliceblue").place(x=300, y=2)
    tk.Label(top_frame, text="Checked by", bg="black", fg="aliceblue").place(x=1100, y=2)

    left_frame = tk.Frame(root, bg="aliceblue", relief="groove", bd=2)
    left_frame.place(x=5, y=30, width=680, height=670)

    right_frame = tk.Frame(root, bg="lightgrey", relief="groove", bd=2)
    right_frame.place(x=690, y=30, width=685, height=670)

    labels = [
        ("Awb No.", 10), ("Branch", 40), ("Client", 70), ("Date", 100),
        ("Origin", 130), ("Zip Code", 160), ("Destination", 190),
        ("Network", 220), ("Mode", 250), ("Commodity", 280),
        ("Pickup By", 310)
    ]
    # fetch consignor data 
    entries = {}
    def fetch_consignor_details(event=None):
        client_text = entries.get("Client", None)
        if client_text is None:
            return
        selected = client_text.get().strip()
        
        if " - " in selected:
            code = selected.split(" - ")[0]  # Extract code before the ' - '
        else:
            code = selected  # Fallback if format not matched

        if not code:
            return

        try:
            conn = sqlite3.connect("consigners.db")
            cur = conn.cursor()
            cur.execute("SELECT name, mobile, address FROM consigners WHERE code=?", (code,))
            result = cur.fetchone()
            conn.close()

            if result:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, result[0])

                mobile_entry.delete(0, tk.END)
                mobile_entry.insert(0, result[1])

                address1_entry.delete(0, tk.END)
                address1_entry.insert(0, result[2])

                address2_entry.delete(0, tk.END)
                address2_entry.insert(0, "")  # Optionally fill or leave blank
            else:
                messagebox.showwarning("Not Found", f"No consignor found for code '{code}'",parent=root)
        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent=root)

        
    # Declare these at the top-level scope (so fetch_mode_description can use them)
    entries = {}
    def fetch_mode_description(event=None):
        code = entries["Mode"].get().strip()  # use the direct reference
        if not code:
            return
        try:
            conn = sqlite3.connect("mode_master.db")
            cur = conn.cursor()
            cur.execute("SELECT mode FROM mode_master WHERE code=?", (code,))
            result = cur.fetchone()
            conn.close()
            if result:
                mode_desc_entry.config(state='normal')
                mode_desc_entry.delete(0, tk.END)
                mode_desc_entry.insert(0, result[0])
                mode_desc_entry.config(state='readonly')
            else:
                messagebox.showwarning("Not Found", f"No mode found for code '{code}'",parent=root)
                mode_desc_entry.config(state='normal')
                mode_desc_entry.delete(0, tk.END)
                # mode_desc_entry.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent=root)
    
    #=== Function to Fetch Origin and Destination Descriptions========

    def get_codes():
        try:
            # Fetch mode codes
            conn_mode = sqlite3.connect("mode_master.db")
            cur_mode = conn_mode.cursor()
            cur_mode.execute("SELECT DISTINCT code FROM mode_master WHERE code IS NOT NULL")
            mode_codes = [row[0] for row in cur_mode.fetchall()]
            conn_mode.close()

            # Fetch city and state codes
            conn_city = sqlite3.connect("city_master.db")
            cur_city = conn_city.cursor()
            cur_city.execute("SELECT DISTINCT city_code FROM city_master WHERE city_code IS NOT NULL")
            city_codes = [row[0] for row in cur_city.fetchall()]
            cur_city.execute("SELECT DISTINCT state_code FROM city_master WHERE state_code IS NOT NULL")
            state_codes = [row[0] for row in cur_city.fetchall()]
            conn_city.close()

            # Fetch client code and name
            conn_consigners = sqlite3.connect("consigners.db")
            cur_consigners = conn_consigners.cursor()
            cur_consigners.execute("SELECT code, name FROM consigners WHERE code IS NOT NULL AND name IS NOT NULL")
            client_codes_and_names = cur_consigners.fetchall()
            conn_consigners.close()

            return mode_codes, city_codes, state_codes, client_codes_and_names

        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent=root)
            return [], [], [], []
            
    def fetch_origin_destination_description(event=None):
        widget = event.widget
        code = widget.get().strip()
        if not code:
            return

        # Determine which field (e.g., Origin or Destination) triggered the event.
        label = None
        for key, entry in entries.items():
            if entry == widget:
                label = key
                break

        try:
            conn = sqlite3.connect("city_master.db")
            cur = conn.cursor()

            result = None
            if label == "Origin":
                # For Origin, we fetch details using the city_code column.
                cur.execute("SELECT city FROM city_master WHERE city_code=?", (code,))
                result = cur.fetchone()
            elif label == "Destination":
                # For Destination, we fetch details using the state_code column.
                cur.execute("SELECT state FROM city_master WHERE state_code=?", (code,))
                result = cur.fetchone()
            conn.close()

            if result:
                if label == "Origin":
                    origin_desc_entry.config(state='normal')
                    origin_desc_entry.delete(0, tk.END)
                    origin_desc_entry.insert(0, result[0])
                    origin_desc_entry.config(state='readonly')
                elif label == "Destination":
                    destination_desc_entry.config(state='normal')
                    destination_desc_entry.delete(0, tk.END)
                    destination_desc_entry.insert(0, result[0])  # Fixed index
                    destination_desc_entry.config(state='readonly')
            else:
                messagebox.showwarning("Not Found", f"No {label} found for code '{code}'",parent=root)
                if label == "Origin":
                    origin_desc_entry.config(state='normal')
                    origin_desc_entry.delete(0, tk.END)
                    origin_desc_entry.config(state='readonly')
                elif label == "Destination":
                    destination_desc_entry.config(state='normal')
                    destination_desc_entry.delete(0, tk.END)
                    destination_desc_entry.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent=root)

    def fetch_client_name(event):
        selected = entries["Client"].get()
        if " - " in selected:
            code, name = selected.split(" - ", 1)
            entries["ClientName"].config(state="normal")
            entries["ClientName"].delete(0, tk.END)
            entries["ClientName"].insert(0, name)
            entries["ClientName"].config(state="readonly")

    # --- Dummy placeholder functions for bindings ---

    

    mode_code_list, city_code_list, state_code_list, client_list = get_codes()
    client_code_name_list = [f"{code} - {name}" for code, name in client_list]

    dropdown_data = {
        "Client": client_code_name_list,
        "Mode": mode_code_list,
        "Origin": city_code_list,
        "Destination": state_code_list
    }

    vars_dict = {
        "Client": tk.StringVar(),
        "Mode": tk.StringVar(),
        "Origin": tk.StringVar(),
        "Destination": tk.StringVar()
    }

    entries = {}

    for label, y in labels:
        tk.Label(left_frame, text=label, bg="aliceblue").place(x=10, y=y)

        if label == "Date":
            date_entry = DateEntry(left_frame, width=27, date_pattern='dd-mm-yyyy')
            date_entry.place(x=100, y=y)
            entries[label] = date_entry

        elif label == "Commodity":
            type_cb = ttk.Combobox(left_frame, values=["DOC", "NON-DOC"], width=27, state="readonly")
            type_cb.set("DOC")
            type_cb.place(x=100, y=y)
            entries[label] = type_cb

        elif label == "Mode":
            mode_cb = ttk.Combobox(left_frame, values=mode_code_list, width=8, state="readonly", textvariable=vars_dict["Mode"])
            mode_cb.place(x=100, y=y)
            mode_cb.bind("<<ComboboxSelected>>", fetch_mode_description)
            entries["Mode"] = mode_cb

            mode_desc_entry = tk.Entry(left_frame, width=20, state="readonly")
            mode_desc_entry.place(x=180, y=y)
            entries["ModeDesc"] = mode_desc_entry

        elif label == "Origin":
            origin_cb = ttk.Combobox(left_frame, values=city_code_list, width=8, state="readonly", textvariable=vars_dict["Origin"])
            origin_cb.place(x=100, y=y)
            origin_cb.bind("<<ComboboxSelected>>", fetch_origin_destination_description)
            entries["Origin"] = origin_cb

            origin_desc_entry = tk.Entry(left_frame, width=20, state="readonly")
            origin_desc_entry.place(x=180, y=y)
            entries["OriginDesc"] = origin_desc_entry

        elif label == "Destination":
            destination_cb = ttk.Combobox(left_frame, values=state_code_list, width=8, state="readonly", textvariable=vars_dict["Destination"])
            destination_cb.place(x=100, y=y)
            destination_cb.bind("<<ComboboxSelected>>", fetch_origin_destination_description)
            entries["Destination"] = destination_cb

            destination_desc_entry = tk.Entry(left_frame, width=20, state="readonly")
            destination_desc_entry.place(x=180, y=y)
            entries["DestinationDesc"] = destination_desc_entry

        elif label == "Client":
            client_cb = ttk.Combobox(left_frame, values=client_code_name_list, width=27, state="readonly", textvariable=vars_dict["Client"])
            client_cb.place(x=100, y=y)
            client_cb.bind("<<ComboboxSelected>>", lambda e: [fetch_client_name(e), fetch_consignor_details(e)])
            entries["Client"] = client_cb

            client_name_entry = tk.Entry(left_frame, width=20, state="readonly")
            client_name_entry.place(x=300, y=y)
            entries["ClientName"] = client_name_entry

        else:
            entry = tk.Entry(left_frame, width=30)
            entry.place(x=100, y=y)
            entries[label] = entry

    # Key bindings to open combobox dropdown using F1–F4 and Ctrl+F1–F4
        key_map = {
            "<F1>": "Client",
            "<F2>": "Origin",
            "<F3>": "Destination",
            "<F4>": "Mode",
            "<Control-F1>": "Client",
            "<Control-F2>": "Origin",
            "<Control-F3>": "Destination",
            "<Control-F4>": "Mode"
        }

        for key, field in key_map.items():
            root.bind(key, lambda e, f=field: entries[f].event_generate("<Down>"))

        

    #====================================== Dimension Frame======================================

    dim_frame = tk.LabelFrame(left_frame, text="Dimension", bg="black", fg="aliceblue")
    dim_frame.place(x=10, y=380, width=650, height=210)

    # Unit dropdown
    unit_cb = ttk.Combobox(dim_frame, values=["Centimeter", "Inch"], width=12)
    unit_cb.set("Centimeter")
    unit_cb.place(x=10, y=5)

    # Entry fields
    dim_entries = {}
    labels = ["Height", "Length", "Width", "Pkgs"]
    for i, label in enumerate(labels):
        entry = tk.Entry(dim_frame, width=8)
        entry.place(x=110 + i * 90, y=5)
        dim_entries[label] = entry

    # Treeview setup
    tree = ttk.Treeview(dim_frame, columns=("Sr", "Height", "Length", "Width", "Weight", "Pkgs"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=85 , anchor="center")
    tree.place(x=0, y=35, width=640, height=140)

    # Function to add entry to treeview on Enter key
    def add_dimension_row(event=None):
        try:
            height = float(dim_entries["Height"].get())
            length = float(dim_entries["Length"].get())
            width = float(dim_entries["Width"].get())
            pkgs = int(dim_entries["Pkgs"].get())
            weight = round((length * width * height) / 5000, 2)
            sr_no = len(tree.get_children()) + 1
            tree.insert("", "end", values=(sr_no, height, length, width, weight, pkgs))
            for entry in dim_entries.values():
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.",parent=root)

    # Bind Enter key to "Pkgs" entry
    dim_entries["Pkgs"].bind("<Return>", add_dimension_row)

    # Function to delete selected row
    def delete_selected_row():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to delete.",parent=root)
            return
        for item in selected:
            tree.delete(item)

    # Delete Button
    tk.Button(dim_frame, text="Delete", command=delete_selected_row).place(x=550, y=2)



    tk.Label(left_frame, text="Vol.Wt", bg="aliceblue").place(x=10, y=600)
    tk.Entry(left_frame, width=10).place(x=70, y=600)
    tk.Label(left_frame, text="B.Wt", bg="aliceblue").place(x=10, y=630)
    tk.Entry(left_frame, width=10).place(x=70, y=630)
    tk.Label(left_frame, text="Total Pkg", bg="aliceblue").place(x=220, y=600)
    tk.Entry(left_frame, width=10).place(x=300, y=600)
    tk.Label(left_frame, text="Act Wt", bg="aliceblue").place(x=220, y=630)
    tk.Entry(left_frame, width=10).place(x=300, y=630)
    payment_cb = ttk.Combobox(left_frame, values=["Credit", "Cash"], width=12)
    payment_cb.set("Credit")
    payment_cb.place(x=530, y=610)

    #========================= Consignor ===============================

    tk.Label(left_frame, text="Client", bg="aliceblue").place(x=10, y=70)
    # entries["Client"] = tk.Entry(left_frame, width=30)
    # entries["Client"].place(x=100, y=70)
    entries["Client"].bind("<Return>", fetch_consignor_details)

    # --- RIGHT FRAME: Consignor Info Fields ---
    tk.Label(right_frame, text="Consignor Name", bg="lightgrey").place(x=10, y=10)
    name_entry = tk.Entry(right_frame, width=35)
    name_entry.place(x=130, y=10)

    tk.Label(right_frame, text="Mobile", bg="lightgrey").place(x=350, y=10)
    mobile_entry = tk.Entry(right_frame, width=20)
    mobile_entry.place(x=400, y=10)

    tk.Label(right_frame, text="Address 1", bg="lightgrey").place(x=10, y=40)
    address1_entry = tk.Entry(right_frame, width=65)
    address1_entry.place(x=130, y=40)

    tk.Label(right_frame, text="Address 2", bg="lightgrey").place(x=10, y=70)
    address2_entry = tk.Entry(right_frame, width=65)
    address2_entry.place(x=130, y=70)

    # ✅ Status Label - Place it visibly below the other fields
    status_label = tk.Label(right_frame, text="", font=("Arial", 10), fg="green", bg="lightgrey")
    status_label.place(x=130, y=100)

    #======================== Consignee ================================
    
    freeze_consignee_var = BooleanVar()
    freeze_consignee_checkbox = Checkbutton(
        right_frame, variable=freeze_consignee_var, bg="lightgrey"
    )
    freeze_consignee_checkbox.place(x=600, y=140)  # Adjusted to visible position

    # Consignee Fields
    def validate_mobile_input(P):
        return P.isdigit() and len(P) <= 10 or P == ""

    def validate_text(P):
        return re.fullmatch(r"[A-Za-z\s]*", P) is not None

    # Register validation commands
    vcmd_mobile = (root.register(validate_mobile_input), '%P')
    vcmd_text = (root.register(validate_text), '%P')

    # Labels and Entries
    tk.Label(right_frame, text="Consignee Name", bg="lightgrey").place(x=10, y=140)
    consignee_name_entry = tk.Entry(right_frame, width=35, validate="key", validatecommand=vcmd_text)
    consignee_name_entry.place(x=130, y=140)

    tk.Label(right_frame, text="Mobile", bg="lightgrey").place(x=350, y=140)
    consignee_mobile_entry = tk.Entry(right_frame, width=20, validate="key", validatecommand=vcmd_mobile)
    consignee_mobile_entry.place(x=400, y=140)

    tk.Label(right_frame, text="Address 1", bg="lightgrey").place(x=10, y=170)
    consignee_address_entry = tk.Entry(right_frame, width=65, validate="key", validatecommand=vcmd_text)
    consignee_address_entry.place(x=130, y=170)

    tk.Label(right_frame, text="Address 2", bg="lightgrey").place(x=10, y=200)
    consignee_address2_entry = tk.Entry(right_frame, width=65, validate="key", validatecommand=vcmd_text)
    consignee_address2_entry.place(x=130, y=200)

    tk.Label(right_frame, text="Description", bg="lightgrey").place(x=10, y=230)
    description_entry = tk.Entry(right_frame, width=65, validate="key", validatecommand=vcmd_text)
    description_entry.place(x=130, y=230)

    tk.Label(right_frame, text="Remarks", bg="lightgrey").place(x=10, y=260)
    remarks_entry = tk.Entry(right_frame, width=65, validate="key", validatecommand=vcmd_text)
    remarks_entry.place(x=130, y=260)

    # Toggle Freeze Function
    def toggle_consignee_freeze():
        state = 'disabled' if freeze_consignee_var.get() else 'normal'
        consignee_name_entry.config(state=state)
        consignee_mobile_entry.config(state=state)
        consignee_address_entry.config(state=state)
        consignee_address2_entry.config(state=state)
        description_entry.config(state=state)
        remarks_entry.config(state=state)

    freeze_consignee_var.trace_add('write', lambda *args: toggle_consignee_freeze())

#======================== Sale window Start ================================
    sale_frame = tk.Frame(right_frame, bg="pink")
    sale_frame.place(x=10, y=310, width=660, height=180)
    tk.Label(sale_frame, text="Sale Invoice Detail", bg="pink", font=('Segoe UI', 10, 'bold')).place(x=5, y=0)

    # Input Fields
    tk.Label(sale_frame, text="Inv No.", bg="pink").place(x=5, y=30)
    inv_no_entry = tk.Entry(sale_frame, width=15)
    inv_no_entry.place(x=60, y=30)

    tk.Label(sale_frame, text="Value", bg="pink").place(x=200, y=30)
    inv_value_entry = tk.Entry(sale_frame, width=15)
    inv_value_entry.place(x=250, y=30)

    tk.Label(sale_frame, text="E. Bill No.", bg="pink").place(x=390, y=30)
    eway_entry = tk.Entry(sale_frame, width=15)
    eway_entry.place(x=470, y=30)

    # Treeview
    invoice_tree = ttk.Treeview(sale_frame, columns=("Sr.", "Inv No.", "Inv Value", "Eway Bill"), show="headings")
    for col in invoice_tree["columns"]:
        invoice_tree.heading(col, text=col)
        invoice_tree.column(col, width=100, anchor="center")
    invoice_tree.place(x=5, y=60, width=645, height=100)

    # Function to Add Data to Table
    def add_to_invoice_tree(event=None):
        inv_no = inv_no_entry.get().strip()
        inv_value = inv_value_entry.get().strip()
        eway = eway_entry.get().strip()

        if not inv_no or not inv_value:
            messagebox.showwarning("Input Error", "Invoice No. and Value are required.",parent=root)
            return

        sr_no = len(invoice_tree.get_children()) + 1
        invoice_tree.insert("", "end", values=(sr_no, inv_no, inv_value, eway))

        # Clear entries after insert
        inv_no_entry.delete(0, tk.END)
        inv_value_entry.delete(0, tk.END)
        eway_entry.delete(0, tk.END)
        inv_no_entry.focus()

    # Function to Delete Selected Row
    def delete_selected_invoice():
        selected_item = invoice_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.",parent=root)
            return
        invoice_tree.delete(selected_item)

        # Reorder Sr. No.
        for index, item in enumerate(invoice_tree.get_children(), start=1):
            values = invoice_tree.item(item, "values")
            invoice_tree.item(item, values=(index, *values[1:]))

    # Bind Enter key to Add
    eway_entry.bind("<Return>", add_to_invoice_tree)

    # Delete Button
    tk.Button(sale_frame, text="Delete", command=delete_selected_invoice).place(x=580, y=25)

#======================== Sale window End ================================
    x = 10
    for b in ["Mail", "SMS", "Lock", "Awb Print", "Sticker"]:
        tk.Checkbutton(right_frame, text=b, bg="lightgrey").place(x=x, y=500)
        x += 100

    tk.Label(right_frame, text="Expt Dlv. Date", bg="lightgrey").place(x=480, y=500)
    tk.Entry(right_frame, width=15).place(x=580, y=500)

    tk.Button(right_frame, text="Save", width=12, bg="#4CAF50", fg="white", command=save_entry).place(x=250, y=550)
    # root.bind("<Return>", lambda event: save_entry())
    tk.Button(right_frame, text="Delete", width=12, bg="#F44336", fg="white", command=delete_entry).place(x=370, y=550)
    tk.Button(right_frame, text="Exit", width=12, bg="#2196F3", fg="white", command=root.quit).place(x=490, y=550)

    root.mainloop() 
    

# =================== Booking Window End====================


# =================== Dispatch Start====================
def build_manifest_gui():
    # Connect to database
    conn = sqlite3.connect("Dispatch.db")
    cursor = conn.cursor()
 
    # Ensure Dispatch table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dispatch (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manf_date TEXT,
            mf_no TEXT,
            fwd TEXT,
            to_dest TEXT,
            vehicle_no TEXT,
            driver TEXT,
            mobile TEXT,
            remark TEXT,
            cd_no TEXT,
            awb_no TEXT UNIQUE,
            pcs TEXT,
            weight TEXT,
            email TEXT,
            FOREIGN KEY (awb_no) REFERENCES Booking(awb_no)
        )
    """)
    
    conn.commit()
    

    win = tk.Toplevel()
    win.title("Manifest - Courier System")
    win.geometry("1200x700")
    win.configure(bg='gainsboro')

    #open in center
    win.update_idletasks()
    window_width = win.winfo_width()
    window_height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    

    # Manifest Save
    def save_manifest():
        try:
            data = (
                manf_date.get(),
                mf_no.get(),
                fwd.get(),
                to_entry.get(),
                vehicle_no.get(),
                driver.get(),
                mobile.get(),
                email.get(),
                remark_text.get("1.0", "end-1c"),
                cd_no.get(),
                awb_no.get(),
                pcs.get(),
                weight.get(),
            )
            cursor.execute("""
                INSERT INTO Dispatch (
                    manf_date, mf_no, fwd, to_dest, vehicle_no, driver, mobile,
                    email, remark, cd_no, awb_no, pcs, weight
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            messagebox.showinfo("Success", "Manifest data saved successfully!",parent=win)
            fetch_manifest_data()
            clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "AWB No already exists or invalid!",parent=win)
        
    win.bind('<Return>', lambda event: save_manifest())

    # Fetch Manifested Data
    def fetch_manifest_data():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT id, awb_no, manf_date, to_dest, fwd, driver, vehicle_no, weight FROM Dispatch")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert('', 'end', values=row)

    # Clear Fields after Save
    def clear_fields():
        manf_date.set_date('')
        mf_no.delete(0, 'end')
        fwd.delete(0, 'end')
        to_entry.delete(0, 'end')
        vehicle_no.delete(0, 'end')
        driver.delete(0, 'end')
        mobile.delete(0, 'end')
        email.delete(0, 'end')
        remark_text.delete('1.0', 'end')
        cd_no.delete(0, 'end')
        awb_no.delete(0, 'end')
        pcs.delete(0, 'end')
        weight.delete(0, 'end')
        email_text.delete('1.0', 'end')

    # Show Entry Details

    def show_entry_details(event):
        selected_item = tree.focus()
        if not selected_item:
            return
        values = tree.item(selected_item, 'values')
        record_id = values[0]

        cursor.execute("SELECT * FROM Dispatch WHERE id=?", (record_id,))
        record = cursor.fetchone()

        if record:
            detail_window = tk.Toplevel(win)
            detail_window.title("Manifest Details")
            detail_window.geometry("600x750")
            detail_window.configure(bg='lightblue')

            fields = [
                "ID", "Manf Date", "Mf No", "Fwd", "To Dest", "Vehicle No", "Driver",
                "Mobile", "Email", "Remark", "CD No", "AWB No", "PCS", "Weight"
            ]

            entry_vars = []

            # Display fields
            for idx, field in enumerate(fields):
                tk.Label(detail_window, text=field + ":", font=('Arial', 10, 'bold'), bg='lightblue').place(x=30, y=30 + idx * 35)
                
                var = tk.StringVar()
                if record[idx] is not None:
                    var.set(str(record[idx]))
                if idx == 0:  # ID field should be read-only
                    entry = ttk.Entry(detail_window, textvariable=var, state='readonly', width=40)
                else:
                    entry = ttk.Entry(detail_window, textvariable=var, width=40)
                entry.place(x=180, y=30 + idx * 35)
                entry_vars.append(var)

            # Functions for Edit, Save, and Delete
            def enable_edit():
                for i, entry in enumerate(detail_window.winfo_children()):
                    if isinstance(entry, ttk.Entry) and i != 0:  # Skip ID field
                        entry.config(state='normal')

            def save_edits():
                updated_data = [var.get() for var in entry_vars[1:]]  # Skip ID field
                updated_data.append(record_id)  # Where condition

                cursor.execute("""
                    UPDATE Dispatch SET 
                        manf_date=?, mf_no=?, fwd=?, to_dest=?, vehicle_no=?, driver=?, 
                        mobile=?, email=?, remark=?, cd_no=?, awb_no=?, pcs=?, weight=?
                    WHERE id=?
                """, updated_data)
                conn.commit()
                messagebox.showinfo("Success", "Manifest details updated successfully!",parent=win)
                fetch_manifest_data()
                detail_window.destroy()

            def delete_entry():
                answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?",parent=win)
                if answer:
                    cursor.execute("DELETE FROM Dispatch WHERE id=?", (record_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "Manifest entry deleted successfully!")
                    fetch_manifest_data()
                    detail_window.destroy()

            def back_to_manifest():
                detail_window.destroy()

            # Buttons
            button_frame = tk.Frame(detail_window, bg='lightblue')
            button_frame.place(x=100, y=650, width=400, height=50)

            ttk.Button(button_frame, text="Edit", command=enable_edit).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Save", command=save_edits).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Delete", command=delete_entry).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Back", command=back_to_manifest).pack(side='left', padx=10)

    # Print mainfest deatils
    def print_manifest():

    # Fetch last inserted manifest details
        cursor.execute("SELECT * FROM Dispatch ORDER BY id DESC LIMIT 1")
        record = cursor.fetchone()

        if not record:
            messagebox.showwarning("No Data", "No manifest found to print!",parent=win)
            return

        # Open a new window showing manifest
        print_win = tk.Toplevel(win)
        print_win.title("Print Manifest")
        print_win.geometry("500x700")
        print_win.configure(bg='aliceblue')

        fields = [
            "ID", "Manf Date", "Mf No", "Fwd", "To Dest", "Vehicle No", "Driver",
            "Mobile", "Email", "Remark", "CD No", "AWB No", "PCS", "Weight"
        ]

        for idx, field in enumerate(fields):
            tk.Label(print_win, text=f"{field}: {record[idx]}", font=('Arial', 10), bg='aliceblue').place(x=30, y=30 + idx * 30)

        def download_pdf():
            # Choose save location
            now = datetime.now()
            filename = f"Manifest_{record[0]}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter

            y = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(180, y, "Manifest Details")
            y -= 40

            c.setFont("Helvetica", 12)
            for idx, field in enumerate(fields):
                line = f"{field}: {record[idx]}"
                c.drawString(50, y, line)
                y -= 25
                if y < 50:
                    c.showPage()
                    y = height - 50

            c.save()
            messagebox.showinfo("Saved", f"PDF saved as {filename}",parent=win)

        ttk.Button(print_win, text="Download PDF", command=download_pdf).place(x=200, y=650)

    # Manifest Entry Frame
    manifest_frame = tk.LabelFrame(win, text="Manifest", bg='#d6d6ff', font=('Arial', 12, 'bold'))
    manifest_frame.place(x=10, y=10, width=950, height=300)

    x_label = 20
    x_entry = 100
    y_gap = 45
    entry_width = 25

    # Entry Widgets
    tk.Label(manifest_frame, text="Manf. Date", bg='#d6d6ff').place(x=x_label, y=20)
    manf_date = DateEntry(manifest_frame, width=22, background='darkblue', foreground='aliceblue', borderwidth=2, date_pattern='dd/mm/yyyy')
    manf_date.place(x=x_entry, y=20)

    tk.Label(manifest_frame, text="M/f No.", bg='#d6d6ff').place(x=300, y=20)
    mf_no = ttk.Entry(manifest_frame, width=entry_width)
    mf_no.place(x=400, y=20)

    tk.Label(manifest_frame, text="Fwd", bg='#d6d6ff').place(x=600, y=20)
    fwd = ttk.Entry(manifest_frame, width=entry_width)
    fwd.place(x=650, y=20)

    tk.Label(manifest_frame, text="To", bg='#d6d6ff').place(x=x_label, y=20 + y_gap)
    to_entry = ttk.Entry(manifest_frame, width=entry_width)
    to_entry.place(x=x_entry, y=20 + y_gap)

    tk.Label(manifest_frame, text="Vehicle No.", bg='#d6d6ff').place(x=300, y=20 + y_gap)
    vehicle_no = ttk.Entry(manifest_frame, width=entry_width)
    vehicle_no.place(x=400, y=20 + y_gap)

    tk.Label(manifest_frame, text="Driver", bg='#d6d6ff').place(x=600, y=20 + y_gap)
    driver = ttk.Entry(manifest_frame, width=entry_width)
    driver.place(x=650, y=20 + y_gap)

    tk.Label(manifest_frame, text="Mob.", bg='#d6d6ff').place(x=x_label, y=20 + y_gap*2)
    mobile = ttk.Entry(manifest_frame, width=entry_width)
    mobile.place(x=x_entry, y=20 + y_gap*2)

    tk.Label(manifest_frame, text="E-mail", bg='#d6d6ff').place(x=300, y=20 + y_gap*2)
    email = ttk.Entry(manifest_frame, width=entry_width)
    email.place(x=400, y=20 + y_gap*2)

    tk.Label(manifest_frame, text="Remark", bg='#d6d6ff').place(x=x_label, y=20 + y_gap*3)
    remark_text = tk.Text(manifest_frame, width=18, height=3)
    remark_text.place(x=x_entry, y=20 + y_gap*3)

    tk.Label(manifest_frame, text="CD No.", bg='#d6d6ff').place(x=300, y=20 + y_gap*3)
    cd_no = ttk.Entry(manifest_frame, width=entry_width)
    cd_no.place(x=400, y=20 + y_gap*3)

    tk.Label(manifest_frame, text="Awb No.", bg='#d6d6ff').place(x=x_label, y=10 + y_gap*5)
    awb_no = ttk.Entry(manifest_frame, width=entry_width)
    awb_no.place(x=x_entry, y=10 + y_gap*5)

    tk.Label(manifest_frame, text="Pcs", bg='#d6d6ff').place(x=300, y=10 + y_gap*5)
    pcs = ttk.Entry(manifest_frame, width=entry_width)
    pcs.place(x=400, y=10 + y_gap*5)

    tk.Label(manifest_frame, text="Weight", bg='#d6d6ff').place(x=600, y=10 + y_gap*5)
    weight = ttk.Entry(manifest_frame, width=entry_width)
    weight.place(x=650, y=10 + y_gap*5)

    # Email Frame
    email_frame = tk.LabelFrame(win, text="Email To Forwarder", bg='#d6d6ff', font=('Arial', 12, 'bold'))
    email_frame.place(x=850, y=10, width=300, height=300)

    email_text = tk.Text(email_frame, width=30, height=17)
    email_text.pack()

    # Manifested Table Frame
    table_frame = tk.LabelFrame(win, text="Manifested", bg='#d6d6ff', font=('Arial', 12, 'bold'))
    table_frame.place(x=10, y=310, width=1140, height=300)

    columns = ("ID", "Awb No", "Date", "Client", "Network", "Driver", "Vehicle No", "Weight")
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    tree.pack(fill='both', expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)

    tree.bind("<Double-1>", show_entry_details)

    # Bottom Buttons
    bottom_frame = tk.Frame(win, bg='gainsboro')
    bottom_frame.place(x=10, y=620, width=1000, height=50)

    auto_mail_var = tk.IntVar()
    tk.Checkbutton(bottom_frame, text="Auto Mail", bg='gainsboro', variable=auto_mail_var).pack(side='left', padx=10)

    ttk.Button(bottom_frame, text='Save', width=20, command=save_manifest).pack(side='left', padx=10)
    ttk.Button(bottom_frame, text='Print', width=20, command=print_manifest).pack(side='left', padx=10)
    ttk.Button(bottom_frame, text='Exit', width=20, command=win.destroy).pack(side='left', padx=10)
    ttk.Button(bottom_frame, text='Update CD No.', width=20).pack(side='right', padx=10)

    fetch_manifest_data()
    

# =================== Dispatch window End====================

# =================== Reciver Window Start ====================
class ReceivingWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Receiving - Courier Management System")
        self.master.geometry("1200x700")
        self.master.configure(bg='aliceblue')

        self.build_ui()
        self.load_manifest_numbers()

        # Ensure Received table exists
        conn = sqlite3.connect("Receiving.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Received (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rec_date TEXT,
                from_loc TEXT,
                fwd TEXT,
                mf_no TEXT,
                email TEXT,
                remark TEXT,
                awb_no TEXT
            )
        """)
        conn.commit()
        conn.close()

    def build_ui(self):
        tk.Label(self.master, text="Receiving", font=('Arial', 16, 'bold'), bg='aliceblue').place(x=550, y=10)

        # === Left Side Image ===
        try:
            img = Image.open("images/left_image.jpg")  # Replace with your image file
            img = img.resize((550, 300))
            self.left_img = ImageTk.PhotoImage(img)
            tk.Label(self.master, image=self.left_img, bg='aliceblue').place(x=500, y=50)
        except Exception as e:
            tk.Label(self.master, text="Image not found", bg='aliceblue').place(x=850, y=50)

        labels = {
            "Recived Date": (30, 50),
            "From": (30, 90),
            "Fwd": (30, 130),
            "Manifest No.": (30, 170),
            "Email": (30, 210),
            "Remark": (30, 250),
            "Awb No.": (30, 340)
        }

        self.entries = {}
        for label, (x, y) in labels.items():
            tk.Label(self.master, text=label, font=('Arial', 10), bg='aliceblue').place(x=x, y=y)
            if label == "Remark":
                self.entries[label] = tk.Text(self.master, height=4, width=35)
                self.entries[label].place(x=130, y=y)
            elif label == "Manifest No.":
                self.manifest_combobox = ttk.Combobox(self.master, width=32, state="readonly")
                self.manifest_combobox.place(x=130, y=y)
                self.manifest_combobox.bind("<<ComboboxSelected>>", self.fetch_manifest_data)
            elif label == "Recived Date":
                self.entries[label] = DateEntry(self.master, width=33, background='darkblue',
                                                foreground='aliceblue', borderwidth=2, date_pattern='yyyy-mm-dd')
                self.entries[label].place(x=130, y=y)
            else:
                entry = tk.Entry(self.master, width=35)
                entry.place(x=130, y=y)
                self.entries[label] = entry

        self.table_frame = tk.Frame(self.master)
        self.table_frame.place(x=30, y=400, width=1130, height=230)

        self.columns = ("Sr.", "Awb No", "Date", "Driver Name", "Driver Mobile", "Vehicle_no", "Qty.", "Weight")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show='headings')

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor='center')
        self.tree.pack(fill='both', expand=True)

        self.auto_mail_var = tk.IntVar()
        tk.Checkbutton(self.master, text="Auto Mail", variable=self.auto_mail_var, bg='aliceblue').place(x=30, y=650)
        tk.Button(self.master, text="Print", width=12, command=self.save_and_print).place(x=130, y=645)
        tk.Button(self.master, text="Exit", width=12, command=self.master.destroy).place(x=230, y=645)
        tk.Button(self.master, text="Save", width=12, command=self.save_and_print).place(x=330, y=645)

    def load_manifest_numbers(self):
        try:
            conn = sqlite3.connect("dispatch.db")
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT mf_no FROM dispatch")
            mf_numbers = [row[0] for row in cur.fetchall()]
            self.manifest_combobox['values'] = mf_numbers
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent= self.master)

    def fetch_manifest_data(self, event=None):
        mf_no = self.manifest_combobox.get().strip()
        try:
            conn = sqlite3.connect("dispatch.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT ID, awb_no, manf_date, driver, mobile, vehicle_no, pcs, weight 
                FROM dispatch WHERE mf_no=?
            """, (mf_no,))
            rows = cur.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', 'end', values=row)

            if rows:
                self.entries["From"].delete(0, tk.END)
                self.entries["Fwd"].delete(0, tk.END)
                self.entries["Awb No."].delete(0, tk.END)

                self.entries["From"].insert(0, rows[0][3])  # driver
                self.entries["Fwd"].insert(0, rows[0][4])   # mobile
                self.entries["Awb No."].insert(0, rows[0][1])  # awb_no

        except Exception as e:
            messagebox.showerror("Database Error", str(e),parent= self.master)

    def save_and_print(self):
        try:
            rec_date = self.entries["Recived Date"].get()
            from_loc = self.entries["From"].get()
            fwd = self.entries["Fwd"].get()
            mf_no = self.manifest_combobox.get().strip()
            email = self.entries["Email"].get()
            remark = self.entries["Remark"].get("1.0", tk.END).strip()
            awb_no = self.entries["Awb No."].get()

            data = (rec_date, from_loc, fwd, mf_no, email, remark, awb_no)

            conn = sqlite3.connect("Receiving.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Received (rec_date, from_loc, fwd, mf_no, email, remark, awb_no)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Receiving data saved.",parent= self.master)
            self.generate_pdf(data)

        except Exception as e:
            messagebox.showerror("Error", str(e),parent= self.master)

    def generate_pdf(self, data):
        try:
            conn = sqlite3.connect("Receiving.db")
            cur = conn.cursor()
            awb_no = self.entries["Awb No."].get()
            cur.execute("SELECT * FROM Received WHERE awb_no = ?", (awb_no,))
            row = cur.fetchone()
            conn.close()

            if not row:
                messagebox.showwarning("Not Found", "No receiving record found to print.",parent= self.master)
                return

            pdf_file = f"Receiving_{awb_no}.pdf"
            c = canvas.Canvas(pdf_file)
            c.setFont("Helvetica", 12)
            c.drawString(100, 800, "Courier Receiving Receipt")
            c.drawString(100, 770, f"Received Date: {row[1]}")
            c.drawString(100, 750, f"From: {row[2]}")
            c.drawString(100, 730, f"Fwd: {row[3]}")
            c.drawString(100, 710, f"Manifest No: {row[4]}")
            c.drawString(100, 690, f"Email: {row[5]}")
            c.drawString(100, 670, f"Remark: {row[6]}")
            c.drawString(100, 650, f"AWB No: {row[7]}")
            c.drawString(100, 630, f"Printed On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.save()

            messagebox.showinfo("PDF Created", f"PDF saved as {pdf_file}",parent= self.master)
        except Exception as e:
            messagebox.showerror("PDF Error", str(e),parent= self.master)

# =================== Reciver Window End ====================

main_dashboard("Avneesh")
