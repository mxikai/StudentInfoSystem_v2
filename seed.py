"""
seed.py — populates the DB with MSU-IIT colleges, undergraduate programs, and 5200 students.
"""
import random
from database import init_db, get_connection

COLLEGES = [
    ("CCS",  "College of Computer Studies"),
    ("COE",  "College of Engineering"),
    ("CED",  "College of Education"),
    ("CEBA",  "College of Economics, Business, and Accountancy"),
    ("CASS", "College of Arts and Social Sciences"),
    ("CSM",  "College of Science and Mathematics"),
    ("CHS",  "College of Health Sciences"),
]

PROGRAMS = [
    # CCS
    ("BSCS",    "Bachelor of Science in Computer Science",                        "CCS"),
    ("BSIT",    "Bachelor of Science in Information Technology",                  "CCS"),
    ("BSIS",    "Bachelor of Science in Information Systems",                     "CCS"),
    ("BSCA",    "Bachelor of Science in Computer Applications",                   "CCS"),
    # COE
    ("BSCE",    "Bachelor of Science in Civil Engineering",                       "COE"),
    ("BSEE",    "Bachelor of Science in Electrical Engineering",                  "COE"),
    ("BSECE",   "Bachelor of Science in Electronics Engineering",                 "COE"),
    ("BSCPE",   "Bachelor of Science in Computer Engineering",                    "COE"),
    ("BSME",    "Bachelor of Science in Mechanical Engineering",                  "COE"),
    ("BSCHE",   "Bachelor of Science in Chemical Engineering",                    "COE"),
    ("BSCERE",  "Bachelor of Science in Ceramic Engineering",                     "COE"),
    ("BSMETE",  "Bachelor of Science in Metallurgical Engineering",               "COE"),
    ("BSEME",   "Bachelor of Science in Mining Engineering",                      "COE"),
    ("BSENE",   "Bachelor of Science in Environmental Engineering",               "COE"),
    ("BSIAM",   "Bachelor of Science in Industrial Automation and Mechatronics",  "COE"),
    # CED
    ("BEED",    "Bachelor of Elementary Education",                               "CED"),
    ("BSED",    "Bachelor of Secondary Education",                                "CED"),
    ("BTLED",   "Bachelor of Technology and Livelihood Education",                "CED"),
    ("BTVTED",  "Bachelor of Technical-Vocational Teacher Education",             "CED"),
    ("BPED",    "Bachelor of Physical Education",                                 "CED"),
    # CEBA
    ("BSA",     "Bachelor of Science in Accountancy",                             "CEBA"),
    ("BSBA",    "Bachelor of Science in Business Administration",                 "CEBA"),
    ("BSHM",    "Bachelor of Science in Hospitality Management",                  "CEBA"),
    ("BSECON",  "Bachelor of Science in Economics",                               "CEBA"),
    ("BSENTREP","Bachelor of Science in Entrepreneurship",                        "CEBA"),
    # CASS
    ("BAELS",   "Bachelor of Arts in English Language Studies",                   "CASS"),
    ("BALCS",   "Bachelor of Arts in Literary and Cultural Studies",              "CASS"),
    ("BAHIS",   "Bachelor of Arts in History",                                    "CASS"),
    ("BAPOLSCI",   "Bachelor of Arts in Political Science",                          "CASS"),
    ("BSPHIL",  "Bachelor of Science in Philosophy - Applied Ethics",             "CASS"),
    ("BAPSYCH", "Bachelor of Arts in Psychology",                                 "CASS"),
    ("BSPSYCH", "Bachelor of Science in Psychology",                              "CASS"),
    ("BASOC",   "Bachelor of Arts in Sociology",                                  "CASS"),
    ("BAFIL",   "Batsilyer ng Sining sa Filipino",                                "CASS"),
    # CSM
    ("BSBIO",   "Bachelor of Science in Biology",                                 "CSM"),
    ("BSCHEM",  "Bachelor of Science in Chemistry",                               "CSM"),
    ("BSMATH",  "Bachelor of Science in Mathematics",                             "CSM"),
    ("BSSTAT",  "Bachelor of Science in Statistics",                              "CSM"),
    ("BSPHYSICS",  "Bachelor of Science in Physics",                                 "CSM"),
    ("BSMARINEBIO","Bachelor of Science in Marine Biology",                          "CSM"),
    # CHS
    ("BSN",     "Bachelor of Science in Nursing",                                 "CHS"),
]

