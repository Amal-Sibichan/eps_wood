# EPS Wood Project

A Django-based multi-vendor e-commerce platform for buying and selling wood, plywood, veneers, and related products.
Demo:https://amalsibichan.pythonanywhere.com/

---

## 📌 Project Overview

EPS Wood Project is an online marketplace designed specifically for the wood and plywood industry. The system allows multiple sellers to list products while customers can browse, add products to cart, place orders, and track deliveries.

The platform supports:

* Wood sellers
* Plywood sellers
* Customers
* Admin management

---

# ✨ Features

## 👤 Customer Features

* User registration and login
* Browse wood and plywood products
* Product search and filtering
* View product images
* Add products to cart
* Remove items from cart
* Place orders
* Cash on Delivery / Card payment selection
* View order history
* Track item-wise order status
* Cancel orders

---

## 🪵 Owner Features

* Owner registration and login
* Add products
* Upload multiple product images
* Manage stock and pricing
* View incoming orders
* Update delivery status
* Manage product listings

---

## 🛠️ Admin Features

* Manage customers
* Manage sellers
* Monitor products
* Monitor orders
* Manage overall system

---

# 🧱 Technologies Used

* Python
* Django
* SQLite
* HTML
* CSS
* Bootstrap
* JavaScript
* WhiteNoise
* Gunicorn

---

# 🗂️ Project Structure

```text
EPS_WOOD_PROJECT/
│
├── eps_wood_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── eps_wood_app/
├── templates/
├── static/
├── media/
├── staticfiles/
├── manage.py
├── requirements.txt
├── runtime.txt
└── build.sh
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd EPS_WOOD_PROJECT
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv env
```

Activate environment:

### Windows

```bash
env\Scripts\activate
```

### Linux/Mac

```bash
source env/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Migrations

```bash
python manage.py migrate
```

---

## 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Run Development Server

```bash
python manage.py runserver
```

---

# 🚀 Deployment

The project is configured for deployment on Render.

### Build Command

```bash
./build.sh
```

### Start Command

```bash
gunicorn eps_wood_project.wsgi:application
```

---

# 🖼️ Product Image Handling

* Multiple images can be uploaded for a single product.
* Images are stored using a separate ProductImage model.
* Media files are handled using Django media settings.

---

# 🛒 Order Workflow

```text
Browse Products
      ↓
Add to Cart
      ↓
Payment Selection
      ↓
Place Order
      ↓
Owner Updates Status
      ↓
Customer Tracks Order
```

---

# 🔐 Authentication

The project uses a custom Django authentication model:

```python
AUTH_USER_MODEL = "eps_wood_app.Login"
```

---

# 📦 Main Modules

## Customer Module

Handles customer registration, cart management, ordering, and order tracking.

## Owner Module

Handles product management, order fulfillment, and delivery updates.

## Admin Module

Handles overall platform monitoring and management.

---

# 📚 Future Enhancements

* Online payment gateway integration
* Email notifications
* Product reviews and ratings
* Wishlist feature
* Real-time order tracking
* Cloud image storage
* AI-based product recommendations

---

# 👨‍💻 Developed By

Amal Sibichan

---

# 📄 License

This project is developed for educational and academic purposes.
