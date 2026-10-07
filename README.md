# 📝 FastAPI Todo App

## 📌 Project Overview

FastAPI Todo App is a backend application for managing
Todo tasks through RESTful APIs.

The project allows users to create, view, update, and delete
Todo tasks while using a database for persistent data storage.

---


## 🛠️ Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication
- REST API

---

## ✨ Main Features

- 📝 Create Todo tasks
- 📋 View Todo tasks
- ✏️ Update Todo tasks
- 🗑️ Delete Todo tasks
- 🔐 User authentication
- 🔑 JWT-based authentication
- 🗄️ Database integration
- 🔄 Database migrations using Alembic
- 📚 Automatic Swagger API documentation
- 🧪 API testing

---

## 📦 Dependencies

The project dependencies are listed in:

`requirements.txt`

Main technologies and packages include:

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL database driver
- JWT authentication libraries

---

## 🚀 Run Locally

Follow these steps to run the project locally.

1. Clone the repository:
   git clone https://github.com/farhancoded/fastapi-todoapp.git
   cd fastapi-todoapp

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:

   Windows:
   venv\Scripts\activate

   Linux/macOS:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create a `.env` file and configure the environment variables:
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256

6. Run database migrations:
   alembic upgrade head

7. Start the FastAPI server:
   uvicorn main:app --reload

8. Open the API documentation:
   http://127.0.0.1:8000/docs

## 🌐 Live Demo


Render live link:https://fastapi-todoapp-4mbv.onrender.com/docs
