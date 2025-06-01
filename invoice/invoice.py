import tkinter as tk
from tkinter import ttk
from docxtpl import DocxTemplate


window=tk.Tk()
window.title("SAS Software Invoice Builder")
window.geometry("1000x600")

productList = [
    ["Laptop", 1, 30000, 30000],
    ["Phone", 2, 30000, 60000]
]

def generateInvoice():
    try:
        doc = DocxTemplate("SAS.docx")  # Make sure SAS.docx exists and is properly formatted
        total_amount = sum(item[3] for item in productList)  # Auto-calculate total

        context = {
            "name": "Sayam Kumar",
            "address": "Delhi, India",
            "phone": "9953406578",
            "itemList": productList,
            "total": total_amount
        }

        doc.render(context)
        doc.save("new_invoice.docx")
        print("✅ Invoice generated: new_invoice.docx")
    
    except Exception as e:
        print(f"❌ Error generating invoice: {e}")

# Call the function
generateInvoice()

window.mainloop()