FIRST_NAMES_M = [
    "James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles",
    "Christopher","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua",
    "Kenneth","Kevin","Brian","George","Timothy","Ronald","Edward","Jason","Jeffrey","Ryan",
    "Jacob","Gary","Nicholas","Eric","Jonathan","Stephen","Larry","Justin","Scott","Brandon",
    "Benjamin","Samuel","Raymond","Gregory","Frank","Alexander","Patrick","Jack","Dennis","Jerry",
    "Juan","Carlos","Luis","Miguel","Marco","Jose","Angelo","Jerome","Renz","Jayson",
    "Noel","Aldrin","Rommel","Ariel","Ronaldo","Dante","Erwin","Rodel","Gerry","Lester",
    "Marvin","Nico","Kurt","Lance","Clark","Neil","Ivan","Leon","Adrian","Cyril",
]

FIRST_NAMES_F = [
    "Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen",
    "Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna",
    "Michelle","Carol","Amanda","Melissa","Deborah","Stephanie","Rebecca","Sharon","Laura","Cynthia",
    "Kathleen","Amy","Angela","Shirley","Anna","Brenda","Pamela","Emma","Nicole","Helen",
    "Maria","Liza","Jasmine","Princess","Angel","Christine","Grace","Ana","Rosario","Cynthia",
    "Maricel","Hazel","Faith","Hope","Joy","Lovely","Marites","Rowena","Sheila","Trisha",
    "Vanessa","Kathrina","Rhea","Leilani","Cristine","Pia","Nina","Lea","Aira","Bea",
]

LAST_NAMES = [
    "Santos","Reyes","Cruz","Bautista","Ocampo","Garcia","Mendoza","Torres","Flores","Ramos",
    "Aquino","Diaz","Lopez","Morales","Castillo","Rivera","Gonzales","Villanueva","Rodriguez","Perez",
    "De Leon","Dela Cruz","Ramirez","Navarro","Valdez","Fernandez","Pascual","Herrera","Castro","Medina",
    "Soriano","Aguilar","Luna","Lim","Tan","Go","Sy","Ong","Co","Chua",
    "Domingo","Delos Santos","Dela Torre","Espiritu","Mercado","Salazar","Santiago","Tolentino","Vega","Vergara",
    "Abella","Ablaza","Abad","Acosta","Adriano","Alcantara","Aldana","Alfonso","Almario","Alvarado",
    "Alvarez","Andres","Angeles","Antonio","Aranda","Arce","Arcega","Arenas","Arias","Arroyo",
    "Asuncion","Atienza","Austria","Avila","Bacalso","Bacani","Balboa","Balderas","Bello","Bernabe",
    "Bernal","Borja","Briones","Buenaventura","Caballero","Cabrera","Campos","Capuno","Cariaga","Catacutan",
    "Cervantes","Claudio","Clemente","Colon","Corpuz","Cortez","Cunanan","Dacanay","Dalisay","David",
    "De Guzman","De Jesus","De Villa","Defensor","Del Rosario","Dela Paz","Delgado","Dizon","Duarte","Dumlao",
    "Enriquez","Escoto","Esguerra","Espino","Estrada","Evangelista","Fajardo","Faustino","Felipe","Ferrer",
    "Francisco","Fuentes","Galang","Galvez","Geronda","Gloria","Gomez","Guerrero","Guevarra","Guillermo",
    "Gutierrez","Guzman","Hernandez","Ilagan","Ilustre","Imperial","Jimenez","Lagrimas","Laserna","Laurel",
]

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

    print("Seeding 5000 students...")
    program_codes = [p[0] for p in PROGRAMS]
    used_ids = set()
    students = []
    for _ in range(5000):
        while True:
            yr  = random.randint(2018, 2025)
            seq = random.randint(1, 3000)
            sid = f"{yr}-{seq:04d}"
            if sid not in used_ids:
                used_ids.add(sid)
                break
        gender    = random.choice(["Male", "Female"])
        firstname = random.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
        lastname  = random.choice(LAST_NAMES)
        course    = random.choice(program_codes)
        year      = random.choice([1, 2, 3, 4])
        students.append((sid, firstname, lastname, course, year, gender))

    conn.executemany(
        "INSERT OR IGNORE INTO student (id, firstname, lastname, course, year, gender) VALUES (?,?,?,?,?,?)",
        students,
    )
    conn.commit()
    conn.close()
    print(f"Done! {len(students)} students inserted.")

if __name__ == "__main__":
    seed()
