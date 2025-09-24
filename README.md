# 📚 ScrapeData API

A FastAPI-based project for managing **students, teachers, courses, enrollments**, and **scraped resources**.  
It supports CRUD operations, enrollment rules (duplicate + capacity check), and importing scraped JSON data directly into the database.

---

## 🚀 Features
- Student, Teacher, Course, and Enrollment management
- Enrollment rules:
  - Prevent duplicate enrollments
  - Enforce course capacity
- Scraped resource import:
  - Import data from `samples/scraped.json` into database
- Auto table creation (no manual migrations needed)
- Interactive API docs at `/docs`

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **SQLite / PostgreSQL** (SQLite default for local dev)
- **Uvicorn** – ASGI server

---

## 📂 Project Structure
```

scrapeData/
│── api/
│   └── routes.py          # All API endpoints
│── models/
│   ├── base.py            # SQLAlchemy Base
│   ├── student.py
│   ├── teacher.py
│   ├── course.py
│   ├── enrollment.py
│   └── scraped.py
│── schemas/
│   ├── student\_schema.py
│   ├── teacher\_schema.py
│   ├── course\_schema.py
│   ├── enrollment\_schema.py
│   └── scraped\_schema.py
│── samples/
│   └── scraped.json       # Sample scraped data
│── main.py                # App entry point
│── database.py            # DB connection + Session
│── README.md

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/wahidrana2108/scrapeData.git
cd scrapeData
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run App

```bash
uvicorn main:app --reload
```

Server will start at 👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📑 API Endpoints

### 🔹 Students

* `POST /students` → Create student
* `GET /students` → List all students
* `GET /students/{id}` → Get student by ID
* `PUT /students/{id}` → Update student
* `DELETE /students/{id}` → Delete student

### 🔹 Teachers

* `POST /teachers`
* `GET /teachers`
* `GET /teachers/{id}`
* `PUT /teachers/{id}`
* `DELETE /teachers/{id}`

### 🔹 Courses

* `POST /courses`
* `GET /courses`
* `GET /courses/{id}`
* `PUT /courses/{id}`
* `DELETE /courses/{id}`

### 🔹 Enrollments

* `POST /enrollments` → Enroll student to course

  * Prevents duplicate enrollment
  * Respects course capacity
* `GET /enrollments`
* `DELETE /enrollments/{id}`

### 🔹 Scraped Resources

* `GET /scraped_resources` → List resources
* `POST /import/scraped` → Import data from `samples/scraped.json` into DB

---

## 🧪 Testing

You can explore the APIs at:

* Swagger UI 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Notes

* Tables auto-create on startup (no need for Alembic migration for now).
* If schema changes, delete `scrapeData.db` (SQLite file) and restart app.
* For production, switch DB from SQLite to PostgreSQL in `database.py`.

---

## 👨‍💻 Author

Developed by **Md. Wahiduzzaman** 

```
