# Friday Project 5
# 📂 Simple Customer Data System

This repository contains a simple Python application designed to collect customer information via a GUI and store it persistently using the **SQLite database** engine.

---

## 🚀 Getting Started

To run this project, you only need **Python 3.x** installed.

1.  **Clone the Repository:** Download or clone the files to your local machine.
2.  **Run the GUI:** Execute the main application file to start the data entry window.
3.  **View the Data:** Run the utility script to inspect the database contents.

---

## 📁 Project Files Explained

| File Name | Primary Role | Details |
| :--- | :--- | :--- |
| **`fridayProject5.py`** | **Data Entry Interface (GUI)** | This is the main script that uses a library (likely **Tkinter**) to display a window. It handles collecting customer inputs and executing the **SQL INSERT statement** to save the data. |
| **`readDB.py`** | **Data Viewer Utility** | This script connects to the `customers.db` file and runs an **SQL SELECT statement** to retrieve *all* records. It then prints the organized data (with headers) directly to your console. |
| **`customers.db`** | **SQLite Database** | This file holds all the structured customer data. It's automatically created or updated when you submit data through the GUI. |

---

## 📝 How to Use the Scripts

### 1. Launch the Customer GUI

Run this command to open the input form:

```bash
python fridayProject5.py