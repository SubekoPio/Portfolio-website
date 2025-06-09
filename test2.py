import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

# --------------------------------------------------
# MySQL Connection and Table Setup
# --------------------------------------------------

db_config = {
    'user': 'root',
    'password': 'subeko223',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'management'
}

# Connect to the MySQL database, create it if it doesn't exist.
try:
    conn = mysql.connector.connect(**db_config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        try:
            temp_conn = mysql.connector.connect(user=db_config['user'],
                                                password=db_config['subeko223'],
                                                host=db_config['localhost'])
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_config['database']))
            temp_conn.database = db_config['database']
            conn = temp_conn
            print("Database created successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed creating database: {err}")
            exit(1)
    else:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        exit(1)

cursor = conn.cursor()

# Create the students table if it doesn't exist, with class and section columns.
create_students_table = '''
    CREATE TABLE IF NOT EXISTS students (
        reg_no VARCHAR(10) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        class VARCHAR(50),
        section VARCHAR(50)
    )
'''
try:
    cursor.execute(create_students_table)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error creating students table: {err}")
    exit(1)

# Create the class_section table if it doesn't exist.
create_class_section_table = '''
    CREATE TABLE IF NOT EXISTS class_section (
        class VARCHAR(50) PRIMARY KEY,
        section VARCHAR(50) NOT NULL,
        fee INT NOT NULL
    )
'''
try:
    cursor.execute(create_class_section_table)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error creating class_section table: {err}")
    exit(1)

# Create the payments table if it doesn't exist.
create_payments_table = '''
    CREATE TABLE IF NOT EXISTS payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        reg_no VARCHAR(10) NOT NULL,
        term VARCHAR(50) NOT NULL,
        fee INT NOT NULL,
        amount_paid INT NOT NULL,
        balance INT NOT NULL,
        payment_date DATETIME NOT NULL,
        FOREIGN KEY (reg_no) REFERENCES students(reg_no)
    )
'''
try:
    cursor.execute(create_payments_table)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error creating payments table: {err}")
    exit(1)

# --------------------------------------------------
# GUI Setup
# --------------------------------------------------

root = tk.Tk()
root.title("Student Payment System")
root.geometry("800x650")

# ----------- Search Section -----------
search_frame = tk.LabelFrame(root, text="Search Student", padx=30, pady=10)
search_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

search_reg_label = tk.Label(search_frame, text="Registration Number:")
search_reg_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
search_reg_entry = tk.Entry(search_frame)
search_reg_entry.grid(row=0, column=1, padx=5, pady=5)

search_name_label = tk.Label(search_frame, text="Student Name:")
search_name_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
search_name_entry = tk.Entry(search_frame)
search_name_entry.grid(row=0, column=3, padx=5, pady=5)

# ----------- Payment Section -----------
payment_frame = tk.LabelFrame(root, text="Payment Details", padx=10, pady=10)
payment_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Registration Number (read-only)
payment_reg_label = tk.Label(payment_frame, text="Registration Number:")
payment_reg_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
payment_reg_entry = tk.Entry(payment_frame, state="readonly")
payment_reg_entry.grid(row=0, column=1, padx=5, pady=5)

# Student Name (read-only)
payment_name_label = tk.Label(payment_frame, text="Student Name:")
payment_name_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
payment_name_entry = tk.Entry(payment_frame, state="readonly")
payment_name_entry.grid(row=0, column=3, padx=5, pady=5)

# Class (read-only, same row as name)
class_label = tk.Label(payment_frame, text="Class:")
class_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
class_entry = tk.Entry(payment_frame, state="readonly")
class_entry.grid(row=0, column=5, padx=5, pady=5)

# Term Combobox
term_label = tk.Label(payment_frame, text="Term:")
term_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
term_combobox = ttk.Combobox(payment_frame, values=["term1", "term2", "term3"], state="readonly")
term_combobox.grid(row=1, column=1, padx=5, pady=5)
term_combobox.set("Select Term")

# Amount Entry with integer validation.
amount_label = tk.Label(payment_frame, text="Amount to Pay:")
amount_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

amount_entry = tk.Entry(payment_frame)
amount_entry.grid(row=1, column=3, padx=5, pady=5)

error_label = tk.Label(payment_frame, text="", fg="red")
error_label.grid(row=2, column=2, columnspan=4, sticky="w", padx=5)

