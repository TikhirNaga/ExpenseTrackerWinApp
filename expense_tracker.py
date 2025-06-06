import sqlite3
import os
from tkinter import *
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ----- Initialize Database -----
conn = sqlite3.connect("expenses.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
''')
conn.commit()

# ----- Functions -----
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not (date and category and amount):
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return

    c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
              (date, category, amount, description))
    conn.commit()
    load_expenses()
    clear_fields()
    update_total()

def load_expenses():
    for row in expense_tree.get_children():
        expense_tree.delete(row)

    c.execute("SELECT id, date, category, amount, description FROM expenses")
    rows = c.fetchall()
    for i, row in enumerate(rows, start=1):
        expense_tree.insert('', END, values=(i, *row[1:]))

    update_total()

def clear_fields():
    date_entry.delete(0, END)
    category_entry.delete(0, END)
    amount_entry.delete(0, END)
    description_entry.delete(0, END)

def delete_selected():
    selected = expense_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return
    for sel in selected:
        item = expense_tree.item(sel)
        values = item['values']
        date, category, amount, description = values[1:]
        c.execute("DELETE FROM expenses WHERE date=? AND category=? AND amount=? AND description=?", (date, category, amount, description))
    conn.commit()
    load_expenses()

def update_total():
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]
    total = total if total else 0.0
    total_label.config(text=f"Total: ₹{total:.2f}")

def show_total_message():
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]
    total = total if total else 0.0
    messagebox.showinfo("Total Expenses", f"Your total expenses are: ₹{total:.2f}")

def download_pdf():
    if not expense_tree.get_children():
        messagebox.showinfo("No Data", "No expenses to export.")
        return

    pdf_path = os.path.join(os.getcwd(), "expenses_report.pdf")
    c_pdf = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c_pdf.setFont("Helvetica-Bold", 16)
    c_pdf.drawString(200, height - 50, "Expense Report")

    c_pdf.setFont("Helvetica-Bold", 12)
    c_pdf.drawString(50, height - 80, "Date")
    c_pdf.drawString(150, height - 80, "Category")
    c_pdf.drawString(300, height - 80, "Amount")
    c_pdf.drawString(400, height - 80, "Description")

    y = height - 100
    c_pdf.setFont("Helvetica", 12)
    for item in expense_tree.get_children():
        _, date, category, amount, description = expense_tree.item(item, "values")

        c_pdf.drawString(50, y, str(date))
        c_pdf.drawString(150, y, str(category))
        c_pdf.drawString(300, y, str(amount))
        c_pdf.drawString(400, y, str(description))
        y -= 20
        if y < 70:
            c_pdf.showPage()
            y = height - 50

    # Add total at the end of PDF
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]
    total = total if total else 0.0

    if y < 100:
        c_pdf.showPage()
        y = height - 50

    c_pdf.setFont("Helvetica-Bold", 12)
    c_pdf.drawString(50, y - 20, f"Total Expenses: ₹{total:.2f}")

    c_pdf.save()
    messagebox.showinfo("Success", f"PDF saved to:\n{pdf_path}")

# ----- GUI Setup -----
root = Tk()
root.title("Budget Expense Tracker")
root.geometry("800x600")
root.configure(bg="#f2f2f2")

# Labels and Entries
Label(root, text="Date (DD-MM-YYYY):", bg="#f2f2f2", font=("Arial", 12)).grid(row=0, column=0, sticky=W, padx=10, pady=5)
date_entry = Entry(root, width=30)
date_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Category:", bg="#f2f2f2", font=("Arial", 12)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
category_entry = Entry(root, width=30)
category_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Amount:", bg="#f2f2f2", font=("Arial", 12)).grid(row=2, column=0, sticky=W, padx=10, pady=5)
amount_entry = Entry(root, width=30)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Description:", bg="#f2f2f2", font=("Arial", 12)).grid(row=3, column=0, sticky=W, padx=10, pady=5)
description_entry = Entry(root, width=30)
description_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
button_style = {"width": 20, "font": ("Arial", 11), "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049"}
Button(root, text="➕ Add Expense", command=add_expense, **button_style).grid(row=4, column=1, pady=10)
Button(root, text="🗑️ Delete Selected", command=delete_selected, **button_style).grid(row=5, column=1, pady=5)
Button(root, text="📄 Download PDF", command=download_pdf, **button_style).grid(row=6, column=1, pady=5)
Button(root, text="💰 Show Total", command=show_total_message, **button_style).grid(row=7, column=1, pady=5)

# Treeview (Table)
columns = ("S.No", "Date", "Category", "Amount", "Description")
expense_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=120)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

expense_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=20)

# Total Label
total_label = Label(root, text="Total: ₹0.00", bg="#f2f2f2", font=("Arial", 14, "bold"))
total_label.grid(row=9, column=0, columnspan=2, pady=10)

load_expenses()
root.mainloop()
