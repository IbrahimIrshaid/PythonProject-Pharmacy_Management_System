# 💊 Pharmacy Management System (PMS)

A comprehensive desktop application for managing pharmacy inventory, sales, users, and reports. Built with **Python 3** and **Tkinter**, the system supports secure login, user role control, inventory tracking, sales processing, reporting, and analytics.

---

## 👨‍💻 Authors

- **Ibrahim Irshaid** - 1231870  
- **Ameer Khalili** - 1230881

---

## 📦 Features

### 🔐 Authentication
- Secure login system with password hashing (`SHA-256`)
- Role-based access control: `admin` and `pharmacist`
- Default admin: `admin/admin123`

### 📦 Inventory Management
- Add/update/remove medicines *(admin only)*
- Validate expiry dates
- Search by name or category
- View entire inventory with detailed fields (name, quantity, price, cost, expiry date, category)

### 💰 Sales Management
- Process medicine sales
- Auto-generate bill (saved to `bill.txt`)
- Update stock and customer records
- Record profit per transaction

### 👤 Customer Management
- Add new customers
- Maintain purchase history
- View customer history

### 📊 Reports & Analytics
- Sales report (custom date range)
- Low stock report
- Expired medicines report
- Top selling medicines
- Profit analysis (total and per medicine)
- Sales trends analysis (monthly, quarterly, yearly)

### 🛠️ System Management *(admin only)*
- Add new users with roles
- View system logs
- All actions and errors are logged

---

## 🖥️ GUI Overview

- Built using `Tkinter`
- Interactive, responsive interface with `Toplevel`, `Treeview`, and `SimpleDialog`
- Windowed views for login, medicine entry, updates, sales, and reports

---

## 📁 Project Structure

```
📦 Pharmacy Management System
│
├── pms_python.py         # Main application script
├── inventory.txt         # Stores medicine data
├── customers.txt         # Stores customer records
├── sales.txt             # Logs sales transactions
├── users.txt             # Stores user credentials and roles
├── logs.txt              # Logs user actions
├── error.txt             # Logs application errors
└── bill.txt              # Auto-generated sales bills
```

---

## ⚙️ How to Run

1. Ensure you have **Python 3** installed.
2. Run the script:

```bash
python3 pms_python.py
```

3. Login with the default admin credentials:
   - Username: `admin`
   - Password: `admin123`

> On first run, all necessary `.txt` files are auto-created if missing.

---

## 🛡️ Security

- Passwords are stored using **SHA-256 hashing**
- Admins can add other users (admin/pharmacist)
- Logs include timestamps, actions, and usernames

---

## 🚫 Limitations

- No database; uses plain text files for data persistence
- Desktop only; no web or mobile interface
- Single-user GUI (no concurrency/multi-client support)

---

## 📝 Notes

- Avoid manual edits to `.txt` files to prevent format issues
- For analysis features to work, ensure `sales.txt` is populated through proper sale entries
- Log and error files are overwritten only on new sessions

---

## 📌 Future Improvements

- Migrate to a database (e.g., SQLite or PostgreSQL)
- Add barcode scanning
- Implement multi-user concurrent access
- Export reports to PDF/CSV
