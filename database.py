import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS college (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS program (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            college TEXT NOT NULL,
            FOREIGN KEY (college) REFERENCES college(code) ON UPDATE CASCADE ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS student (
            id TEXT PRIMARY KEY,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            course TEXT NOT NULL,
            year INTEGER NOT NULL,
            gender TEXT NOT NULL,
            FOREIGN KEY (course) REFERENCES program(code) ON UPDATE CASCADE ON DELETE RESTRICT
        );

        CREATE INDEX IF NOT EXISTS idx_student_course ON student(course);
        CREATE INDEX IF NOT EXISTS idx_student_lastname ON student(lastname);
        CREATE INDEX IF NOT EXISTS idx_program_college ON program(college);
    """)

    conn.commit()
    conn.close()

# ─── College CRUD ────────────────────────────────────────────────────────────

def college_list(search="", sort_col="code", sort_dir="ASC", page=1, per_page=20):
    conn = get_connection()
    c = conn.cursor()
    allowed_cols = {"code", "name"}
    col = sort_col if sort_col in allowed_cols else "code"
    direction = "DESC" if sort_dir == "DESC" else "ASC"
    like = f"%{search}%"
    offset = (page - 1) * per_page
    c.execute(f"""
        SELECT code, name,
               (SELECT COUNT(*) FROM program WHERE college = college.code) AS program_count
        FROM college
        WHERE code LIKE ? OR name LIKE ?
        ORDER BY {col} {direction}
        LIMIT ? OFFSET ?
    """, (like, like, per_page, offset))
    rows = [dict(r) for r in c.fetchall()]
    c.execute("SELECT COUNT(*) FROM college WHERE code LIKE ? OR name LIKE ?", (like, like))
    total = c.fetchone()[0]
    conn.close()
    return rows, total

def college_get(code):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM college WHERE code = ?", (code,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def college_create(code, name):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO college (code, name) VALUES (?, ?)", (code.upper(), name))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def college_update(old_code, code, name):
    conn = get_connection()
    try:
        conn.execute("UPDATE college SET code=?, name=? WHERE code=?", (code.upper(), name, old_code))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def college_delete(code):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM college WHERE code=?", (code,))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, "Cannot delete: programs are assigned to this college."
    finally:
        conn.close()

def college_all():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT code, name FROM college ORDER BY code")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ─── Program CRUD ─────────────────────────────────────────────────────────────

def program_list(search="", sort_col="code", sort_dir="ASC", page=1, per_page=20):
    conn = get_connection()
    c = conn.cursor()
    allowed_cols = {"code", "name", "college"}
    col = sort_col if sort_col in allowed_cols else "code"
    direction = "DESC" if sort_dir == "DESC" else "ASC"
    like = f"%{search}%"
    offset = (page - 1) * per_page
    c.execute(f"""
        SELECT p.code, p.name, p.college, cl.name AS college_name,
               (SELECT COUNT(*) FROM student WHERE course = p.code) AS student_count
        FROM program p
        LEFT JOIN college cl ON cl.code = p.college
        WHERE p.code LIKE ? OR p.name LIKE ? OR p.college LIKE ?
        ORDER BY p.{col} {direction}
        LIMIT ? OFFSET ?
    """, (like, like, like, per_page, offset))
    rows = [dict(r) for r in c.fetchall()]
    c.execute("SELECT COUNT(*) FROM program p WHERE p.code LIKE ? OR p.name LIKE ? OR p.college LIKE ?", (like, like, like))
    total = c.fetchone()[0]
    conn.close()
    return rows, total

def program_get(code):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM program WHERE code=?", (code,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def program_create(code, name, college):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO program (code, name, college) VALUES (?, ?, ?)", (code.upper(), name, college))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def program_update(old_code, code, name, college):
    conn = get_connection()
    try:
        conn.execute("UPDATE program SET code=?, name=?, college=? WHERE code=?", (code.upper(), name, college, old_code))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def program_delete(code):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM program WHERE code=?", (code,))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, "Cannot delete: students are enrolled in this program."
    finally:
        conn.close()

def program_all():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT code, name FROM program ORDER BY code")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

# ─── Student CRUD ─────────────────────────────────────────────────────────────

def student_list(search="", sort_col="id", sort_dir="ASC", page=1, per_page=20):
    conn = get_connection()
    c = conn.cursor()
    allowed_cols = {"id", "firstname", "lastname", "course", "year", "gender"}
    col = sort_col if sort_col in allowed_cols else "id"
    direction = "DESC" if sort_dir == "DESC" else "ASC"
    like = f"%{search}%"
    offset = (page - 1) * per_page
    c.execute(f"""
        SELECT s.id, s.firstname, s.lastname, s.course, s.year, s.gender,
               p.name AS program_name
        FROM student s
        LEFT JOIN program p ON p.code = s.course
        WHERE s.id LIKE ? OR s.firstname LIKE ? OR s.lastname LIKE ?
              OR s.course LIKE ? OR CAST(s.year AS TEXT) LIKE ?
        ORDER BY s.{col} {direction}
        LIMIT ? OFFSET ?
    """, (like, like, like, like, like, per_page, offset))
    rows = [dict(r) for r in c.fetchall()]
    c.execute("""
        SELECT COUNT(*) FROM student s
        WHERE s.id LIKE ? OR s.firstname LIKE ? OR s.lastname LIKE ?
              OR s.course LIKE ? OR CAST(s.year AS TEXT) LIKE ?
    """, (like, like, like, like, like))
    total = c.fetchone()[0]
    conn.close()
    return rows, total

def student_get(sid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT s.*, p.name AS program_name, cl.name AS college_name
        FROM student s
        LEFT JOIN program p ON p.code = s.course
        LEFT JOIN college cl ON cl.code = p.college
        WHERE s.id = ?
    """, (sid,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def student_create(sid, firstname, lastname, course, year, gender):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO student (id, firstname, lastname, course, year, gender) VALUES (?, ?, ?, ?, ?, ?)",
            (sid, firstname, lastname, course, year, gender)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def student_update(old_id, sid, firstname, lastname, course, year, gender):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE student SET id=?, firstname=?, lastname=?, course=?, year=?, gender=? WHERE id=?",
            (sid, firstname, lastname, course, year, gender, old_id)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

def student_delete(sid):
    conn = get_connection()
    conn.execute("DELETE FROM student WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    return True, None

def get_stats():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM student")
    students = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM program")
    programs = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM college")
    colleges = c.fetchone()[0]
    conn.close()
    return students, programs, colleges