def validate_amount(new_value):
    """
    Validate that the amount entry has only digits or is empty.
    """
    if new_value == "":
        error_label.config(text="")
        return True
    if new_value.isdigit():
        error_label.config(text="")
        return True
    error_label.config(text="Error: Only integers allowed for amount.")
    return False

vcmd = (root.register(validate_amount), '%P')
amount_entry = tk.Entry(payment_frame, validate="key", validatecommand=vcmd)
amount_entry.grid(row=1, column=3, padx=5, pady=5)

# Section (read-only, same row as amount)
section_label = tk.Label(payment_frame, text="Section:")
section_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")
section_entry = tk.Entry(payment_frame, state="readonly")
section_entry.grid(row=1, column=5, padx=5, pady=5)

# Receipt/Invoice Text Area
receipt_label = tk.Label(payment_frame, text="Payment Receipt / Invoice:")
receipt_label.grid(row=2, column=0, padx=5, pady=(15, 5), sticky="w", columnspan=2)
receipt_text = tk.Text(payment_frame, height=10, width=70, state="disabled", bg="#f9f9f9")
receipt_text.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

# Print Button
def print_receipt():
    import tempfile
    import os
    import platform
    receipt = receipt_text.get("1.0", tk.END)
    if not receipt.strip():
        messagebox.showerror("Print Error", "No receipt to print.")
        return
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp:
        temp.write(receipt)
        temp_path = temp.name
    if platform.system() == "Windows":
        os.startfile(temp_path, "print")
    else:
        os.system(f"lp {temp_path}")
    messagebox.showinfo("Print", "Receipt sent to printer.")

print_btn = tk.Button(payment_frame, text="Print Receipt" , cursor="hand2", command=print_receipt)
print_btn.grid(row=4, column=2, padx=5, pady=10, sticky="e")

# error_label = tk.Label(payment_frame, text="", fg="red")
# error_label.grid(row=2, column=3, padx=5, pady=(0, 5), sticky="w")


def get_class_fee(student_class):
    cursor.execute("SELECT fee FROM class_section WHERE class = %s", (student_class,))
    result = cursor.fetchone()
    return result[0] if result else 0

# ----------- Search Logic -----------

def search_student():
    reg_no_input = search_reg_entry.get().strip()
    name_input = search_name_entry.get().strip()
    student = None
    try:
        if reg_no_input:
            reg_no = str(reg_no_input)
            cursor.execute("SELECT reg_no, name, class, section FROM students WHERE reg_no = %s", (reg_no,))
            student = cursor.fetchone()
        elif name_input:
            cursor.execute("SELECT reg_no, name, class, section FROM students WHERE name = %s", (name_input,))
            student = cursor.fetchone()
        else:
            messagebox.showerror("Search Error", "Please enter either a registration number or student name to search.")
            return
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error during search: {err}")
        return

    if student:
        reg_no, name, student_class, student_section = student
        payment_reg_entry.config(state="normal")
        payment_reg_entry.delete(0, tk.END)
        payment_reg_entry.insert(0, str(reg_no))
        payment_reg_entry.config(state="readonly")
        
        payment_name_entry.config(state="normal")
        payment_name_entry.delete(0, tk.END)
        payment_name_entry.insert(0, name)
        payment_name_entry.config(state="readonly")

        class_entry.config(state="normal")
        class_entry.delete(0, tk.END)
        class_entry.insert(0, student_class if student_class else "")
        class_entry.config(state="readonly")

        section_entry.config(state="normal")
        section_entry.delete(0, tk.END)
        section_entry.insert(0, student_section if student_section else "")
        section_entry.config(state="readonly")

        # Also load the payment records for this student.
        load_payments(reg_no)
    else:
        messagebox.showerror("Search Error", "Student not found, either invalid registration number/name or student not registered.")
        payment_reg_entry.config(state="normal")
        payment_reg_entry.delete(0, tk.END)
        payment_reg_entry.config(state="readonly")
        payment_name_entry.config(state="normal")
        payment_name_entry.delete(0, tk.END)
        payment_name_entry.config(state="readonly")
        class_entry.config(state="normal")
        class_entry.delete(0, tk.END)
        class_entry.config(state="readonly")
        section_entry.config(state="normal")
        section_entry.delete(0, tk.END)
        section_entry.config(state="readonly")
        for item in tree.get_children():
            tree.delete(item)

