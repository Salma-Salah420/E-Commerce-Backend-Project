# E-Commerce Backend Project 🚀

A scalable RESTful API backend system for an online e-commerce platform beautifully unified using **FastAPI** and **SQLAlchemy**.

## 🚀 Quick Start & Testing

Follow these quick steps to get the app running and test it using the built-in Frontend Dashboard.

### 1. Install Dependencies
Ensure you have `pip` installed, then run the following in the project root:
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
Run the FastAPI development server:
```bash
cd app
uvicorn main:app --reload
```
*(The database `ecommerce.db` will be dynamically generated in the `app/` folder upon first run)*

### 3. Test Using the Dashboard!
We have bundled a sleek HTML frontend right into the project so you can visually test everything seamlessly.
- Open the `frontend/index.html` file directly in your web browser (Chrome, Edge, Firefox).
- The dashboard validates your token and natively allows you to visually test:
  - Registering and logging in safely via tokens.
  - Adding product categories (Admin Only)
  - Submitting new products assigned to your categories (Admin Only)

> [!TIP]
> **Testing Admin Accounts:** If you want to log in as an administrator to bypass the `403 Forbidden` limits on adding products and categories, simply ensure your email address contains the word "**admin**" when you register (e.g. *admin_test@example.com*). The system will automatically upgrade your privileges!

### 4. Advanced API Documentation
If you want to manually test raw API endpoints, you can access the automatically generated interactive documentation while the server is running:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc UI:** `http://localhost:8000/redoc`

---

## Overview 
This project expertly combined separate Authentication & Users logic seamlessly alongside Categories & Products logic. Instead of scattered architecture, it utilizes a deeply integrated **SQLite database**, robust JSON Pydantic serialization models (fully backward-compatible with legacy database strings via `Optional`), and native frontend DOM connections.

## Features Included
- **User Authentication:** Token-based secure registration and login (using JWT and pure `bcrypt`).
- **Users Management:** Protected `/users/me` endpoint.
- **Product Management:** Full CRUD actions, advanced filtering, backwards-compatibility error handling, and python-native schemas.
- **Category Management:** Full CRUD actions for organizing products easily.

## Tech Stack
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy (Using SQLite database)
- **Data Validation:** Pydantic
- **Security:** Pure `bcrypt` (secure hashing) & `pyjwt` (Authentication Tokens)
