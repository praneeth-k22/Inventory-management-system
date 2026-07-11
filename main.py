import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database
conn = sqlite3.connect("inventory_v2.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS inventory")

cursor.execute("""
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    quantity INTEGER
)
""")

# Functions
def add_item():
    name = name_entry.get()
    category = category_entry.get()
    qty = qty_entry.get()

    if name and category and qty:
        cursor.execute(
            "INSERT INTO inventory (name, category, quantity) VALUES (?, ?, ?)",
            (name, category, qty)
        )
        
def view_items():
    listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    low_stock_count = 0

    for row in rows:
        status = ""

        if row[2] < 5:
            status = " ⚠ LOW STOCK"
            low_stock_count += 1

        listbox.insert(
            tk.END,
            f"ID:{row[0]} | {row[1]} | Qty:{row[2]}{status}"
        )

    total_items_label.config(
        text=f"Total Items: {len(rows)}"
    )

    low_stock_label.config(
        text=f"Low Stock Items: {low_stock_count}"
    )

def update_item():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected)

        item_id = item.split("|")[0].replace("ID:", "").strip()

        new_qty = qty_entry.get()

        if new_qty:
            cursor.execute(
                "UPDATE inventory SET quantity=? WHERE id=?",
                (new_qty, item_id)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Quantity Updated"
            )

            view_items()

def update_item():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an item first"
        )
        return

    item = listbox.get(selected)

    item_id = item.split("|")[0].replace("ID:", "").strip()

    new_qty = qty_entry.get()

    if not new_qty:
        messagebox.showwarning(
            "Warning",
            "Enter a new quantity"
        )
        return

    cursor.execute(
        "UPDATE inventory SET quantity=? WHERE id=?",
        (new_qty, item_id)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Quantity Updated"
    )

    view_items()

def delete_item():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected)
        item_id = item.split("|")[0].replace("ID:", "").strip()

        cursor.execute(
            "DELETE FROM inventory WHERE id=?",
            (item_id,)
        )
        conn.commit()
        view_items()

def search_item():
    keyword = search_entry.get()

    listbox.delete(0, tk.END)

    cursor.execute(
        "SELECT * FROM inventory WHERE name LIKE ?",
        ('%' + keyword + '%',)
    )

    rows = cursor.fetchall()

    for row in rows:
        status = ""

        if row[2] < 5:
            status = " ⚠ LOW STOCK"

        listbox.insert(
            tk.END,
            f"ID:{row[0]} | {row[1]} | Qty:{row[2]}{status}"
        )

# GUI
root = tk.Tk()
root.title("Smart Inventory Management System")
root.geometry("600x500")

tk.Label(root, text="Item Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()


tk.Label(root, text="Quantity").pack()
qty_entry = tk.Entry(root)
qty_entry.pack()

tk.Label(root, text="Search Item").pack()
search_entry = tk.Entry(root)
search_entry.pack()

total_items_label = tk.Label(root, text="Total Items: 0", font=("Arial", 12, "bold"))
total_items_label.pack()

low_stock_label = tk.Label(root, text="Low Stock Items: 0", font=("Arial", 12, "bold"))
low_stock_label.pack()

tk.Button(root, text="Add Item", command=add_item).pack(pady=5)

tk.Button(root, text="View Inventory", command=view_items).pack(pady=5)

tk.Button(root, text="Search", command=search_item).pack(pady=5)

tk.Button(root, text="Delete Selected", command=delete_item).pack(pady=5)

tk.Button(root, text="Update Quantity", command=update_item).pack(pady=5)

listbox = tk.Listbox(root, width=80)
listbox.pack(pady=10)

view_items()

root.mainloop()