"""
seed.py — populates the database with colleges, programs, and 5000+ students.
Run once: python seed.py
"""

import random
import sqlite3
from database import init_db, get_connection

COLLEGES = [
    ("CCS",  "College of Computer Studies"),
    ("COE",  "College of Engineering"),
    ("CED",  "College of Education"),
    ("CBA",  "College of Business Administration"),
    ("CASS", "College of Arts and Social Sciences"),
    ("CN",   "College of Nursing"),
    ("CP",   "College of Pharmacy"),
    ("CAFA", "College of Architecture and Fine Arts"),
    ("CL",   "College of Law"),
    ("CM",   "College of Medicine"),
]

PROGRAMS = [
    # CCS
    ("BSCS",   "Bachelor of Science in Computer Science",          "CCS"),
    ("BSIT",   "Bachelor of Science in Information Technology",    "CCS"),
    ("BSIS",   "Bachelor of Science in Information Systems",       "CCS"),
    ("BSEMC",  "Bachelor of Science in Entertainment & Multimedia Computing", "CCS"),
    # COE
    ("BSCE",   "Bachelor of Science in Civil Engineering",         "COE"),
    ("BSEE",   "Bachelor of Science in Electrical Engineering",    "COE"),
    ("BSME",   "Bachelor of Science in Mechanical Engineering",    "COE"),
    ("BSECE",  "Bachelor of Science in Electronics Engineering",   "COE"),
    ("BSIE",   "Bachelor of Science in Industrial Engineering",    "COE"),
    ("BSCHE",  "Bachelor of Science in Chemical Engineering",      "COE"),
    # CED
    ("BEED",   "Bachelor of Elementary Education",                 "CED"),
    ("BSED",   "Bachelor of Secondary Education",                  "CED"),
    ("BSPE",   "Bachelor of Science in Physical Education",        "CED"),
    # CBA
    ("BSBA",   "Bachelor of Science in Business Administration",   "CBA"),
    ("BSACCO", "Bachelor of Science in Accountancy",               "CBA"),
    ("BSFM",   "Bachelor of Science in Financial Management",      "CBA"),
    ("BSHM",   "Bachelor of Science in Hospitality Management",    "CBA"),
    ("BSTM",   "Bachelor of Science in Tourism Management",        "CBA"),
    # CASS
    ("ABCOMM", "Bachelor of Arts in Communication",                "CASS"),
    ("ABPSY",  "Bachelor of Arts in Psychology",                   "CASS"),
    ("ABSOC",  "Bachelor of Arts in Sociology",                    "CASS"),
    ("ABPOL",  "Bachelor of Arts in Political Science",            "CASS"),
    ("ABFIL",  "Bachelor of Arts in Filipino",                     "CASS"),
    # CN
    ("BSN",    "Bachelor of Science in Nursing",                   "CN"),
    # CP
    ("BSPHAR", "Bachelor of Science in Pharmacy",                  "CP"),
    # CAFA
    ("BSARCH", "Bachelor of Science in Architecture",              "CAFA"),
    ("BSID",   "Bachelor of Science in Interior Design",           "CAFA"),
    ("BFA",    "Bachelor of Fine Arts",                            "CAFA"),
    # CL
    ("JD",     "Juris Doctor",                                     "CL"),
    # CM
    ("MD",     "Doctor of Medicine",                               "CM"),
]

FIRST_NAMES_M = [
    "James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles",
    "Christopher","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua",
    "Kenneth","Kevin","Brian","George","Timothy","Ronald","Edward","Jason","Jeffrey","Ryan",
    "Jacob","Gary","Nicholas","Eric","Jonathan","Stephen","Larry","Justin","Scott","Brandon",
    "Benjamin","Samuel","Raymond","Gregory","Frank","Alexander","Patrick","Jack","Dennis","Jerry",
    "Juan","Carlos","Luis","Miguel","Marco","Jose","Angelo","Jerome","Renz","Jayson",
    "Mark","Noel","Aldrin","Rommel","Ariel","Ronaldo","Dante","Erwin","Rodel","Gerry",
    "Lester","Marvin","Nico","Kurt","Lance","Clark","Neil","Ivan","Leon","Adrian",
]

