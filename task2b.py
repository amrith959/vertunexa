import sqlite3
import logging
import tkinter as tk
from tkinter import messagebox

# Setup logging
logging.basicConfig(filename='calculator.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            result REAL
        )
    ''')
    conn.commit()
    conn.close()

# Save operation to DB
def save_to_db(operation, result):
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (operation, result) VALUES (?, ?)', (operation, result))
    conn.commit()
    conn.close()

# Console Calculator
def console_calculator():
    print("\nConsole Calculator")
    print("Operations: +, -, *, /")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            expression = input("Enter expression (ex: 5 + 3): ")

            if expression.lower() == 'exit':
                print("Goodbye!")
                break

            parts = expression.split()

            if len(parts) != 3:
                raise ValueError("Invalid format! Use: number operator number")

            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero!")
                result = num1 / num2
            else:
                raise ValueError("Unsupported operator!")

            print(f"Result: {result}")

            operation_str = f"{num1} {operator} {num2}"
            save_to_db(operation_str, result)
            logging.info(f"{operation_str} = {result}")

        except Exception as e:
            print(f"Error: {e}")

# GUI Calculator
def gui_calculator():
    def calculate():
        try:
            expr = entry.get()
            result = eval(expr)
            result_label.config(text=f"Result: {result}")

            save_to_db(expr, result)
            logging.info(f"{expr} = {result}")

        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input! {e}")

    root = tk.Tk()
    root.title("Tkinter Calculator")

    entry = tk.Entry(root, width=30, font=("Arial", 16))
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    result_label = tk.Label(root, text="Result: ", font=("Arial", 16))
    result_label.grid(row=1, column=0, columnspan=4, pady=10)

    btn_calculate = tk.Button(root, text="Calculate", command=calculate, width=15, font=("Arial", 12))
    btn_calculate.grid(row=2, column=0, columnspan=4, pady=10)

    root.mainloop()

# Main entry point
if __name__ == '__main__':
    init_db()

    print("Welcome to Combined Calculator App")
    print("Choose Mode:")
    print("1. Console Calculator")
    print("2. GUI Calculator")
    mode = input("Enter 1 or 2: ")

    if mode == '1':
        console_calculator()
    elif mode == '2':
        gui_calculator()
    else:
        print("Invalid selection. Exiting...")
