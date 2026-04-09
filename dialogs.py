"""
dialogs.py — CRUD dialogs + detail view popups for College, Program, Student
"""
import re
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QLabel,
    QFrame, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPen
import database as db

# ── Name validator: letters, spaces, hyphens only ────────────────────────────
NAME_RE = re.compile(r"^[A-Za-z\u00C0-\u024F\s\-]+$")

def valid_name(s):
    return bool(NAME_RE.match(s.strip())) if s.strip() else False

# ── helpers ───────────────────────────────────────────────────────────────────
def _primary_btn(text):
    b = QPushButton(text)
    b.setObjectName("primaryBtn")
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b

def _cancel_btn(dlg):
    b = QPushButton("Cancel")
    b.setObjectName("cancelBtn")
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.clicked.connect(dlg.reject)
    return b

def _btn_row(*btns):
    row = QHBoxLayout(); row.addStretch()
    for b in btns: row.addWidget(b)
    return row

# ════════════════════════════════════════════════════════════════════════════
#  DETAIL POPUP WIDGETS
# ════════════════════════════════════════════════════════════════════════════

class _CircleIcon(QWidget):
    """Draws the round icon shown in detail popups."""
    def __init__(self, text, size=80, parent=None):
        super().__init__(parent)
        self._text = text
        self.setFixedSize(size, size)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor("#6366f1"), 3))
        p.setBrush(QColor("#1e2237"))
        r = self.rect().adjusted(4, 4, -4, -4)
        p.drawEllipse(r)
        p.setPen(QColor("#e2e8f0"))
        f = QFont("Segoe UI", 13, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, self._text)
        p.end()


class CollegeDetailDialog(QDialog):
    def __init__(self, parent, row):
        super().__init__(parent)
        self.setWindowTitle("College Details")
        self.setFixedSize(380, 340)
        self.setStyleSheet(parent.styleSheet())
        lay = QVBoxLayout(self)
        lay.setContentsMargins(30, 30, 30, 24)
        lay.setSpacing(10)

        icon = _CircleIcon(row["code"])
        icon_row = QHBoxLayout(); icon_row.addStretch(); icon_row.addWidget(icon); icon_row.addStretch()
        lay.addLayout(icon_row)

        code_lbl = QLabel(row["code"])
        code_lbl.setObjectName("detailCode")
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(code_lbl)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep")
        lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def _row(label, val):
            lbl = QLabel(val or "—")
            lbl.setWordWrap(True)
            lbl.setObjectName("detailVal")
            form.addRow(QLabel(label), lbl)

        _row("College Name:", row["name"])
        _row("Programs:", str(row.get("program_count", "—")))
        lay.addLayout(form)
        lay.addStretch()

        close = _primary_btn("Close"); close.clicked.connect(self.accept)
        lay.addLayout(_btn_row(close))


class ProgramDetailDialog(QDialog):
    def __init__(self, parent, row):
        super().__init__(parent)
        self.setWindowTitle("Program Details")
        self.setFixedSize(420, 360)
        self.setStyleSheet(parent.styleSheet())
        lay = QVBoxLayout(self)
        lay.setContentsMargins(30, 30, 30, 24)
        lay.setSpacing(10)

        icon = _CircleIcon(row["code"][:4])
        icon_row = QHBoxLayout(); icon_row.addStretch(); icon_row.addWidget(icon); icon_row.addStretch()
        lay.addLayout(icon_row)

        code_lbl = QLabel(row["code"])
        code_lbl.setObjectName("detailCode")
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(code_lbl)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep")
        lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def _row(label, val):
            lbl = QLabel(val or "—"); lbl.setWordWrap(True); lbl.setObjectName("detailVal")
            form.addRow(QLabel(label), lbl)

        _row("Program Name:", row["name"])
        _row("College Code:", row["college"])
        _row("College Name:", row.get("college_name", ""))
        _row("Enrolled Students:", str(row.get("student_count", "—")))
        lay.addLayout(form)
        lay.addStretch()

        close = _primary_btn("Close"); close.clicked.connect(self.accept)
        lay.addLayout(_btn_row(close))


