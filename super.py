import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import datetime

# ----------------- Database Setup -----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="subeko223",  # Change to your MySQL password
        database="supermarket"
    )

def setup_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="subeko223"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS supermarket")
    conn.commit()
    conn.close()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL,
            stock INT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id VARCHAR(20),
            customer_name VARCHAR(100),
            customer_phone VARCHAR(20),
            invoice_text TEXT,
            total FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

setup_db()

# ----------------- Main Application -----------------
class SupermarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Product Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.product_id = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_stock = tk.StringVar()
        self.search_var = tk.StringVar()
        self.bill_items = []
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        

        # ----------------- GUI Layout -----------------
        self.create_product_frame()
        self.create_treeview_frame()
        self.create_billing_frame()
        self.load_products()

    # ----------------- Product Management Frame -----------------
    def create_product_frame(self):
        prod_frame = tk.LabelFrame(self.root, text="Product Management", bg="#e8eaf6", font=("Arial", 12, "bold"))
        prod_frame.place(x=10, y=10, width=400, height=320)

        tk.Label(prod_frame, text="Product Name:", bg="#e8eaf6", font=("Arial", 11)).place(x=10, y=20)
        tk.Entry(prod_frame, textvariable=self.product_name, font=("Arial", 11)).place(x=130, y=20, width=240)

        tk.Label(prod_frame, text="Price:", bg="#e8eaf6", font=("Arial", 11)).place(x=10, y=60)
        tk.Entry(prod_frame, textvariable=self.product_price, font=("Arial", 11)).place(x=130, y=60, width=240)

        tk.Label(prod_frame, text="Stock:", bg="#e8eaf6", font=("Arial", 11)).place(x=10, y=100)
        tk.Entry(prod_frame, textvariable=self.product_stock, font=("Arial", 11)).place(x=130, y=100, width=240)

        tk.Button(prod_frame, text="Add Product", bg="#43a047", fg="white", font=("Arial", 11, "bold"),
                  command=self.add_product).place(x=10, y=150, width=120)
        tk.Button(prod_frame, text="Update Product", bg="#1e88e5", fg="white", font=("Arial", 11, "bold"),
                  command=self.update_product).place(x=140, y=150, width=120)
        tk.Button(prod_frame, text="Delete Product", bg="#e53935", fg="white", font=("Arial", 11, "bold"),
                  command=self.delete_product).place(x=270, y=150, width=120)

        tk.Label(prod_frame, text="Search Product:", bg="#e8eaf6", font=("Arial", 11)).place(x=10, y=200)
        tk.Entry(prod_frame, textvariable=self.search_var, font=("Arial", 11)).place(x=130, y=200, width=140)
        tk.Button(prod_frame, text="Search", bg="#3949ab", fg="white", font=("Arial", 11, "bold"),
                  command=self.search_product).place(x=280, y=195, width=90)
        tk.Button(prod_frame, text="Show All", bg="#6d4c41", fg="white", font=("Arial", 11, "bold"),
                  command=self.load_products).place(x=10, y=250, width=360)

    # ----------------- Product Treeview Frame -----------------
    def create_treeview_frame(self):
        tree_frame = tk.LabelFrame(self.root, text="Product List", bg="#e3f2fd", font=("Arial", 12, "bold"))
        tree_frame.place(x=420, y=10, width=660, height=320)

        columns = ("ID", "Name", "Price", "Stock")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add to bill button
        tk.Button(tree_frame, text="Add to Bill", bg="#00897b", fg="white", font=("Arial", 11, "bold"),
                  command=self.add_to_bill).pack(side=tk.BOTTOM, fill=tk.X)

    # ----------------- Billing/Invoice Frame -----------------
    # Add this to your setup_db() function to create the invoices table:

    def create_billing_frame(self):
        bill_frame = tk.LabelFrame(self.root, text="Billing & Invoice", bg="#fffde7", font=("Arial", 12, "bold"))
        bill_frame.place(x=10, y=340, width=1070, height=340)

        # Customer details
        # tk.Label(bill_frame, text="Customer ID:", bg="#fffde7", font=("Arial", 11)).place(x=10, y=10)
        # tk.Entry(bill_frame, textvariable=self.customer_id, font=("Arial", 11)).place(x=110, y=10, width=120)
        tk.Label(bill_frame, text="Name:", bg="#fffde7", font=("Arial", 11)).place(x=10, y=10)
        tk.Entry(bill_frame, textvariable=self.customer_name, font=("Arial", 11)).place(x=110, y=10, width=150)
        tk.Label(bill_frame, text="Phone:", bg="#fffde7", font=("Arial", 11)).place(x=250, y=10)
        tk.Entry(bill_frame, textvariable=self.customer_phone, font=("Arial", 11)).place(x=310, y=10, width=150)

        # Bill area (left)
        self.bill_text = tk.Text(bill_frame, font=("Consolas", 11), width=50, height=16, state="disabled", bg="#f5f5f5")
        self.bill_text.place(x=10, y=50)

        # Bill items Treeview (right)
        bill_tree_frame = tk.Frame(bill_frame, bg="#fffde7")
        bill_tree_frame.place(x=430, y=50, width=620, height=220)

        bill_columns = ("Name", "Price", "Qty", "Total")
        self.bill_tree = ttk.Treeview(bill_tree_frame, columns=bill_columns, show="headings", height=9)
        for col in bill_columns:
            self.bill_tree.heading(col, text=col)
            self.bill_tree.column(col, anchor="center", width=120)
        self.bill_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bill_scroll = ttk.Scrollbar(bill_tree_frame, orient="vertical", command=self.bill_tree.yview)
        self.bill_tree.configure(yscroll=bill_scroll.set)
        bill_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bill buttons (below bill tree)
        btn_y = 280
        tk.Button(bill_frame, text="Remove Selected", bg="#e53935", fg="white", font=("Arial", 11, "bold"),
                command=self.remove_from_bill).place(x=430, y=btn_y, width=150)
        tk.Button(bill_frame, text="Generate Invoice", bg="#43a047", fg="white", font=("Arial", 11, "bold"),
                command=self.generate_invoice).place(x=600, y=btn_y, width=150)
        tk.Button(bill_frame, text="Clear Bill", bg="#1e88e5", fg="white", font=("Arial", 11, "bold"),
                command=self.clear_bill).place(x=770, y=btn_y, width=130)
        tk.Button(bill_frame, text="Print Invoice", bg="#6d4c41", fg="white", font=("Arial", 11, "bold"),
                command=self.print_invoice).place(x=920, y=btn_y, width=120)

    # Add this method to save invoices and print:
    def print_invoice(self):
        import tempfile, os, platform
        invoice = self.bill_text.get("1.0", tk.END)
        if not invoice.strip():
            messagebox.showerror("Print Error", "No invoice to print.")
            return
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp:
            temp.write(invoice)
            temp_path = temp.name
        if platform.system() == "Windows":
            os.startfile(temp_path, "print")
        else:
            os.system(f"lp {temp_path}")
        messagebox.showinfo("Print", "Invoice sent to printer.")

    # ----------------- Product CRUD Functions -----------------
    def add_product(self):
        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        stock = self.product_stock.get().strip()
        if not name or not price or not stock:
            messagebox.showerror("Input Error", "All product fields are required.")
            return
        try:
            price = int(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number and Stock must be an integer.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
        conn.commit()
        conn.close()
        self.load_products()
        self.clear_product_fields()
        messagebox.showinfo("Success", "Product added successfully.")

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a product to update.")
            return
        if not messagebox.askyesno("Confirm Update", "Are you sure you want to update this product?"):
            return
    
        prod_id = self.tree.item(selected[0])["values"][0]
        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        stock = self.product_stock.get().strip()
        if not name or not price or not stock:
            messagebox.showerror("Input Error", "All product fields are required.")
            return
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number and Stock must be an integer.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s", (name, price, stock, prod_id))
        conn.commit()
        conn.close()
        self.load_products()
        self.clear_product_fields()
        messagebox.showinfo("Success", "Product updated successfully.")

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a product to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            return
    
        prod_id = self.tree.item(selected[0])["values"][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (prod_id,))
        conn.commit()
        conn.close()
        self.load_products()
        self.clear_product_fields()
        messagebox.showinfo("Success", "Product deleted successfully.")

    def clear_product_fields(self):
        self.product_id.set("")
        self.product_name.set("")
        self.product_price.set("")
        self.product_stock.set("")

    # ----------------- Product Loading and Search -----------------
    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def search_product(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showerror("Input Error", "Enter a product name to search.")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE %s", (f"%{query}%",))
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        self.product_id.set(values[0])
        self.product_name.set(values[1])
        self.product_price.set(values[2])
        self.product_stock.set(values[3])

    # ----------------- Billing Functions -----------------
    def add_to_bill(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select a product to add to bill.")
            return
        values = self.tree.item(selected[0])["values"]
        name, price, stock = values[1], float(values[2]), float(values[3])
        qty = simpledialog.askinteger("Quantity", f"Enter quantity for {name} (Available: {stock}):", minvalue=1, maxvalue=stock)
        if qty is None:
            return
        if qty > stock:
            messagebox.showerror("Stock Error", "Not enough stock available.")
            return
        # Reduce stock in DB
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET stock=stock-%s WHERE id=%s", (qty, values[0]))
        conn.commit()
        conn.close()
        # Add to bill
        total = price * qty
        self.bill_items.append({"name": name, "price": price, "qty": qty, "total": total})
        self.bill_tree.insert("", tk.END, values=(name, price, qty, total))
        self.load_products()

    def remove_from_bill(self):
        selected = self.bill_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Select an item to remove from bill.")
            return
        item = self.bill_tree.item(selected[0])["values"]
        name, qty = item[0], int(item[2])
        # Restore stock in DB
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET stock=stock+%s WHERE name=%s", (qty, name))
        conn.commit()
        conn.close()
        # Remove from bill
        for i, bill_item in enumerate(self.bill_items):
            if bill_item["name"] == name and bill_item["qty"] == qty:
                del self.bill_items[i]
                break
        self.bill_tree.delete(selected[0])
        self.load_products()

    def clear_bill(self):
        # Restore all stock
        for item in self.bill_items:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET stock=stock+%s WHERE name=%s", (item["qty"], item["name"]))
            conn.commit()
            conn.close()
        self.bill_items.clear()
        for row in self.bill_tree.get_children():
            self.bill_tree.delete(row)
        self.bill_text.config(state="normal")
        self.bill_text.delete("1.0", tk.END)
        self.bill_text.config(state="disabled")
        self.load_products()

    def generate_invoice(self):
        if not self.bill_items:
            messagebox.showerror("Invoice Error", "No items in the bill.")
            return
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        name = self.customer_name.get().strip()
        phone = self.customer_phone.get().strip()
        if not name or not phone:
            messagebox.showerror("Input Error", "Enter all customer details.")
            return

        # Save customer and get auto-generated ID
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        customer_id = cursor.lastrowid  # Get the auto-generated customer ID

        # Generate invoice
        total_amount = sum(item["total"] for item in self.bill_items)
        invoice = f"--- Supermarket Invoice ---\n"
        invoice += f"Date: {date_str}\n"
        invoice += f"Customer ID: {customer_id}\nName: {name}\nPhone: {phone}\n\n"
        invoice += f"{'Product':<15}{'Price':<10}{'Qty':<8}{'Total':<10}\n"
        invoice += "-"*45 + "\n"
        for item in self.bill_items:
            invoice += f"{item['name']:<15}{item['price']:<10}{item['qty']:<8}{item['total']:<10}\n"
        invoice += "-"*45 + "\n"
        invoice += f"{'Total Bill:':<33}{total_amount}\n"
        invoice += "-"*45 + "\nThank you for shopping!\n"

        self.bill_text.config(state="normal")
        self.bill_text.delete("1.0", tk.END)
        self.bill_text.insert(tk.END, invoice)
        self.bill_text.config(state="disabled")

        # Save invoice to DB
        cursor.execute(
            "INSERT INTO invoices (customer_id, customer_name, customer_phone, invoice_text, total) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, name, phone, invoice, total_amount)
        )
        conn.commit()
        conn.close()

        # Clear bill items and bill tree
        self.bill_items.clear()
        for row in self.bill_tree.get_children():
            self.bill_tree.delete(row)
        self.customer_name.set("")
        self.customer_phone.set("")

# ----------------- Run Application -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SupermarketApp(root)
    root.mainloop()