search_btn = tk.Button(search_frame, text="Search", cursor="hand2", command=search_student)
search_btn.grid(row=0, column=4, padx=5, pady=5)

def clear_fields():
    search_reg_entry.delete(0, tk.END)
    search_name_entry.delete(0, tk.END)
    payment_reg_entry.config(state="normal")
    payment_reg_entry.delete(0, tk.END)
    payment_reg_entry.config(state="readonly")
    payment_name_entry.config(state="normal")
    payment_name_entry.delete(0, tk.END)
    payment_name_entry.config(state="readonly")
    class_entry.config(state="normal")
    class_entry.delete(0, tk.END)
    class_entry.config(state="readonly")
    section_entry.config(state="normal")
    section_entry.delete(0, tk.END)
    section_entry.config(state="readonly")
    amount_entry.delete(0, tk.END)
    term_combobox.set("Select Term")
    error_label.config(text="")
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.config(state="disabled")
    #for item in tree.get_children():
       # tree.delete(item)

clear_btn = tk.Button(search_frame, text="Clear" ,cursor="hand2", command=clear_fields)
clear_btn.grid(row=0, column=5, padx=5, pady=5)

#-----------show all button--------------

showall_btn = tk.Button(search_frame, text="Show All", cursor="hand2", command=lambda: load_payments())
showall_btn.grid(row=0, column=6, padx=5, pady=5)