class StudentDetailDialog(QDialog):
    def __init__(self, parent, row):
        super().__init__(parent)
        self.setWindowTitle("Student Details")
        self.setFixedSize(440, 440)
        self.setStyleSheet(parent.styleSheet())
        lay = QVBoxLayout(self)
        lay.setContentsMargins(30, 30, 30, 24)
        lay.setSpacing(10)

        initials = (row.get("firstname","?")[:1] + row.get("lastname","?")[:1]).upper()
        icon = _CircleIcon(initials, size=90)
        icon_row = QHBoxLayout(); icon_row.addStretch(); icon_row.addWidget(icon); icon_row.addStretch()
        lay.addLayout(icon_row)

        name_lbl = QLabel(f"{row['firstname']} {row['lastname']}")
        name_lbl.setObjectName("detailCode")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(name_lbl)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep")
        lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def _row(label, val):
            lbl = QLabel(val or "—"); lbl.setWordWrap(True); lbl.setObjectName("detailVal")
            form.addRow(QLabel(label), lbl)

        _row("Student ID:", row.get("id",""))
        _row("First Name:", row.get("firstname",""))
        _row("Last Name:", row.get("lastname",""))
        _row("Program:", f"{row.get('course','')} — {row.get('program_name','')}")
        _row("College:", row.get("college_name","") or "N/A")
        _row("Year Level:", str(row.get("year","")))
        _row("Gender:", row.get("gender",""))
        lay.addLayout(form)
        lay.addStretch()

        close = _primary_btn("Close"); close.clicked.connect(self.accept)
        lay.addLayout(_btn_row(close))


# ════════════════════════════════════════════════════════════════════════════
#  CRUD DIALOGS
# ════════════════════════════════════════════════════════════════════════════

class CollegeDialog(QDialog):
    def __init__(self, parent=None, college=None):
        super().__init__(parent)
        self.college = college
        self.setWindowTitle("Edit College" if college else "Add College")
        self.setFixedWidth(440)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setSpacing(16); lay.setContentsMargins(24,24,24,24)
        t = QLabel("Edit College" if self.college else "New College"); t.setObjectName("dlgTitle"); lay.addWidget(t)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep"); lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.code_edit = QLineEdit(); self.code_edit.setPlaceholderText("e.g. CCS"); self.code_edit.setMaxLength(20)
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("e.g. College of Computer Studies")
        if self.college:
            self.code_edit.setText(self.college["code"]); self.name_edit.setText(self.college["name"])
        form.addRow("Code *", self.code_edit)
        form.addRow("Full Name *", self.name_edit)
        lay.addLayout(form); lay.addStretch()
        save_btn = _primary_btn("Save"); save_btn.clicked.connect(self._save)
        lay.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        code = self.code_edit.text().strip().upper()
        name = self.name_edit.text().strip()
        if not code or not name:
            QMessageBox.warning(self, "Validation", "All fields are required."); return
        if not re.match(r'^[A-Z0-9]+$', code):
            QMessageBox.warning(self, "Validation", "Code must be letters/numbers only (no spaces)."); return
        ok, err = db.college_update(self.college["code"], code, name) if self.college else db.college_create(code, name)
        if ok: self.accept()
        else: QMessageBox.critical(self, "Error", f"Could not save: {err}")


class ProgramDialog(QDialog):
    def __init__(self, parent=None, program=None):
        super().__init__(parent)
        self.program = program
        self.setWindowTitle("Edit Program" if program else "Add Program")
        self.setFixedWidth(480)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setSpacing(16); lay.setContentsMargins(24,24,24,24)
        t = QLabel("Edit Program" if self.program else "New Program"); t.setObjectName("dlgTitle"); lay.addWidget(t)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep"); lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.code_edit = QLineEdit(); self.code_edit.setPlaceholderText("e.g. BSCS"); self.code_edit.setMaxLength(20)
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("e.g. Bachelor of Science in Computer Science")
        self.college_combo = QComboBox()
        for col in db.college_all():
            self.college_combo.addItem(f"{col['code']} — {col['name']}", col["code"])
        if self.program:
            self.code_edit.setText(self.program["code"]); self.name_edit.setText(self.program["name"])
            idx = self.college_combo.findData(self.program["college"])
            if idx >= 0: self.college_combo.setCurrentIndex(idx)
        form.addRow("Code *", self.code_edit)
        form.addRow("Full Name *", self.name_edit)
        form.addRow("College *", self.college_combo)
        lay.addLayout(form); lay.addStretch()
        save_btn = _primary_btn("Save"); save_btn.clicked.connect(self._save)
        lay.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        code = self.code_edit.text().strip().upper()
        name = self.name_edit.text().strip()
        college = self.college_combo.currentData()
        if not code or not name or not college:
            QMessageBox.warning(self, "Validation", "All fields are required."); return
        if not re.match(r'^[A-Z0-9]+$', code):
            QMessageBox.warning(self, "Validation", "Code must be letters/numbers only."); return
        ok, err = db.program_update(self.program["code"], code, name, college) if self.program else db.program_create(code, name, college)
        if ok: self.accept()
        else: QMessageBox.critical(self, "Error", f"Could not save: {err}")


