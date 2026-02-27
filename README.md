# 📦 Inventory Management System (Full-Stack: Streamlit + Python + MySQL)

![Python](https://img.shields.io/badge/Language-Python-blue)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![Type](https://img.shields.io/badge/Type-Full%20Stack-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📝 Problem Statement

Many small and medium businesses struggle with:

- ❌ Manual inventory tracking  
- ❌ Stock shortages or overstocking  
- ❌ No centralized sales tracking  
- ❌ Delayed reorder processing  
- ❌ No real-time dashboard visibility  

There is a need for a **centralized, automated, and interactive inventory system** that:

- Tracks products and suppliers  
- Monitors stock levels in real-time  
- Records sales and restocking  
- Automatically handles reorders  
- Provides analytical insights through a dashboard  

This project solves these problems using:

- **MySQL (Database Layer)**
- **Python + MySQL Connector (Backend Logic)**
- **Streamlit (Frontend Dashboard)**

---

# 🚀 Project Overview

This is a **Full-Stack Inventory Management System** built using:

- 🐍 Python
- 🗄️ MySQL
- 🎨 Streamlit
- 🔌 mysql-connector-python

The system provides:

- 📦 Product Management  
- 🏢 Supplier Management  
- 📊 Inventory Tracking  
- 🔁 Reorder Automation  
- 💰 Sales & Restock Analytics  
- 📈 Interactive Dashboard  

---

---

# 🗺️ Database Architecture (ER Diagram)

Below is the Entity Relationship Diagram representing the database structure of the Inventory Management System.

![Inventory ER Diagram](assets/er_diagram.png)

---

## 🔎 Relationship Explanation

### 🏢 suppliers
- Primary Key: `supplier_id`
- One supplier can supply multiple products.
- Connected to:
  - `products`
  - `shipments`

---

### 📦 products
- Primary Key: `product_id`
- Foreign Key: `supplier_id`
- One product:
  - Can have multiple shipments
  - Can have multiple stock entries
  - Can have multiple reorders

---

### 🚚 shipments
- Primary Key: `shipment_id`
- Foreign Keys:
  - `product_id`
  - `supplier_id`
- Records incoming stock from suppliers.

---

### 📊 stock_entries
- Primary Key: `entry_id`
- Foreign Key: `product_id`
- Tracks:
  - Sales (negative quantity)
  - Restocks (positive quantity)

---

### 🔁 reorders
- Primary Key: `reorder_id`
- Foreign Key: `product_id`
- Tracks reorder lifecycle:
  - Ordered
  - Received

---

## 🔗 Relationship Summary

- **One Supplier → Many Products**
- **One Supplier → Many Shipments**
- **One Product → Many Shipments**
- **One Product → Many Stock Entries**
- **One Product → Many Reorders**

This relational structure ensures:

✔ Data consistency  
✔ Referential integrity  
✔ Transaction-safe inventory updates  
✔ Scalable design  

---