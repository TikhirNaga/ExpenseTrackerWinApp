# ExpenseTrackerWinApp
A Windows expense tracker app built with Python, Tkinter (GUI), SQLite (data storage), and ReportLab (PDF export). Lets users add, view, and categorize expenses, calculate totals, and download reports. Perfect for students and individuals seeking simple, offline money tracking.

---

## 🧩 Features

- 📅 Add expenses with **date**, **category**, **amount**, and **description**
- 🗂 View expense history in a tabular format
- 🗑️ Delete individual records
- 📊 Real-time calculation of total expenses
- 📄 Export data to **PDF summary reports**
- 🎨 Clean and intuitive graphical user interface (GUI)
- 💾 Offline data storage using **SQLite database**

---

## 🏗️ Tech Stack

| Component | Technology Used |
|----------|-----------------|
| Language | Python 3 |
| GUI Framework | Tkinter |
| Database | SQLite |
| PDF Generator | ReportLab |
| Packaging Tool | PyInstaller (for .exe generation) |

---

## 🚀 How to Run

git clone https://github.com/TikhirNaga/expenseTrackerWinApp
cd expenseTrackerWinApp

python expense_tracker.py

## To Generate .exe

pip install pyinstaller
pyinstaller --onefile --windowed expense_tracker.py

### 🔧 Prerequisites

- Python installed (3.10 or above)
- Packages:
  ```bash
  pip install reportlab