class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.setWindowTitle("Edit Student" if student else "Add Student")
        self.setFixedWidth(500)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setSpacing(16); lay.setContentsMargins(24,24,24,24)
        t = QLabel("Edit Student" if self.student else "New Student"); t.setObjectName("dlgTitle"); lay.addWidget(t)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("dlgSep"); lay.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.id_edit = QLineEdit(); self.id_edit.setPlaceholderText("YYYY-NNNN  e.g. 2024-0001"); self.id_edit.setMaxLength(9)
        self.first_edit = QLineEdit(); self.first_edit.setPlaceholderText("First name (letters and hyphens only)")
        self.last_edit  = QLineEdit(); self.last_edit.setPlaceholderText("Last name (letters and hyphens only)")
        self.course_combo = QComboBox()
        for p in db.program_all():
            self.course_combo.addItem(f"{p['code']} — {p['name']}", p["code"])
        self.year_spin = QSpinBox(); self.year_spin.setRange(1, 4)
        self.gender_combo = QComboBox(); self.gender_combo.addItems(["Male", "Female"])

        if self.student:
            self.id_edit.setText(self.student["id"])
            self.first_edit.setText(self.student["firstname"])
            self.last_edit.setText(self.student["lastname"])
            idx = self.course_combo.findData(self.student["course"])
            if idx >= 0: self.course_combo.setCurrentIndex(idx)
            self.year_spin.setValue(self.student["year"])
            gi = self.gender_combo.findText(self.student["gender"])
            if gi >= 0: self.gender_combo.setCurrentIndex(gi)

        form.addRow("Student ID *", self.id_edit)
        form.addRow("First Name *", self.first_edit)
        form.addRow("Last Name *",  self.last_edit)
        form.addRow("Program *",    self.course_combo)
        form.addRow("Year Level *", self.year_spin)
        form.addRow("Gender *",     self.gender_combo)

        hint = QLabel("Names: letters and hyphens only (e.g. Maria, Santos-Cruz)")
        hint.setObjectName("hintLabel")
        form.addRow("", hint)
        lay.addLayout(form); lay.addStretch()
        save_btn = _primary_btn("Save"); save_btn.clicked.connect(self._save)
        lay.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        sid       = self.id_edit.text().strip()
        firstname = self.first_edit.text().strip()
        lastname  = self.last_edit.text().strip()
        course    = self.course_combo.currentData()
        year      = self.year_spin.value()
        gender    = self.gender_combo.currentText()

        if not all([sid, firstname, lastname, course]):
            QMessageBox.warning(self, "Validation", "All fields are required."); return
        if not re.match(r'^\d{4}-\d{4}$', sid):
            QMessageBox.warning(self, "Validation", "ID must be YYYY-NNNN (e.g. 2024-0001)."); return
        yr = int(sid[:4]); seq = int(sid[5:])
        if not (2018 <= yr <= 2025):
            QMessageBox.warning(self, "Validation", "Year in ID must be between 2018 and 2025."); return
        if not (1 <= seq <= 3000):
            QMessageBox.warning(self, "Validation", "Sequence number must be between 0001 and 3000."); return
        if not valid_name(firstname):
            QMessageBox.warning(self, "Validation", "First name: letters and hyphens only."); return
        if not valid_name(lastname):
            QMessageBox.warning(self, "Validation", "Last name: letters and hyphens only."); return

        if self.student:
            ok, err = db.student_update(self.student["id"], sid, firstname, lastname, course, year, gender)
        else:
            ok, err = db.student_create(sid, firstname, lastname, course, year, gender)

        if ok: self.accept()
        else: QMessageBox.critical(self, "Error", f"Could not save: {err}")
