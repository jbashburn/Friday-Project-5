import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    birthday TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    contact_method TEXT
)
""")
conn.commit()

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Customer Information Manager")
root.geometry("800x600")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#dbe9f4")
style.configure("Treeview", font=("Arial", 10), rowheight=25)

# ---------- Input Frame ----------
input_frame = tk.Frame(root, bg="#f0f4f7")
input_frame.pack(pady=10)

fields = {
    "First Name": tk.StringVar(),
    "Last Name": tk.StringVar(),
    "Birthday (MM DD YYYY)": tk.StringVar(),
    "Email": tk.StringVar(),
    "Phone Number": tk.StringVar(),
    "Address": tk.StringVar(),
    "Preferred Contact Method": tk.StringVar()
}

row = 0
for label, var in fields.items():
    tk.Label(input_frame, text=label, bg="#f0f4f7", font=("Arial", 10)).grid(row=row, column=0, sticky="w", padx=10, pady=5)
    if label == "Preferred Contact Method":
        dropdown = ttk.Combobox(input_frame, textvariable=var, values=["Email", "Phone", "Mail"], state="readonly")
        dropdown.grid(row=row, column=1, padx=10, pady=5)
    else:
        tk.Entry(input_frame, textvariable=var, width=30).grid(row=row, column=1, padx=10, pady=5)
    row += 1

# ---------- Submit Button ----------
def submit():
    data = [var.get() for var in fields.values()]
    if all(data):
        cursor.execute("INSERT INTO customers (first_name, last_name, birthday, email, phone, address, contact_method) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        load_data()
        for var in fields.values():
            var.set("")
    else:
        messagebox.showwarning("Missing Info", "Please fill out all fields.")

tk.Button(root, text="Submit", command=submit, bg="#4caf50", fg="white", font=("Helvetica", 10, "bold")).pack(pady=10)

# ---------- Table Frame ----------
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("id", "first_name", "last_name", "birthday", "email", "phone", "address", "contact_method")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col.replace("_", " ").title(), command=lambda c=col: sort_column(c, False))
    if col == "id":
        tree.column(col, width=50, anchor="center")  # Smaller width for ID
    else:
        tree.column(col, width=100, anchor="w")

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def sort_column(col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children()]
    data.sort(reverse=reverse)
    for index, (val, k) in enumerate(data):
        tree.move(k, "", index)
    tree.heading(col, command=lambda: sort_column(col, not reverse))

# ---------- Edit on Double Click ----------
def on_double_click(event):
    item = tree.selection()[0]
    values = tree.item(item, "values")
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Entry")
    edit_window.geometry("400x400")
    edit_vars = [tk.StringVar(value=v) for v in values[1:]]

    for i, label in enumerate(columns[1:]):
        tk.Label(edit_window, text=label.replace("_", " ").title()).pack(pady=5)
        if label == "contact_method":
            ttk.Combobox(edit_window, textvariable=edit_vars[i], values=["Email", "Phone", "Mail"], state="readonly").pack()
        else:
            tk.Entry(edit_window, textvariable=edit_vars[i]).pack()

    def save_changes():
        updated = [v.get() for v in edit_vars]
        cursor.execute("""
            UPDATE customers SET first_name=?, last_name=?, birthday=?, email=?, phone=?, address=?, contact_method=?
            WHERE id=?
        """, (*updated, values[0]))
        conn.commit()
        load_data()
        edit_window.destroy()

    tk.Button(edit_window, text="Save", command=save_changes, bg="#2196f3", fg="white").pack(pady=20)

tree.bind("<Double-1>", on_double_click)

load_data()
root.mainloop()