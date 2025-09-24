# 🎓 ScrapeData API

A FastAPI-based project for managing **Students, Teachers, Courses, Enrollments** and importing **Scraped Resources** from JSON.

---

## 🚀 Features
- Student CRUD (Create, Read, Update, Delete)
- Teacher CRUD
- Course CRUD
- Enrollment system (student → course)
- Import external scraped data from `samples/scraped.json`
- PostgreSQL database with SQLAlchemy ORM
- Interactive API docs (Swagger & Redoc)

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Uvicorn](https://www.uvicorn.org/)

---

## ⚙️ Installation

1️⃣ Clone the repo:
```bash
git clone https://github.com/wahidrana2108/scrapeData.git
cd scrapeData
````

2️⃣ Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

4️⃣ Set up PostgreSQL and update `DATABASE_URL` inside `database.py`:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/scrapedb"
```

5️⃣ Run migrations (if using Alembic) or create tables:

```bash
alembic upgrade head
```

6️⃣ Start server:

```bash
uvicorn main:app --reload
```

---

## 📜 API Docs

* Swagger UI 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Redoc 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📂 Project Structure

```
scrapeData/
│── main.py
│── models.py
│── schemas.py
│── database.py
│── routes.py
│── samples/
│   └── scraped.json
│── docs/
│   └── api_documentation.md
│── README.md
```

---

## 🧪 Testing

```bash
pytest
```

---

## 📥 Import Scraped Data

Keep your scraped JSON file in `samples/scraped.json` then call:

```http
POST /import/scraped
```

to insert into the database.

````

---

## 📄 `docs/api_documentation.md`

```markdown
# 📑 API Documentation

All endpoints are prefixed with:  
`http://127.0.0.1:8000/`

---

## 🔹 Students

### ➕ Create Student
`POST /students`
```json
{ "name": "John Doe", "email": "john@example.com" }
````

### 📜 Get All Students

`GET /students`

### 📌 Get Student by ID

`GET /students/{id}`

### ✏️ Update Student

`PUT /students/{id}`

### ❌ Delete Student

`DELETE /students/{id}`

---

## 🔹 Teachers

### ➕ Create Teacher

`POST /teachers`

```json
{ "name": "Alice Smith", "email": "alice@example.com" }
```

### 📜 Get All Teachers

`GET /teachers`

### 📌 Get Teacher by ID

`GET /teachers/{id}`

### ✏️ Update Teacher

`PUT /teachers/{id}`

### ❌ Delete Teacher

`DELETE /teachers/{id}`

---

## 🔹 Courses

### ➕ Create Course

`POST /courses`

```json
{
  "title": "Math 101",
  "description": "Basic Math Course",
  "capacity": 2,
  "teacher_id": 1
}
```

### 📜 Get All Courses

`GET /courses`

### 📌 Get Course by ID

`GET /courses/{id}`

### ✏️ Update Course

`PUT /courses/{id}`

### ❌ Delete Course

`DELETE /courses/{id}`

---

## 🔹 Enrollments

### ➕ Enroll Student

`POST /enrollments`

```json
{ "student_id": 1, "course_id": 1 }
```

### 📜 Get All Enrollments

`GET /enrollments`

### 📌 Get Enrollment by ID

`GET /enrollments/{id}`

### ✏️ Update Enrollment

`PUT /enrollments/{id}`

### ❌ Delete Enrollment

`DELETE /enrollments/{id}`

---

## 🔹 Scraped Resources

### 📜 Get Scraped Resources

`GET /scraped_resources`

**Example Response**

```json
[
  {
    "id": 1,
    "title": "Sample Book",
    "url": "http://example.com/book",
    "category": "Books",
    "price": "20 USD"
  }
]
```

---

### 📥 Import Scraped Data

`POST /import/scraped`

👉 This will read from `samples/scraped.json` and insert into DB.

**Response**

```json
{ "message": "Scraped data imported successfully" }
```

```