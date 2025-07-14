# 🛒 MERN E-Commerce Website
A modern, full-featured e-commerce platform built with the MERN stack. Includes a user-facing store and a powerful admin dashboard for product, order, and user management.

---

## ✨ Features

### 🌟 User Frontend
- 🔒 **Authentication**: Register, login, and manage your profile securely
- 🛍️ **Product Catalog**: Browse, search, and filter products by category, type, and more
- 🛒 **Shopping Cart**: Add, update, and remove products from your cart
- 💳 **Checkout & Payments**: Place orders and pay securely (Stripe integration)
- 📦 **Order Tracking**: View your order history and track delivery status

### ⚙️ Admin Dashboard
- 🛠️ **Product Management**: Add, update (including inventory count), or delete products
- 📂 **Category Management**: Organize products by category and subcategory
- 📑 **Order Management**: View, process, and update all user orders
- 👥 **User Management**: Manage users and admin access

---

## 🗂️ Folder Structure

```plaintext
/
|-- admin/            # React.js admin dashboard
|-- backend/          # Node.js/Express backend API
|-- frontend/         # React.js user frontend
|-- .gitignore        # Git ignore rules
|-- README.md         # Project documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/en)
- [NPM](https://www.npmjs.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/GGajanan1/E-Commerce-Main.git
cd E-Commerce-Main
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Set Up Environment Variables

<details>
<summary><code>/admin/.env</code></summary>

```env
VITE_BACKEND_URL = "http://localhost:4000"
```
</details>

<details>
<summary><code>/backend/.env</code></summary>

```env
MONGODB_URI = <your_mongodb_uri>
CLOUDINARY_API_KEY = <your_cloudinary_key>
CLOUDINARY_SECRET_KEY = <your_cloudinary_secret>
CLOUDINARY_CLOUD_NAME = <your_cloudinary_cloud>
JWT_SECRET = <your_jwt_secret>
ADMIN_EMAIL = "admin@clicknshop.com" # For testing only
ADMIN_PASSWORD = "admin@123" # For testing only
```
</details>

<details>
<summary><code>/frontend/.env</code></summary>

```env
VITE_BACKEND_URL = "http://localhost:4000"
```
</details>

---

### 5. Running the Project

#### Admin Dashboard
```bash
cd admin
npm run dev
```
Visit: [http://localhost:5174](http://localhost:5174)

#### Backend API
```bash
cd backend
npm run server
```
Visit: [http://localhost:4000](http://localhost:4000)

#### User Frontend
```bash
cd frontend
npm run dev
```
Visit: [http://localhost:5173](http://localhost:5173)

---

## 📝 Notes
- Replace all placeholder values in `.env` files with your actual credentials.
- Admin credentials are set in `/backend/.env`.
- Product inventory is managed via the `count` field.
- Orders automatically decrease product inventory.
- Admin can edit product details and inventory from the dashboard.

---

## 📬 Feedback & Contributions
Pull requests and issues are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License.
