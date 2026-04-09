# StudentInfoSystem — RDBMS Edition

A modern Student Information System using **Python + SQLite + PyQt6**.

## Requirements

- Python 3.10 or higher (https://python.org)
- pip (comes with Python)

## Quick Start (Windows)

Open **Command Prompt** or **PowerShell** in this folder, then:

```
# 1. Install the GUI library (only needed once)
pip install PyQt6

# 2. Run the app
python main.py
```

That's it. The database file (`students.db`) is created automatically on first run,
and 5,200 students are pre-seeded.

---

## Project Structure

```
StudentInfoSystem/
├── main.py        ← Run this to launch the app
├── database.py    ← All SQL queries (CRUD for student/program/college)
├── dialogs.py     ← Add/Edit popup windows
├── seed.py        ← Generates 5200 students + 30 programs on first run
├── students.db    ← Created automatically (SQLite database file)
└── README.md      ← This file
```

---

## Database Schema

```sql
college  (code PK, name)
program  (code PK, name, college FK→college)
student  (id PK "YYYY-NNNN", firstname, lastname, course FK→program, year, gender)
```

---

## Features

| Feature        | Details |
|----------------|---------|
| CRUD           | Create, Read, Update, Delete for Students, Programs, Colleges |
| List           | Paginated table view |
| Search         | Real-time search across all relevant fields |
| Sort           | Click any column header to sort asc/desc |
| Pagination     | 10 / 25 / 50 / 100 rows per page, smart page buttons |
| Pre-seeded     | 7 colleges, 40 programs, 5200 students |
| Themes         | Night and Day Mode for preference |

---

## SQL Concepts Used

- **DDL**: `CREATE TABLE`, `CREATE INDEX`
- **DML**: `INSERT`, `UPDATE`, `DELETE`, `SELECT`
- **Joins**: `LEFT JOIN` to pull program/college names into student list
- **Aggregate**: `COUNT(*)` for student/program counts
- **Filtering**: `WHERE ... LIKE ?` for search
- **Ordering**: `ORDER BY col ASC/DESC`
- **Pagination**: `LIMIT ? OFFSET ?`
- **Foreign Keys**: referential integrity enforced at DB level
- **Parameterized queries**: all queries use `?` placeholders (prevents SQL injection)
