#!/usr/bin/env python3
"""
Ibrahim Irshaid 1231870
Ameer Khalili 1230881
"""

import os
import sys
import datetime
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import re

class PharmacyManagementSystem:
    def __init__(self):
        """Initialize the PMS with file paths and setup"""
        self.inventory_file = "inventory.txt"
        self.customers_file = "customers.txt"
        self.sales_file = "sales.txt"
        self.users_file = "users.txt"
        self.logs_file = "logs.txt"
        self.error_file = "error.txt"
        self.current_user = None
        self.current_role = None
        
        # Create files if they don't exist
        self.initialize_files()
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Pharmacy Management System")
        self.root.geometry("800x600")
        
    def initialize_files(self):
        """Create necessary files if they don't exist"""
        files = [self.inventory_file, self.customers_file, self.sales_file, 
                self.users_file, self.logs_file, self.error_file]
        
        for file in files:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    if file == self.users_file:
                        # Create default admin user (password: admin123)
                        hashed_pass = hashlib.sha256("admin123".encode()).hexdigest()
                        f.write(f"admin,{hashed_pass},admin\n")
                    pass
    
    def log_action(self, action):
        """Log user actions with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{self.current_user},{self.current_role},{action}\n"
        
        try:
            with open(self.logs_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            self.log_error(f"Failed to write log: {str(e)}")
    
    def log_error(self, error_message):
        """Log errors with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_entry = f"{error_message} at {timestamp}\n"
        
        try:
            with open(self.error_file, 'a') as f:
                f.write(error_entry)
        except:
            pass  # If we can't log the error, we can't do much about it
    
    def validate_date(self, date_string):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_number(self, value):
        """Validate if value is a valid number"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def authenticate_user(self):
        """Handle user authentication"""
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x200")
        login_window.grab_set()
        
        tk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)
        
        tk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password")
                return
            
            # Hash the password for comparison
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                with open(self.users_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split(',')
                            if len(parts) >= 3:
                                stored_user, stored_pass, role = parts[0], parts[1], parts[2]
                                if username == stored_user and hashed_password == stored_pass:
                                    self.current_user = username
                                    self.current_role = role
                                    self.log_action("User logged in")
                                    login_window.destroy()
                                    return True
                
                messagebox.showerror("Error", "Invalid username or password")
                return False
                
            except Exception as e:
                self.log_error(f"Login error: {str(e)}")
                messagebox.showerror("Error", "Login failed")
                return False
        
        tk.Button(login_window, text="Login", command=login).pack(pady=10)
        
        # Wait for login window to close
        self.root.wait_window(login_window)
        
        return self.current_user is not None
    
    def add_medicine(self):
        """Add new medicine to inventory"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        if self.current_role != "admin":
            messagebox.showerror("Error", "Only admins can add medicines")
            return
        
        # Create input dialog
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Medicine")
        add_window.geometry("400x350")
        add_window.grab_set()
        
        # Input fields
        tk.Label(add_window, text="Medicine Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        name_entry = tk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Quantity:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        quantity_entry = tk.Entry(add_window, width=30)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Price:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        price_entry = tk.Entry(add_window, width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Cost:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        cost_entry = tk.Entry(add_window, width=30)
        cost_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Expiry Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        expiry_entry = tk.Entry(add_window, width=30)
        expiry_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Category:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        category_entry = tk.Entry(add_window, width=30)
        category_entry.grid(row=5, column=1, padx=5, pady=5)
        
        def save_medicine():
            name = name_entry.get().strip()
            quantity = quantity_entry.get().strip()
            price = price_entry.get().strip()
            cost = cost_entry.get().strip()
            expiry = expiry_entry.get().strip()
            category = category_entry.get().strip()
            
            # Validation
            if not all([name, quantity, price, cost, expiry, category]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if not self.validate_number(quantity) or not self.validate_number(price) or not self.validate_number(cost):
                messagebox.showerror("Error", "Quantity, price, and cost must be numbers")
                self.log_error("Invalid numeric input for medicine")
                return
            
            if not self.validate_date(expiry):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                self.log_error("Invalid date format")
                return
            
            # Add end date validation
            current_date = datetime.datetime.now().date()
            expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
            if expiry_date <= current_date:
                messagebox.showerror("Error", "Expiry date must be greater than current date")
                return
            
            # Check if medicine already exists
            try:
                with open(self.inventory_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            existing_name = line.split(',')[0]
                            if existing_name.lower() == name.lower():
                                messagebox.showerror("Error", f"Medicine '{name}' already exists")
                                self.log_error(f"Tried to add existing medicine: {name}")
                                return
            except:
                pass
            
            # Add medicine to inventory with cost field
            try:
                with open(self.inventory_file, 'a') as f:
                    f.write(f"{name},{quantity},{price},{cost},{expiry},{category}\n")
                
                messagebox.showinfo("Success", f"Medicine '{name}' added successfully")
                self.log_action(f"Added medicine: {name}")
                add_window.destroy()
                
            except Exception as e:
                self.log_error(f"Failed to add medicine: {str(e)}")
                messagebox.showerror("Error", "Failed to add medicine")
        
        tk.Button(add_window, text="Save", command=save_medicine).grid(row=6, column=0, pady=10)
        tk.Button(add_window, text="Cancel", command=add_window.destroy).grid(row=6, column=1, pady=10)
    
    def update_medicine(self):
        """Update existing medicine details"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        if self.current_role != "admin":
            messagebox.showerror("Error", "Only admins can update medicines")
            return
        
        medicine_name = simpledialog.askstring("Update Medicine", "Enter medicine name to update:")
        if not medicine_name:
            return
        
        # Find and update medicine
        try:
            lines = []
            found = False
            with open(self.inventory_file, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 5 and parts[0].lower() == medicine_name.lower():
                        found = True
                        # Create update window
                        self.show_update_window(parts, i, lines)
                        break
            
            if not found:
                messagebox.showerror("Error", f"Medicine '{medicine_name}' not found")
                self.log_error(f"Tried to update non-existent medicine: {medicine_name}")
                
        except Exception as e:
            self.log_error(f"Update medicine error: {str(e)}")
            messagebox.showerror("Error", "Failed to update medicine")
    
    def show_update_window(self, medicine_parts, line_index, all_lines):
        """Show window for updating medicine details"""
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Medicine")
        update_window.geometry("400x350")
        update_window.grab_set()
        
        name, quantity, price, cost, expiry, category = medicine_parts
        
        tk.Label(update_window, text=f"Updating: {name}").grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(update_window, text="Quantity:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        quantity_entry = tk.Entry(update_window, width=30)
        quantity_entry.insert(0, quantity)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(update_window, text="Price:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        price_entry = tk.Entry(update_window, width=30)
        price_entry.insert(0, price)
        price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(update_window, text="Cost:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        cost_entry = tk.Entry(update_window, width=30)
        cost_entry.insert(0, cost)
        cost_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def save_updates():
            new_quantity = quantity_entry.get().strip()
            new_price = price_entry.get().strip()
            new_cost = cost_entry.get().strip()
            
            if not self.validate_number(new_quantity) or not self.validate_number(new_price) or not self.validate_number(new_cost):
                messagebox.showerror("Error", "Quantity, price, and cost must be numbers")
                return
            
            # Update the line
            all_lines[line_index] = f"{name},{new_quantity},{new_price},{new_cost},{expiry},{category}\n"
            
            try:
                with open(self.inventory_file, 'w') as f:
                    f.writelines(all_lines)
                
                messagebox.showinfo("Success", f"Medicine '{name}' updated successfully")
                self.log_action(f"Updated medicine: {name}")
                update_window.destroy()
                
            except Exception as e:
                self.log_error(f"Failed to save updates: {str(e)}")
                messagebox.showerror("Error", "Failed to save updates")
        
        tk.Button(update_window, text="Save", command=save_updates).grid(row=4, column=0, pady=10)
        tk.Button(update_window, text="Cancel", command=update_window.destroy).grid(row=4, column=1, pady=10)
    
    def remove_expired_medicines(self):
        """Remove all expired medicines from inventory"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        if self.current_role != "admin":
            messagebox.showerror("Error", "Only admins can remove medicines")
            return
        
        current_date = datetime.datetime.now().date()
        removed_count = 0
        
        try:
            lines = []
            with open(self.inventory_file, 'r') as f:
                lines = f.readlines()
            
            updated_lines = []
            for line in lines:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        expiry_date = datetime.datetime.strptime(parts[3], "%Y-%m-%d").date()
                        if expiry_date > current_date:
                            updated_lines.append(line)
                        else:
                            removed_count += 1
                            self.log_action(f"Removed expired medicine: {parts[0]}")
            
            with open(self.inventory_file, 'w') as f:
                f.writelines(updated_lines)
            
            messagebox.showinfo("Success", f"Removed {removed_count} expired medicine(s)")
            
        except Exception as e:
            self.log_error(f"Failed to remove expired medicines: {str(e)}")
            messagebox.showerror("Error", "Failed to remove expired medicines")
    
    def display_inventory(self):
        """Display current inventory in a new window"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Current Inventory")
        inventory_window.geometry("900x400")
        
        # Create treeview for better display with cost column
        columns = ("Name", "Quantity", "Price", "Cost", "Expiry Date", "Category")
        tree = ttk.Treeview(inventory_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        try:
            with open(self.inventory_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            tree.insert("", "end", values=parts)
        except:
            pass
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_action("Viewed inventory")
    
    def process_sale(self):
        """Process a new sale"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        # Create sale window
        sale_window = tk.Toplevel(self.root)
        sale_window.title("Process Sale")
        sale_window.geometry("500x400")
        sale_window.grab_set()
        
        tk.Label(sale_window, text="Customer Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        customer_entry = tk.Entry(sale_window, width=30)
        customer_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(sale_window, text="Medicine Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        medicine_entry = tk.Entry(sale_window, width=30)
        medicine_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(sale_window, text="Quantity:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        quantity_entry = tk.Entry(sale_window, width=30)
        quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def process():
            customer_name = customer_entry.get().strip()
            medicine_name = medicine_entry.get().strip()
            quantity = quantity_entry.get().strip()
            
            if not all([customer_name, medicine_name, quantity]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if not self.validate_number(quantity):
                messagebox.showerror("Error", "Quantity must be a number")
                return
            
            quantity = int(float(quantity))
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            # Process the sale
            if self.execute_sale(customer_name, medicine_name, quantity):
                messagebox.showinfo("Success", "Sale processed successfully")
                sale_window.destroy()
        
        tk.Button(sale_window, text="Process Sale", command=process).grid(row=3, column=0, pady=10)
        tk.Button(sale_window, text="Cancel", command=sale_window.destroy).grid(row=3, column=1, pady=10)
    
    def execute_sale(self, customer_name, medicine_name, quantity):
        """Execute the actual sale transaction"""
        try:
            # Read inventory
            lines = []
            with open(self.inventory_file, 'r') as f:
                lines = f.readlines()
            
            medicine_found = False
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split(',')
                    if len(parts) >= 6 and parts[0].lower() == medicine_name.lower():
                        medicine_found = True
                        current_quantity = int(parts[1])
                        price = float(parts[2])
                        cost = float(parts[3])  # Get cost for profit calculation
                        
                        if current_quantity < quantity:
                            messagebox.showerror("Error", "Insufficient stock")
                            self.log_error(f"Insufficient stock for {medicine_name}")
                            return False
                        
                        # Update inventory
                        new_quantity = current_quantity - quantity
                        lines[i] = f"{parts[0]},{new_quantity},{parts[2]},{parts[3]},{parts[4]},{parts[5]}\n"
                        
                        # Write back to inventory
                        with open(self.inventory_file, 'w') as f:
                            f.writelines(lines)
                        
                        # Record sale with profit information
                        total_price = price * quantity
                        profit = (price - cost) * quantity
                        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        
                        with open(self.sales_file, 'a') as f:
                            f.write(f"{current_date},{medicine_name},{quantity},{total_price},{profit}\n")
                        
                        # Update customer record
                        self.update_customer_record(customer_name, medicine_name, total_price, current_date)
                        
                        # Generate bill
                        self.generate_bill(customer_name, medicine_name, quantity, price, total_price)
                        
                        self.log_action(f"Processed sale: {medicine_name} to {customer_name}")
                        return True
            
            if not medicine_found:
                messagebox.showerror("Error", f"Medicine '{medicine_name}' not found")
                self.log_error(f"Tried to sell non-existent medicine: {medicine_name}")
                return False
                
        except Exception as e:
            self.log_error(f"Sale processing error: {str(e)}")
            messagebox.showerror("Error", "Failed to process sale")
            return False
    
    def update_customer_record(self, customer_name, medicine_name, total_price, date):
        """Update customer purchase history"""
        try:
            # Read existing customers
            lines = []
            customer_found = False
            
            if os.path.exists(self.customers_file):
                with open(self.customers_file, 'r') as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines):
                    if line.strip():
                        parts = line.strip().split(',', 2)  # Split into max 3 parts
                        if len(parts) >= 1 and parts[0].lower() == customer_name.lower():
                            customer_found = True
                            # Add to existing purchase history
                            if len(parts) >= 3:
                                history = parts[2]
                                new_entry = f" [{date}|{medicine_name}|{total_price}]"
                                lines[i] = f"{parts[0]},{parts[1]},{history}{new_entry}\n"
                            break
            
            if not customer_found:
                # New customer - ask for contact info
                contact = simpledialog.askstring("New Customer", f"Enter contact info for {customer_name}:")
                if not contact:
                    contact = "N/A"
                
                purchase_history = f"PurchaseHistory: [{date}|{medicine_name}|{total_price}]"
                lines.append(f"{customer_name},{contact},{purchase_history}\n")
            
            # Write back to file
            with open(self.customers_file, 'w') as f:
                f.writelines(lines)
                
        except Exception as e:
            self.log_error(f"Failed to update customer record: {str(e)}")
    
    def generate_bill(self, customer_name, medicine_name, quantity, unit_price, total_price):
        """Generate and display bill"""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        bill_content = f"""Customer Name: {customer_name:<20} Date: {current_date}

Medicine Name: {medicine_name:<20} Quantity: {quantity:<10} UnitPrice: {unit_price:<10} TotalPrice: {total_price:<10}

Total Bill: {total_price}"""
        
        try:
            with open("bill.txt", 'w') as f:
                f.write(bill_content)
            
            # Show bill in a dialog
            bill_window = tk.Toplevel(self.root)
            bill_window.title("Bill")
            bill_window.geometry("500x300")
            
            text_widget = tk.Text(bill_window, wrap=tk.WORD)
            text_widget.insert("1.0", bill_content)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            self.log_error(f"Failed to generate bill: {str(e)}")
    
    def search_medicine(self):
        """Search for medicines by name or category"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Medicine")
        search_window.geometry("400x200")
        search_window.grab_set()
        
        tk.Label(search_window, text="Search by:").pack(pady=5)
        
        search_type = tk.StringVar(value="name")
        tk.Radiobutton(search_window, text="Medicine Name", variable=search_type, value="name").pack()
        tk.Radiobutton(search_window, text="Category", variable=search_type, value="category").pack()
        
        tk.Label(search_window, text="Enter search term:").pack(pady=5)
        search_entry = tk.Entry(search_window, width=30)
        search_entry.pack(pady=5)
        
        def search():
            search_term = search_entry.get().strip().lower()
            if not search_term:
                messagebox.showerror("Error", "Please enter a search term")
                return
            
            results = []
            try:
                with open(self.inventory_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split(',')
                            if len(parts) >= 5:
                                if search_type.get() == "name":
                                    if search_term in parts[0].lower():
                                        results.append(line.strip())
                                else:  # category
                                    if search_term in parts[4].lower():
                                        results.append(line.strip())
                
                if results:
                    result_text = "\n".join(results)
                    messagebox.showinfo("Search Results", f"Found {len(results)} medicine(s):\n\n{result_text}")
                    self.log_action(f"Searched for: {search_term}")
                else:
                    messagebox.showinfo("Search Results", "No medicines found")
                    self.log_error(f"Search term not found: {search_term}")
                
                search_window.destroy()
                
            except Exception as e:
                self.log_error(f"Search error: {str(e)}")
                messagebox.showerror("Error", "Search failed")
        
        tk.Button(search_window, text="Search", command=search).pack(pady=10)
        tk.Button(search_window, text="Cancel", command=search_window.destroy).pack()
    def sales_trends_analysis(self, parent_window):
        """Analyze sales trends over periods"""
        try:
            # Get period type
            period_window = tk.Toplevel(self.root)
            period_window.title("Sales Trends Analysis")
            period_window.geometry("300x200")
            period_window.grab_set()
            
            tk.Label(period_window, text="Select Analysis Period:").pack(pady=10)
            
            period_var = tk.StringVar(value="monthly")
            tk.Radiobutton(period_window, text="Monthly", variable=period_var, value="monthly").pack()
            tk.Radiobutton(period_window, text="Quarterly", variable=period_var, value="quarterly").pack()
            tk.Radiobutton(period_window, text="Yearly", variable=period_var, value="yearly").pack()
            
            def analyze():
                period_type = period_var.get()
                period_window.destroy()
                
                # Analyze sales based on period
                sales_data = {}
                
                with open(self.sales_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split(',')
                            if len(parts) >= 4:
                                date_obj = datetime.datetime.strptime(parts[0], "%Y-%m-%d")
                                
                                if period_type == "monthly":
                                    period_key = date_obj.strftime("%Y-%m")
                                elif period_type == "quarterly":
                                    quarter = (date_obj.month - 1) // 3 + 1
                                    period_key = f"{date_obj.year}-Q{quarter}"
                                else:  # yearly
                                    period_key = str(date_obj.year)
                                
                                if period_key not in sales_data:
                                    sales_data[period_key] = {"total_sales": 0, "total_quantity": 0}
                                
                                sales_data[period_key]["total_sales"] += float(parts[3])
                                sales_data[period_key]["total_quantity"] += int(parts[2])
                
                # Generate report
                if sales_data:
                    report = f"Sales Trends Analysis ({period_type.title()}):\n\n"
                    for period, data in sorted(sales_data.items()):
                        report += f"{period}: Sales: ${data['total_sales']:.2f}, Quantity: {data['total_quantity']} units\n"
                else:
                    report = "No sales data available for analysis"
                
                self.show_report("Sales Trends Analysis", report)
                self.log_action(f"Generated {period_type} sales trends analysis")
            
            tk.Button(period_window, text="Analyze", command=analyze).pack(pady=10)
            tk.Button(period_window, text="Cancel", command=period_window.destroy).pack()
            
        except Exception as e:
            self.log_error(f"Sales trends analysis error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate sales trends analysis")

    def profit_analysis(self, parent_window):
        """Generate profit analysis report"""
        try:
            # Get date range for profit analysis
            start_date = simpledialog.askstring("Profit Analysis", "Enter start date (YYYY-MM-DD):")
            if not start_date or not self.validate_date(start_date):
                messagebox.showerror("Error", "Invalid start date")
                return
            
            end_date = simpledialog.askstring("Profit Analysis", "Enter end date (YYYY-MM-DD):")
            if not end_date or not self.validate_date(end_date):
                messagebox.showerror("Error", "Invalid end date")
                return
            
            total_profit = 0
            medicine_profits = {}
            
            with open(self.sales_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 5:  # Now includes profit column
                            sale_date = parts[0]
                            if start_date <= sale_date <= end_date:
                                medicine = parts[1]
                                profit = float(parts[4])
                                total_profit += profit
                                
                                if medicine not in medicine_profits:
                                    medicine_profits[medicine] = 0
                                medicine_profits[medicine] += profit
            
            if medicine_profits:
                report = f"Profit Analysis from {start_date} to {end_date}:\n\n"
                report += f"Total Profit: ${total_profit:.2f}\n\n"
                report += "Profit by Medicine:\n"
                
                # Sort by profit descending
                sorted_profits = sorted(medicine_profits.items(), key=lambda x: x[1], reverse=True)
                for medicine, profit in sorted_profits:
                    report += f"{medicine}: ${profit:.2f}\n"
            else:
                report = f"No profit data found between {start_date} and {end_date}"
            
            self.show_report("Profit Analysis", report)
            self.log_action(f"Generated profit analysis for {start_date} to {end_date}")
            
        except Exception as e:
            self.log_error(f"Profit analysis error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate profit analysis")

    def generate_reports(self):
        """Show reports menu"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        reports_window = tk.Toplevel(self.root)
        reports_window.title("Reports")
        reports_window.geometry("300x300")
        reports_window.grab_set()
        
        tk.Label(reports_window, text="Select Report Type:", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Button(reports_window, text="Low Stock Report", width=20, 
                command=lambda: self.low_stock_report(reports_window)).pack(pady=5)
        tk.Button(reports_window, text="Expired Medicines", width=20,
                command=lambda: self.expired_medicines_report(reports_window)).pack(pady=5)
        tk.Button(reports_window, text="Sales Report", width=20,
                command=lambda: self.sales_report(reports_window)).pack(pady=5)
        tk.Button(reports_window, text="Top Selling Medicines", width=20,
                command=lambda: self.top_selling_report(reports_window)).pack(pady=5)
        tk.Button(reports_window, text="Sales Trends Analysis", width=20,
                command=lambda: self.sales_trends_analysis(reports_window)).pack(pady=5)
        tk.Button(reports_window, text="Profit Analysis", width=20,
                command=lambda: self.profit_analysis(reports_window)).pack(pady=5)
        
        tk.Button(reports_window, text="Close", command=reports_window.destroy).pack(pady=10)
    
    def low_stock_report(self, parent_window):
        """Generate low stock report"""
        threshold = simpledialog.askinteger("Low Stock Threshold", 
                                          "Enter maximum quantity for low stock:")
        if threshold is None:
            return
        
        try:
            low_stock_medicines = []
            with open(self.inventory_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 5:
                            quantity = int(parts[1])
                            if quantity <= threshold:
                                low_stock_medicines.append(line.strip())
            
            if low_stock_medicines:
                report = "Low Stock Medicines:\n\n" + "\n".join(low_stock_medicines)
            else:
                report = "No medicines are low in stock."
            
            self.show_report("Low Stock Report", report)
            self.log_action("Generated low stock report")
            
        except Exception as e:
            self.log_error(f"Low stock report error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate report")
    
    def expired_medicines_report(self, parent_window):
        """Generate expired medicines report"""
        try:
            current_date = datetime.datetime.now().date()
            expired_medicines = []
            
            with open(self.inventory_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            expiry_date = datetime.datetime.strptime(parts[3], "%Y-%m-%d").date()
                            if expiry_date < current_date:
                                expired_medicines.append(line.strip())
            
            if expired_medicines:
                report = "Expired Medicines:\n\n" + "\n".join(expired_medicines)
            else:
                report = "No expired medicines found."
            
            self.show_report("Expired Medicines Report", report)
            self.log_action("Generated expired medicines report")
            
        except Exception as e:
            self.log_error(f"Expired medicines report error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate report")
    
    def sales_report(self, parent_window):
        """Generate sales report for a period"""
        # Get date range
        start_date = simpledialog.askstring("Sales Report", "Enter start date (YYYY-MM-DD):")
        if not start_date or not self.validate_date(start_date):
            messagebox.showerror("Error", "Invalid start date")
            return
        
        end_date = simpledialog.askstring("Sales Report", "Enter end date (YYYY-MM-DD):")
        if not end_date or not self.validate_date(end_date):
            messagebox.showerror("Error", "Invalid end date")
            return
        
        try:
            sales_in_period = []
            total_sales = 0
            
            with open(self.sales_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            sale_date = parts[0]
                            if start_date <= sale_date <= end_date:
                                sales_in_period.append(line.strip())
                                total_sales += float(parts[3])
            
            if sales_in_period:
                report = f"Sales Report from {start_date} to {end_date}:\n\n"
                report += "\n".join(sales_in_period)
                report += f"\n\nTotal Sales Amount: {total_sales:.2f}"
            else:
                report = f"No sales found between {start_date} and {end_date}"
            
            self.show_report("Sales Report", report)
            self.log_action(f"Generated sales report for {start_date} to {end_date}")
            
        except Exception as e:
            self.log_error(f"Sales report error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate sales report")
    
    def top_selling_report(self, parent_window):
        """Generate top selling medicines report"""
        top_k = simpledialog.askinteger("Top Selling", "How many top medicines to show:")
        if not top_k or top_k <= 0:
            return
        
        try:
            # Count sales per medicine
            medicine_sales = {}
            
            with open(self.sales_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 3:
                            medicine = parts[1]
                            quantity = int(parts[2])
                            
                            if medicine in medicine_sales:
                                medicine_sales[medicine] += quantity
                            else:
                                medicine_sales[medicine] = quantity
            
            # Sort by quantity sold
            sorted_medicines = sorted(medicine_sales.items(), key=lambda x: x[1], reverse=True)
            top_medicines = sorted_medicines[:top_k]
            
            if top_medicines:
                report = f"Top {top_k} Selling Medicines:\n\n"
                for i, (medicine, quantity) in enumerate(top_medicines, 1):
                    report += f"{i}. {medicine}: {quantity} units sold\n"
            else:
                report = "No sales data available"
            
            self.show_report("Top Selling Medicines", report)
            self.log_action(f"Generated top {top_k} selling medicines report")
            
        except Exception as e:
            self.log_error(f"Top selling report error: {str(e)}")
            messagebox.showerror("Error", "Failed to generate report")
    
    def show_report(self, title, content):
        """Display report in a new window"""
        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry("600x400")
        
        text_widget = tk.Text(report_window, wrap=tk.WORD, font=("Courier", 10))
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(report_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
    
    def view_customer_history(self):
        """View customer purchase history"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        customer_name = simpledialog.askstring("Customer History", "Enter customer name:")
        if not customer_name:
            return
        
        try:
            with open(self.customers_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',', 2)
                        if len(parts) >= 3 and parts[0].lower() == customer_name.lower():
                            history = parts[2] if len(parts) > 2 else "No purchase history"
                            messagebox.showinfo("Customer History", 
                                              f"Customer: {parts[0]}\nContact: {parts[1]}\n\n{history}")
                            self.log_action(f"Viewed customer history: {customer_name}")
                            return
            
            messagebox.showinfo("Customer History", f"Customer '{customer_name}' not found")
            self.log_error(f"Customer not found: {customer_name}")
            
        except Exception as e:
            self.log_error(f"Customer history error: {str(e)}")
            messagebox.showerror("Error", "Failed to retrieve customer history")
    
    def view_logs(self):
        """View system logs (admin only)"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        if self.current_role != "admin":
            messagebox.showerror("Error", "Only admins can view logs")
            return
        
        try:
            with open(self.logs_file, 'r') as f:
                logs_content = f.read()
            
            if logs_content:
                self.show_report("System Logs", logs_content)
                self.log_action("Viewed system logs")
            else:
                messagebox.showinfo("System Logs", "No logs available")
                
        except Exception as e:
            self.log_error(f"View logs error: {str(e)}")
            messagebox.showerror("Error", "Failed to view logs")
    
    def add_user(self):
        """Add new user (admin only)"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        if self.current_role != "admin":
            messagebox.showerror("Error", "Only admins can add users")
            return
        
        user_window = tk.Toplevel(self.root)
        user_window.title("Add User")
        user_window.geometry("350x250")
        user_window.grab_set()
        
        tk.Label(user_window, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        username_entry = tk.Entry(user_window, width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(user_window, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        password_entry = tk.Entry(user_window, show="*", width=25)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(user_window, text="Role:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        role_var = tk.StringVar(value="pharmacist")
        role_combo = ttk.Combobox(user_window, textvariable=role_var, values=["admin", "pharmacist"], width=22)
        role_combo.grid(row=2, column=1, padx=5, pady=5)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            
            if not all([username, password, role]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Check if user already exists
            try:
                with open(self.users_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            existing_user = line.split(',')[0]
                            if existing_user == username:
                                messagebox.showerror("Error", f"User '{username}' already exists")
                                return
            except:
                pass
            
            # Hash password and save user
            try:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                with open(self.users_file, 'a') as f:
                    f.write(f"{username},{hashed_password},{role}\n")
                
                messagebox.showinfo("Success", f"User '{username}' added successfully")
                self.log_action(f"Added user: {username} with role: {role}")
                user_window.destroy()
                
            except Exception as e:
                self.log_error(f"Failed to add user: {str(e)}")
                messagebox.showerror("Error", "Failed to add user")
        
        tk.Button(user_window, text="Save", command=save_user).grid(row=3, column=0, pady=15)
        tk.Button(user_window, text="Cancel", command=user_window.destroy).grid(row=3, column=1, pady=15)
    
    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main title
        title_label = tk.Label(self.root, text="Pharmacy Management System", 
                              font=("Arial", 18, "bold"), fg="blue")
        title_label.pack(pady=20)
        
        # User info
        user_info = tk.Label(self.root, text=f"Welcome, {self.current_user} ({self.current_role})", 
                            font=("Arial", 12))
        user_info.pack(pady=5)
        
        # Create menu frame
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)
        
        # Inventory Management Section
        inventory_frame = tk.LabelFrame(menu_frame, text="Inventory Management", 
                                       font=("Arial", 12, "bold"), padx=10, pady=10)
        inventory_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        if self.current_role == "admin":
            tk.Button(inventory_frame, text="Add Medicine", width=20, 
                     command=self.add_medicine).pack(pady=2)
            tk.Button(inventory_frame, text="Update Medicine", width=20, 
                     command=self.update_medicine).pack(pady=2)
            tk.Button(inventory_frame, text="Remove Expired", width=20, 
                     command=self.remove_expired_medicines).pack(pady=2)
        
        tk.Button(inventory_frame, text="Display Inventory", width=20, 
                 command=self.display_inventory).pack(pady=2)
        
        # Sales Management Section
        sales_frame = tk.LabelFrame(menu_frame, text="Sales Management", 
                                   font=("Arial", 12, "bold"), padx=10, pady=10)
        sales_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        tk.Button(sales_frame, text="Process Sale", width=20, 
                 command=self.process_sale).pack(pady=2)
        tk.Button(sales_frame, text="Customer History", width=20, 
                 command=self.view_customer_history).pack(pady=2)
        
        # Reports Section
        reports_frame = tk.LabelFrame(menu_frame, text="Reports & Analytics", 
                                     font=("Arial", 12, "bold"), padx=10, pady=10)
        reports_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        tk.Button(reports_frame, text="Generate Reports", width=20, 
                 command=self.generate_reports).pack(pady=2)
        tk.Button(reports_frame, text="Search Medicine", width=20, 
                 command=self.search_medicine).pack(pady=2)
        
        # System Management Section
        system_frame = tk.LabelFrame(menu_frame, text="System Management", 
                                    font=("Arial", 12, "bold"), padx=10, pady=10)
        system_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        if self.current_role == "admin":
            tk.Button(system_frame, text="Add User", width=20, 
                     command=self.add_user).pack(pady=2)
            tk.Button(system_frame, text="View Logs", width=20, 
                     command=self.view_logs).pack(pady=2)
        
        # Logout and Exit buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Logout", width=15, bg="orange", 
                 command=self.logout).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", width=15, bg="red", 
                 command=self.exit_application).pack(side=tk.LEFT, padx=5)
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            self.log_action("User logged out")
        
        self.current_user = None
        self.current_role = None
        
        # Clear the main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show login again
        self.run()
    
    def exit_application(self):
        """Exit the application"""
        if self.current_user:
            self.log_action("Application exited")
        
        self.root.quit()
        self.root.destroy()
        sys.exit()
    
    def run(self):
        """Main application loop"""
        # First, try to authenticate user
        if self.authenticate_user():
            # Create and show main menu
            self.create_main_menu()
            
            # Set up window close event
            self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
            
            # Start the GUI event loop
            self.root.mainloop()
        else:
            # Authentication failed or cancelled
            messagebox.showinfo("Goodbye", "Thank you for using Pharmacy Management System")
            self.root.quit()
            self.root.destroy()


def main():
    """Main function to run the Pharmacy Management System"""
    try:
        # Create and run the PMS
        pms = PharmacyManagementSystem()
        pms.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()