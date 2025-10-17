# songa_read
# 📚 Library Management System API

A full-featured RESTful API for managing a digital library — built with **Django REST Framework**.  
It supports **role-based access**, **book management**, and **borrowing/returning workflows** with JWT authentication.

---

## 🚀 Features

✅ **User Authentication**
- JWT-based login and registration.
- Role-based access control: `Admin`, `Librarian`, `Member`.

✅ **Books Management**
- CRUD operations for books (Admin/Librarian only).
- Search and filter by title, author, or ISBN.
- Auto-tracking of available copies.

✅ **Borrowing System**
- Members can borrow and return books.
- Automatic due date calculation.
- Fine calculation for overdue returns.
- Atomic updates using database transactions.

✅ **API Documentation**
- Built-in Swagger UI at `/api/docs/`.

✅ **Deployment Ready**
- Includes Dockerfile + docker-compose for easy deployment.
- PostgreSQL support.

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Django 5 + Django REST Framework |
| Authentication | SimpleJWT |
| Database | PostgreSQL / SQLite (for local dev) |
| API Docs | drf-yasg (Swagger UI) |
| Deployment | Docker / Render / Heroku |

---

## 📁 Project Structure

