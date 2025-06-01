
import tkinter as tk
from tkinter import ttk, messagebox, Menu
from datetime import datetime
from PIL import Image, ImageTk
import sqlite3
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# =================== Checklist Window Start ====================
def create_checklist_gui(root):
    def fetch_by_awb():
        awb_no = awb_entry.get()
        for i in tree.get_children():
            tree.delete(i)
        try:
            conn = sqlite3.connect("Booking.db")
            cursor = conn.cursor()
            query = "SELECT awb_no, date, client, network, fwd_no, mode, origin, destination, weight, freight, fuel, gst, net, pcs, fov FROM Booking WHERE awb_no = ?"
            cursor.execute(query, (awb_no,))
            rows = cursor.fetchall()
            conn.close()
            if not rows:
                messagebox.showinfo("No Results", "No records found for AWB No: " + awb_no)
                return
            for idx, row in enumerate(rows, 1):
                tree.insert('', 'end', values=(idx, row[1], row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    win = tk.Toplevel()
    win.title("Checklist - Courier Management System")
    win.geometry("1400x700")
    win.configure(bg='lavender')

    tk.Label(win, text="Welcome to Administrator Account", font=('Arial', 16, 'bold'), bg='lavender').pack(pady=10)

    filter_frame = tk.LabelFrame(win, bg='white', text='Check List Filters', font=('Arial', 10, 'bold'))
    filter_frame.pack(fill='x', padx=10, pady=5)

    labels = [
        ('Branch', 0), ('Client', 1), ('Origin', 2), ('Dest.', 3),
        ('Forwarder', 4), ('Network', 5), ('Service', 6),
        ('Date From', 7), ('Date To', 8), ('Rate Range', 9), ('Weight Range', 10),
        ('User', 11), ('Consignment Type', 12), ('Status', 13), ('Pay Mode', 14), 
        ('Location', 15), ('M/f #', 16)
    ]

    for text, col in labels:
        r, c = divmod(col, 4)
        tk.Label(filter_frame, text=text, bg='white').grid(row=r, column=c*2, sticky='e', padx=5, pady=5)
        ttk.Entry(filter_frame, width=20).grid(row=r, column=c*2+1, padx=5, pady=5)

    awb_check = tk.IntVar()
    weight_check = tk.IntVar()
    spot_rate_check = tk.IntVar()

    tk.Checkbutton(filter_frame, text="Awb Range", variable=awb_check, bg='white').grid(row=5, column=0, padx=5, pady=5, sticky='w')
    tk.Checkbutton(filter_frame, text="Weight Range", variable=weight_check, bg='white').grid(row=5, column=1, padx=5, pady=5, sticky='w')
    tk.Checkbutton(filter_frame, text="Spot Rate", variable=spot_rate_check, bg='white').grid(row=5, column=2, padx=5, pady=5, sticky='w')

    # AWB Entry Field
    awb_label = tk.Label(filter_frame, text="AWB No:", bg='white')
    awb_label.grid(row=6, column=0, padx=5, pady=5, sticky='e')
    awb_entry = ttk.Entry(filter_frame, width=20)
    awb_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

    summary_frame = tk.Frame(win, bg='lavender')
    summary_frame.pack(fill='x', padx=10)
    for label in ["Total No.Of Ships: ", "Amount: ", "Total Net Amount: "]:
        tk.Label(summary_frame, text=label, bg='lavender', font=('Arial', 10)).pack(side='left', padx=20)

    btn_frame = tk.Frame(win, bg='lavender')
    btn_frame.pack(fill='x', padx=10, pady=10)
    ttk.Button(btn_frame, text="Show", width=20, command=fetch_by_awb).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Excel", width=20).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Exit", width=20, command=win.destroy).pack(side='left', padx=5)

    table_frame = tk.Frame(win)
    table_frame.pack(fill='both', expand=True, padx=10, pady=5)

    columns = ('Sn', 'Date', 'Awb No', 'Client', 'Network', 'Fwd No', 'Mode', 'Origin', 'Destination',
               'Weight', 'Freight', 'Fuel', 'GST', 'Net', 'Pcs', 'FOV/F')

    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    tree.pack(fill='both', expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar.set)
    scrollbar.pack(side='bottom', fill='x')

