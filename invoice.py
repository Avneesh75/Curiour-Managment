import tkinter as tk
from tkinter import ttk

def generate_invoice():
    print("Generating invoice...")

def delete_invoice():
    print("Deleting invoice...")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Invoice Generation")
root.geometry("850x650")
root.configure(bg="#cce6ff")

# Tabs
notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
notebook.add(tab1, text='Date Wise Invoice')
notebook.add(tab2, text='Awb No. Wise Invoice')
notebook.add(tab3, text='Delete Invoice')
notebook.pack(expand=1, fill='both')

# ----------- Date Wise Invoice Tab -----------
frame1 = ttk.LabelFrame(tab1, text="Invoice Info:")
frame1.pack(padx=10, pady=10, fill="x")

ttk.Label(frame1, text="Company").grid(row=0, column=0, padx=5, pady=5, sticky="w")
company_combo = ttk.Combobox(frame1, values=["SKYLARK EXPRESS (DELHI) PRIVATE LIMITED"], state='readonly')
company_combo.current(0)
company_combo.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

ttk.Label(frame1, text="Branch").grid(row=1, column=0, padx=5, pady=5, sticky="w")
branch_entry = ttk.Entry(frame1)
branch_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame1, text="Network").grid(row=1, column=2, padx=5, pady=5, sticky="w")
network_entry = ttk.Entry(frame1)
network_entry.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(frame1, text="From").grid(row=2, column=0, padx=5, pady=5, sticky="w")
from_entry = ttk.Entry(frame1)
from_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame1, text="To").grid(row=2, column=2, padx=5, pady=5, sticky="w")
to_entry = ttk.Entry(frame1)
to_entry.grid(row=2, column=3, padx=5, pady=5)

ttk.Label(frame1, text="Type").grid(row=3, column=0, padx=5, pady=5, sticky="w")
type_combo = ttk.Combobox(frame1, values=["Credit", "Cash"], state='readonly')
type_combo.set("Credit")
type_combo.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame1, text="Date").grid(row=3, column=2, padx=5, pady=5, sticky="w")
date_entry = ttk.Entry(frame1)
date_entry.grid(row=3, column=3, padx=5, pady=5)

ttk.Label(frame1, text="Client").grid(row=4, column=0, padx=5, pady=5, sticky="w")
client_entry = ttk.Entry(frame1)
client_entry.grid(row=4, column=1, padx=5, pady=5)

status_label = tk.Label(frame1, text="F1=Unbilled, F2=All, F3=Billed", fg="blue")
status_label.grid(row=4, column=3, padx=5, pady=5, sticky="e")

ttk.Label(frame1, text="Client Type").grid(row=5, column=0, padx=5, pady=5, sticky="w")
client_type_combo = ttk.Combobox(frame1, values=["Other", "Corporate", "Retail"], state='readonly')
client_type_combo.set("Other")
client_type_combo.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(frame1, text="Invoice No.").grid(row=6, column=0, padx=5, pady=5, sticky="w")
invoice_entry = ttk.Entry(frame1)
invoice_entry.grid(row=6, column=1, padx=5, pady=5)

invoice_type_combo = ttk.Combobox(frame1, values=["Both", "Only New", "Only Existing"], state='readonly')
invoice_type_combo.set("Both")
invoice_type_combo.grid(row=6, column=3, padx=5, pady=5)

option_var = tk.StringVar(value="Addition")
ttk.Radiobutton(frame1, text="Addition", variable=option_var, value="Addition").grid(row=7, column=0, padx=5, pady=5, sticky="w")
ttk.Radiobutton(frame1, text="Discount", variable=option_var, value="Discount").grid(row=7, column=1, padx=5, pady=5, sticky="w")

ttk.Label(frame1, text="%age").grid(row=8, column=0, padx=5, pady=5, sticky="w")
percent_entry = ttk.Entry(frame1)
percent_entry.grid(row=8, column=1, padx=5, pady=5)

ttk.Label(frame1, text="Flat Amt").grid(row=8, column=2, padx=5, pady=5, sticky="w")
flat_amt_entry = ttk.Entry(frame1)
flat_amt_entry.grid(row=8, column=3, padx=5, pady=5)

notes_text = tk.Text(frame1, height=4, width=60)
notes_text.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

tk.Button(frame1, text="Generate", width=12, command=generate_invoice, bg="lightgreen").grid(row=10, column=2, padx=10, pady=10, sticky="e")
tk.Button(frame1, text="Exit", width=10, command=exit_app, bg="tomato").grid(row=10, column=3, padx=10, pady=10, sticky="e")


# ----------- AWB No. Wise Invoice Tab -----------
frame2 = ttk.LabelFrame(tab2, text="AWB Invoice Info:")
frame2.pack(padx=10, pady=10, fill="x")

ttk.Label(frame2, text="AWB No.").grid(row=0, column=0, padx=5, pady=10, sticky="w")
awb_no_entry = ttk.Entry(frame2)
awb_no_entry.grid(row=0, column=1, padx=5, pady=10)

ttk.Label(frame2, text="Client").grid(row=1, column=0, padx=5, pady=10, sticky="w")
awb_client_entry = ttk.Entry(frame2)
awb_client_entry.grid(row=1, column=1, padx=5, pady=10)

tk.Button(frame2, text="Generate", width=12, command=generate_invoice, bg="lightgreen").grid(row=2, column=0, padx=10, pady=15)
tk.Button(frame2, text="Exit", width=10, command=exit_app, bg="tomato").grid(row=2, column=1, padx=10, pady=15)

# ----------- Delete Invoice Tab -----------
frame3 = ttk.LabelFrame(tab3, text="Delete Invoice Info:")
frame3.pack(padx=10, pady=10, fill="x")

ttk.Label(frame3, text="Invoice No.").grid(row=0, column=0, padx=5, pady=10, sticky="w")
del_invoice_entry = ttk.Entry(frame3)
del_invoice_entry.grid(row=0, column=1, padx=5, pady=10)

ttk.Label(frame3, text="Client").grid(row=1, column=0, padx=5, pady=10, sticky="w")
del_client_entry = ttk.Entry(frame3)
del_client_entry.grid(row=1, column=1, padx=5, pady=10)

tk.Button(frame3, text="Delete", width=12, command=delete_invoice, bg="orange").grid(row=2, column=0, padx=10, pady=15)
tk.Button(frame3, text="Exit", width=10, command=exit_app, bg="tomato").grid(row=2, column=1, padx=10, pady=15)

# root.mainloop()
