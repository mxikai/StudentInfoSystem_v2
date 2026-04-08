"""
dialogs.py — All CRUD dialog windows for College, Program, Student
"""

import re
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QLabel,
    QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import database as db


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _make_dialog(parent, title, width=420):
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setFixedWidth(width)
    dlg.setStyleSheet(parent.styleSheet() if parent else "")
    return dlg

def _field(label_text, widget, layout):
    layout.addRow(QLabel(label_text), widget)
    return widget

def _btn_row(*buttons):
    row = QHBoxLayout()
    row.addStretch()
    for b in buttons:
        row.addWidget(b)
    return row

def _primary_btn(text):
    b = QPushButton(text)
    b.setObjectName("primaryBtn")
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b

def _cancel_btn(parent_dlg):
    b = QPushButton("Cancel")
    b.setObjectName("cancelBtn")
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.clicked.connect(parent_dlg.reject)
    return b


# ─── College Dialogs ──────────────────────────────────────────────────────────

class CollegeDialog(QDialog):
    def __init__(self, parent=None, college=None):
        super().__init__(parent)
        self.college = college
        self.setWindowTitle("Edit College" if college else "Add College")
        self.setFixedWidth(440)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Edit College" if self.college else "New College")
        title.setObjectName("dlgTitle")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("dlgSep"); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("e.g. CCS")
        self.code_edit.setMaxLength(20)
        if self.college:
            self.code_edit.setText(self.college["code"])

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. College of Computer Studies")
        if self.college:
            self.name_edit.setText(self.college["name"])

        form.addRow("Code *", self.code_edit)
        form.addRow("Full Name *", self.name_edit)
        layout.addLayout(form)
        layout.addStretch()

        save_btn = _primary_btn("Save")
        save_btn.clicked.connect(self._save)
        layout.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        code = self.code_edit.text().strip().upper()
        name = self.name_edit.text().strip()

        if not code or not name:
            QMessageBox.warning(self, "Validation", "All fields are required.")
            return
        if not re.match(r'^[A-Z0-9]+$', code):
            QMessageBox.warning(self, "Validation", "Code must be letters/numbers only (no spaces).")
            return

        if self.college:
            ok, err = db.college_update(self.college["code"], code, name)
        else:
            ok, err = db.college_create(code, name)

        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", f"Could not save: {err}")


# ─── Program Dialogs ──────────────────────────────────────────────────────────

class ProgramDialog(QDialog):
    def __init__(self, parent=None, program=None):
        super().__init__(parent)
        self.program = program
        self.setWindowTitle("Edit Program" if program else "Add Program")
        self.setFixedWidth(480)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Edit Program" if self.program else "New Program")
        title.setObjectName("dlgTitle")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("dlgSep"); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("e.g. BSCS")
        self.code_edit.setMaxLength(20)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Bachelor of Science in Computer Science")

        self.college_combo = QComboBox()
        colleges = db.college_all()
        for col in colleges:
            self.college_combo.addItem(f"{col['code']} — {col['name']}", col["code"])

        if self.program:
            self.code_edit.setText(self.program["code"])
            self.name_edit.setText(self.program["name"])
            idx = self.college_combo.findData(self.program["college"])
            if idx >= 0:
                self.college_combo.setCurrentIndex(idx)

        form.addRow("Code *", self.code_edit)
        form.addRow("Full Name *", self.name_edit)
        form.addRow("College *", self.college_combo)
        layout.addLayout(form)
        layout.addStretch()

        save_btn = _primary_btn("Save")
        save_btn.clicked.connect(self._save)
        layout.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        code    = self.code_edit.text().strip().upper()
        name    = self.name_edit.text().strip()
        college = self.college_combo.currentData()

        if not code or not name or not college:
            QMessageBox.warning(self, "Validation", "All fields are required.")
            return
        if not re.match(r'^[A-Z0-9]+$', code):
            QMessageBox.warning(self, "Validation", "Code must be letters/numbers only.")
            return

        if self.program:
            ok, err = db.program_update(self.program["code"], code, name, college)
        else:
            ok, err = db.program_create(code, name, college)

        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", f"Could not save: {err}")


# ─── Student Dialogs ──────────────────────────────────────────────────────────

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.setWindowTitle("Edit Student" if student else "Add Student")
        self.setFixedWidth(500)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Edit Student" if self.student else "New Student")
        title.setObjectName("dlgTitle")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("dlgSep"); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(12); form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("YYYY-NNNN  e.g. 2024-0001")
        self.id_edit.setMaxLength(9)

        self.first_edit = QLineEdit()
        self.first_edit.setPlaceholderText("First name")

        self.last_edit = QLineEdit()
        self.last_edit.setPlaceholderText("Last name")

        self.course_combo = QComboBox()
        programs = db.program_all()
        for p in programs:
            self.course_combo.addItem(f"{p['code']} — {p['name']}", p["code"])

        self.year_spin = QSpinBox()
        self.year_spin.setRange(1, 4)
        self.year_spin.setSuffix("  (Year level)")

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])

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
        layout.addLayout(form)
        layout.addStretch()

        save_btn = _primary_btn("Save")
        save_btn.clicked.connect(self._save)
        layout.addLayout(_btn_row(_cancel_btn(self), save_btn))

    def _save(self):
        sid       = self.id_edit.text().strip()
        firstname = self.first_edit.text().strip()
        lastname  = self.last_edit.text().strip()
        course    = self.course_combo.currentData()
        year      = self.year_spin.value()
        gender    = self.gender_combo.currentText()

        if not all([sid, firstname, lastname, course]):
            QMessageBox.warning(self, "Validation", "All fields are required.")
            return
        if not re.match(r'^\d{4}-\d{4}$', sid):
            QMessageBox.warning(self, "Validation", "ID must be in format YYYY-NNNN (e.g. 2024-0001).")
            return

        if self.student:
            ok, err = db.student_update(self.student["id"], sid, firstname, lastname, course, year, gender)
        else:
            ok, err = db.student_create(sid, firstname, lastname, course, year, gender)

        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", f"Could not save: {err}")