FIRST_NAMES_F = [
    "Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen",
    "Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna",
    "Michelle","Carol","Amanda","Melissa","Deborah","Stephanie","Rebecca","Sharon","Laura","Cynthia",
    "Kathleen","Amy","Angela","Shirley","Anna","Brenda","Pamela","Emma","Nicole","Helen",
    "Maria","Liza","Jasmine","Princess","Angel","Christine","Grace","Ana","Rosario","Cynthia",
    "Maricel","Hazel","Faith","Hope","Joy","Lovely","Marites","Natividad","Rowena","Sheila",
    "Trisha","Vanessa","Kathrina","Rhea","Leilani","Cristine","Pia","Nina","Lea","Aira",
]

LAST_NAMES = [
    "Santos","Reyes","Cruz","Bautista","Ocampo","Garcia","Mendoza","Torres","Flores","Ramos",
    "Aquino","Diaz","Lopez","Morales","Castillo","Rivera","Gonzales","Villanueva","Rodriguez","Perez",
    "De Leon","Dela Cruz","Ramirez","Navarro","Valdez","Fernandez","Pascual","Herrera","Castro","Medina",
    "Soriano","Aguilar","Luna","Lim","Tan","Go","Sy","Ong","Co","Chua",
    "Domingo","Delos Santos","Dela Torre","Espiritu","Mercado","Salazar","Santiago","Tolentino","Vega","Vergara",
    "Abella","Ablaza","Abad","Abrera","Acosta","Adriano","Alcantara","Aldana","Alfonso","Alipio",
    "Almario","Alvarado","Alvarez","Andres","Angeles","Antonio","Aranda","Arce","Arcega","Arceo",
    "Arenas","Arguelles","Arias","Arizala","Arroyo","Arteche","Asuncion","Atienza","Austria","Avila",
    "Bacalso","Bacani","Bacolod","Baguio","Balboa","Balderas","Baldos","Bello","Bernabe","Bernal",
    "Borja","Briones","Buenaventura","Caballero","Cabanlit","Cabrera","Cabrido","Cagadas","Caguioa","Cahilig",
]

GENDERS = ["Male", "Female"]
YEARS = [1, 2, 3, 4]


def already_seeded(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM student")
    return c.fetchone()[0] >= 100


def seed():
    init_db()
    conn = get_connection()

    if already_seeded(conn):
        print("Database already seeded. Skipping.")
        conn.close()
        return

    print("Seeding colleges...")
    conn.executemany("INSERT OR IGNORE INTO college (code, name) VALUES (?, ?)", COLLEGES)

    print("Seeding programs...")
    conn.executemany("INSERT OR IGNORE INTO program (code, name, college) VALUES (?, ?, ?)", PROGRAMS)

    print("Seeding 5200 students...")
    program_codes = [p[0] for p in PROGRAMS]
    used_ids = set()
    students = []

    year_range = range(2018, 2026)

    for _ in range(5200):
        # Generate unique ID: YYYY-NNNN
        while True:
            yr = random.choice(year_range)
            seq = random.randint(1, 9999)
            sid = f"{yr}-{seq:04d}"
            if sid not in used_ids:
                used_ids.add(sid)
                break

        gender = random.choice(GENDERS)
        if gender == "Male":
            firstname = random.choice(FIRST_NAMES_M)
        else:
            firstname = random.choice(FIRST_NAMES_F)

        lastname  = random.choice(LAST_NAMES)
        course    = random.choice(program_codes)
        year      = random.choice(YEARS)

        students.append((sid, firstname, lastname, course, year, gender))

    conn.executemany(
        "INSERT OR IGNORE INTO student (id, firstname, lastname, course, year, gender) VALUES (?,?,?,?,?,?)",
        students
    )

    conn.commit()
    conn.close()
    print("Done! 5200 students inserted.")


if __name__ == "__main__":
    seed()