# ----------- Payment Logic -----------
def process_payment():
    reg_no_text = payment_reg_entry.get().strip()
    if not reg_no_text:
        messagebox.showerror("Input Error", "Please search for a student first.")
        return

    student_reg_no = str(reg_no_text)
    student_name = payment_name_entry.get().strip()
    student_class = class_entry.get().strip()
    student_section = section_entry.get().strip()
    term = term_combobox.get()
    if not student_class:
        messagebox.showerror("Input Error", "Student class not found. Please check student record.")
        return
    term = term_combobox.get()
    if term not in ["term1", "term2", "term3"]:
        error_label.config(text="Error: Please select a valid term.")
        # messagebox.showerror("Input Error", "Please select a valid term before making payment.")
        return

    # Get the fee for the student's class
    fee = get_class_fee(student_class)
    if not fee:
        messagebox.showerror("Fee Error", f"No fee set for class '{student_class}'. Please check class_section table.")
        return

    amount_text = amount_entry.get().strip()
    if not amount_text:
        messagebox.showerror("Input Error", "Please enter the payment amount.")
        return

    try:
        amount_paid = int(amount_text)
    except ValueError:
        messagebox.showerror("Input Error", "The amount must be an integer.")
        return

    term_order = ["term1", "term2", "term3"]
    term_index = term_order.index(term)

    # Helper: Get the carry-over for a term, recursively if needed
    def get_carry_over(reg_no, idx):
        if idx == 0:
            return 0
        prev_term = term_order[idx - 1]
        cursor.execute(
            "SELECT balance FROM payments WHERE reg_no = %s AND term = %s ORDER BY id DESC LIMIT 1",
            (reg_no, prev_term)
        )
        prev = cursor.fetchone()
        prev_balance = prev[0] if prev and prev[0] > 0 else 0
        if prev_balance > 0:
            cursor.execute(
                "SELECT fee FROM payments WHERE reg_no = %s AND term = %s ORDER BY id DESC LIMIT 1",
                (reg_no, prev_term)
            )
            prev_fee = cursor.fetchone()
            if prev_fee and prev_fee[0] == 0:
                return prev_balance + get_carry_over(reg_no, idx - 1)
            else:
                return prev_balance
        return 0

    # Helper: Check if a term is fully paid (balance >= 0, considering carry-over)
    def is_term_fully_paid(reg_no, term):
        idx = term_order.index(term)
        cursor.execute(
            "SELECT SUM(amount_paid) FROM payments WHERE reg_no = %s AND term = %s",
            (reg_no, term)
        )
        total_paid = cursor.fetchone()[0] or 0
        fee_for_term = get_class_fee(class_entry.get().strip())
        carry_over = get_carry_over(reg_no, idx)
        effective_fee = max(fee_for_term - carry_over, 0)
        return total_paid >= effective_fee

    # Check if all terms are fully paid
    all_terms_paid = all(is_term_fully_paid(student_reg_no, t) for t in term_order)
    if all_terms_paid:
        messagebox.showerror(
            "All Terms Paid",
            "All term payments are completed. Please keep the payment receipt for next year's payment."
        )
        return

    # If selected term is already fully paid, find the next unpaid term
    original_term = term
    while is_term_fully_paid(student_reg_no, term):
        term_index += 1
        if term_index >= len(term_order):
            messagebox.showinfo(
                "Term Already Paid",
                f"You have already completed all fees for {original_term.capitalize()}.\n"
                "All term payments are completed. Please keep the payment receipt for next year's payment."
            )
            return
        term = term_order[term_index]

    # Calculate carry-over for this term (using the recursive logic)
    carry_over = get_carry_over(student_reg_no, term_order.index(term))
    fee = get_class_fee(class_entry.get().strip())
    effective_fee = max(fee - carry_over, 0)

    # Get total previously paid for this term
    cursor.execute(
        "SELECT SUM(amount_paid) FROM payments WHERE reg_no = %s AND term = %s",
        (student_reg_no, term)
    )
    previous_paid = cursor.fetchone()[0] or 0

    # Calculate new total paid for this term
    total_paid = previous_paid + amount_paid

    # Calculate balance based on total paid
    balance = total_paid - effective_fee

    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare a feedback message.
    if original_term != term:
        msg = (
            f"You have already completed all fees for {original_term.capitalize()}.\n"
            f"Your payment has been carried to {term.capitalize()}.\n\n"
        )
    else:
        msg = ""

    if effective_fee == 0 and carry_over > 0:
        msg += (
            f"Your carry-over from previous term(s) fully covers {term.capitalize()}.\n"
            f"No payment is required for this term, but your payment will be recorded as an additional credit."
        )
    elif balance == 0:
        msg += f"Payment successful!\n\n{student_name}, you've paid the exact fee for {term.capitalize()}."
    elif balance < 0:
        msg += f"Payment recorded with debit balance.\n\n{student_name}, you still owe {abs(balance)} for {term.capitalize()}."
    else:
        msg += f"Payment recorded with credit balance.\n\n{student_name}, you've overpaid by {balance} for {term.capitalize()}.\nThis will be carried to the next term."

    insert_query = '''
        INSERT INTO payments (reg_no, term, fee, amount_paid, balance, payment_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    try:
        cursor.execute(insert_query, (student_reg_no, term, fee, amount_paid, balance, payment_date))
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting record: {err}")
        return

    messagebox.showinfo("Payment Status", msg)

    # Get balances for all terms
    balances_info = ""
    for t in ["term1", "term2", "term3"]:
        cursor.execute(
            "SELECT SUM(amount_paid) FROM payments WHERE reg_no = %s AND term = %s",
            (student_reg_no, t)
        )
        paid = cursor.fetchone()[0] or 0
        fee_for_term = get_class_fee(student_class)
        idx = term_order.index(t)
        carry_over = get_carry_over(student_reg_no, idx)
        effective_fee = max(fee_for_term - carry_over, 0)
        bal = paid - effective_fee
        balances_info += f"{t.capitalize()} Balance: {bal}\n"

    # Generate and display receipt
    receipt = (
    f"--- PAYMENT RECEIPT ---\n"
    f"Date: {payment_date}\n"
    f"Name: {student_name}\n"
    f"Registration No: {student_reg_no}\n"
    f"Class: {student_class}\n"
    f"Section: {student_section}\n"
    f"Term: {term.capitalize()}\n"
    f"Term Fee: {fee}\n"
    f"Carry-over: {carry_over}\n"
    f"Amount Paid: {amount_paid}\n"
    f"Total Paid for Term: {total_paid}\n"
    f"Balance for Term: {balance}\n"
    f"\n{msg}\n"
    f"-----------------------\n"
    
    )

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, receipt)
    receipt_text.config(state="disabled")

    # Reset the form for the next input.
    payment_name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    term_combobox.current(0)
    error_label.config(text="")

    # Reload the Treeview with updated records.
    load_payments(student_reg_no)

submit_button = tk.Button(payment_frame, text="Submit Payment" , cursor="hand2", command=process_payment)
submit_button.grid(row=4, column=1, padx=5, pady=10, sticky="e")

# ------------------------------------------
# Treeview Section (Display Payment Records)
# ------------------------------------------

tree_frame = tk.Frame(root)
tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Add horizontal scrollbar
tree_xscroll = tk.Scrollbar(tree_frame, orient="horizontal")
tree_xscroll.pack(side=tk.BOTTOM, fill=tk.X)

tree = ttk.Treeview(
    tree_frame,
    yscrollcommand=tree_scroll.set,
    xscrollcommand=tree_xscroll.set,
    columns=("ID", "Name", "Class", "Section", "Term", "Fee", "Paid", "Balance", "Date"),
    show="headings"
)


tree.column("ID", width=30, anchor="center")
tree.column("Name", width=120, anchor="w")
tree.column("Class", width=80, anchor="center")
tree.column("Section", width=80, anchor="center")
tree.column("Term", width=60, anchor="center")
tree.column("Fee", width=60, anchor="center")
tree.column("Paid", width=60, anchor="center")
tree.column("Balance", width=60, anchor="center")
tree.column("Date", width=130, anchor="w")

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Class", text="Class")
tree.heading("Section", text="Section")
tree.heading("Term", text="Term")
tree.heading("Fee", text="Fee")
tree.heading("Paid", text="Paid")
tree.heading("Balance", text="Balance")
tree.heading("Date", text="Date")
tree.pack(fill=tk.BOTH, expand=True)


tree_scroll.config(command=tree.yview)
tree_xscroll.config(command=tree.xview)


def load_payments(reg_no=None):
    """
    Retrieves payment records from the MySQL database
    and loads them into the Treeview.
    If reg_no is provided, only loads payments for that student.
    """
    for item in tree.get_children():
        tree.delete(item)
    if reg_no:
        select_query = '''
            SELECT payments.id, students.name, students.class, students.section, payments.term, payments.fee, payments.amount_paid, payments.balance, payments.payment_date
            FROM payments
            JOIN students ON payments.reg_no = students.reg_no
            WHERE payments.reg_no = %s
            ORDER BY payments.id DESC
        '''
        params = (reg_no,)
    else:
        select_query = '''
            SELECT payments.id, students.name, students.class, students.section, payments.term, payments.fee, payments.amount_paid, payments.balance, payments.payment_date
            FROM payments
            JOIN students ON payments.reg_no = students.reg_no
            ORDER BY payments.id DESC
        '''
        params = ()
    try:
        cursor.execute(select_query, params)
        records = cursor.fetchall()
        for row in records:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching records: {err}")


# 🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️  On select tree view 🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️🏘️

def on_tree_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if not values or len(values) < 9:
        return

    # Unpack values
    payment_id, name, student_class, student_section, term, fee, amount_paid, balance, payment_date = values

    # Fill entry fields
    payment_name_entry.config(state="normal")
    payment_name_entry.delete(0, tk.END)
    payment_name_entry.insert(0, name)
    payment_name_entry.config(state="readonly")

    class_entry.config(state="normal")
    class_entry.delete(0, tk.END)
    class_entry.insert(0, student_class)
    class_entry.config(state="readonly")

    section_entry.config(state="normal")
    section_entry.delete(0, tk.END)
    section_entry.insert(0, student_section)
    section_entry.config(state="readonly")

    term_combobox.set(term)
    # amount_entry.delete(0, tk.END)
    # amount_entry.insert(0, amount_paid)

    # Get reg_no for the selected payment
    cursor.execute("SELECT reg_no FROM payments WHERE id = %s", (payment_id,))
    reg_no_row = cursor.fetchone()
    reg_no = reg_no_row[0] if reg_no_row else ""

    payment_reg_entry.config(state="normal")
    payment_reg_entry.delete(0, tk.END)
    payment_reg_entry.insert(0, reg_no)
    payment_reg_entry.config(state="readonly")

    # Generate and display receipt
    receipt = (
        f"--- PAYMENT RECEIPT ---\n"
        f"Date: {payment_date}\n"
        f"Name: {name}\n"
        f"Registration No: {reg_no}\n"
        f"Class: {student_class}\n"
        f"Section: {student_section}\n"
        f"Term: {term.capitalize()}\n"
        f"Term Fee: {fee}\n"
        f"Amount Paid: {amount_paid}\n"
        f"Balance for Term: {balance}\n"
        f"-----------------------\n"
    )
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, receipt)
    receipt_text.config(state="disabled")
    #tree.selection_remove(tree.selection())

def clear_tree_selection(event):
    tree.selection_remove(tree.selection())

tree.bind("<<TreeviewSelect>>", on_tree_select)
tree.bind("<ButtonRelease-1>", clear_tree_selection)


root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

load_payments()

root.mainloop()