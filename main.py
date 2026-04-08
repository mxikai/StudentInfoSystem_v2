"""
main.py — Student Information System main window
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QFrame, QMessageBox,
    QComboBox, QSizePolicy, QAbstractItemView, QSpacerItem
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QColor

import database as db
from dialogs import CollegeDialog, ProgramDialog, StudentDialog
from seed import seed


# ─── Style sheet ──────────────────────────────────────────────────────────────

STYLE = """
/* ── Root ── */
QMainWindow, QDialog {
    background: #0f1117;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}

QWidget {
    background: #0f1117;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

/* ── Sidebar / Header ── */
#header {
    background: #13151f;
    border-bottom: 1px solid #1e2130;
    min-height: 64px;
    max-height: 64px;
}
#appTitle {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: 0.5px;
}
#appSubtitle {
    font-size: 11px;
    color: #64748b;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── Stats bar ── */
#statsBar {
    background: #13151f;
    border-bottom: 1px solid #1e2130;
}
#statCard {
    background: #1a1d2e;
    border: 1px solid #1e2130;
    border-radius: 10px;
    padding: 12px 20px;
    min-width: 140px;
}
#statNumber {
    font-size: 26px;
    font-weight: 700;
    color: #6366f1;
}
#statLabel {
    font-size: 10px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* ── Tabs ── */
QTabWidget::pane {
    border: none;
    background: #0f1117;
}
QTabBar::tab {
    background: transparent;
    color: #64748b;
    padding: 12px 28px;
    font-size: 13px;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}
QTabBar::tab:selected {
    color: #6366f1;
    border-bottom: 2px solid #6366f1;
}
QTabBar::tab:hover:!selected {
    color: #94a3b8;
}

/* ── Toolbar ── */
#toolbar {
    background: #13151f;
    border-bottom: 1px solid #1e2130;
    padding: 10px 20px;
    min-height: 56px;
    max-height: 56px;
}

/* ── Search box ── */
QLineEdit {
    background: #1a1d2e;
    border: 1px solid #1e2130;
    border-radius: 8px;
    color: #e2e8f0;
    padding: 8px 14px;
    font-size: 13px;
    min-width: 260px;
}
QLineEdit:focus {
    border: 1px solid #6366f1;
    background: #1e2237;
}
QLineEdit::placeholder {
    color: #475569;
}

/* ── Buttons ── */
QPushButton {
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    cursor: pointer;
}
#primaryBtn {
    background: #6366f1;
    color: #fff;
    padding: 8px 22px;
}
#primaryBtn:hover { background: #818cf8; }
#primaryBtn:pressed { background: #4f46e5; }

#dangerBtn {
    background: #ef4444;
    color: #fff;
}
#dangerBtn:hover { background: #f87171; }
#dangerBtn:pressed { background: #dc2626; }

#secondaryBtn {
    background: #1e2237;
    color: #94a3b8;
    border: 1px solid #2d3352;
}
#secondaryBtn:hover { background: #252840; color: #e2e8f0; }

#cancelBtn {
    background: #1e2237;
    color: #94a3b8;
    border: 1px solid #2d3352;
    padding: 8px 18px;
}
#cancelBtn:hover { background: #252840; color: #e2e8f0; }

/* ── Table ── */
QTableWidget {
    background: #0f1117;
    border: none;
    gridline-color: #1a1d2e;
    color: #e2e8f0;
    font-size: 13px;
    selection-background-color: #1e2237;
    alternate-background-color: #111420;
}
QTableWidget::item {
    padding: 10px 14px;
    border-bottom: 1px solid #1a1d2e;
}
QTableWidget::item:selected {
    background: #1e2237;
    color: #f1f5f9;
}
QHeaderView::section {
    background: #13151f;
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid #1e2130;
    border-right: 1px solid #1e2130;
}
QHeaderView::section:hover {
    color: #e2e8f0;
    background: #1a1d2e;
}

/* ── Scroll bars ── */
QScrollBar:vertical {
    background: #0f1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2d3352;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #6366f1; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Pagination ── */
#pageBtn {
    background: #1a1d2e;
    color: #94a3b8;
    border: 1px solid #2d3352;
    border-radius: 6px;
    min-width: 34px;
    max-width: 34px;
    min-height: 34px;
    max-height: 34px;
    padding: 0;
    font-size: 13px;
}
#pageBtn:hover { background: #252840; color: #e2e8f0; }
#pageBtnActive {
    background: #6366f1;
    color: #fff;
    border: none;
    border-radius: 6px;
    min-width: 34px;
    max-width: 34px;
    min-height: 34px;
    max-height: 34px;
    padding: 0;
    font-size: 13px;
    font-weight: 600;
}
#pageInfo {
    color: #64748b;
    font-size: 12px;
}

/* ── Combo ── */
QComboBox {
    background: #1a1d2e;
    border: 1px solid #1e2130;
    border-radius: 8px;
    color: #e2e8f0;
    padding: 7px 14px;
    font-size: 13px;
    min-width: 120px;
}
QComboBox:focus { border-color: #6366f1; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView {
    background: #1a1d2e;
    border: 1px solid #2d3352;
    color: #e2e8f0;
    selection-background-color: #6366f1;
}

/* ── SpinBox ── */
QSpinBox {
    background: #1a1d2e;
    border: 1px solid #1e2130;
    border-radius: 8px;
    color: #e2e8f0;
    padding: 7px 14px;
    font-size: 13px;
}
QSpinBox:focus { border-color: #6366f1; }

/* ── Dialog internals ── */
#dlgTitle {
    font-size: 16px;
    font-weight: 700;
    color: #f1f5f9;
}
#dlgSep {
    color: #1e2130;
    background: #1e2130;
    max-height: 1px;
}
QFormLayout QLabel {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 500;
}

/* ── Badge chips ── */
#chipM { color: #60a5fa; font-size: 11px; font-weight: 600; }
#chipF { color: #f472b6; font-size: 11px; font-weight: 600; }
"""


# ─── Reusable Table Tab ────────────────────────────────────────────────────────

class TableTab(QWidget):
    """Base class for a tab with search + table + pagination."""

    PER_PAGE = 25

    def __init__(self, columns, fetch_fn, add_fn, edit_fn, delete_fn, parent=None):
        super().__init__(parent)
        self.columns    = columns       # list of (header, key) tuples
        self.fetch_fn   = fetch_fn
        self.add_fn     = add_fn
        self.edit_fn    = edit_fn
        self.delete_fn  = delete_fn

        self.current_page  = 1
        self.total_records = 0
        self.sort_col      = columns[0][1]
        self.sort_dir      = "ASC"
        self._selected_row_data = None

        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_search)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Toolbar
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(20, 0, 20, 0)
        tb.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Search…")
        self.search_box.textChanged.connect(self._on_search_changed)
        tb.addWidget(self.search_box)

        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["10", "25", "50", "100"])
        self.per_page_combo.setCurrentText("25")
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        tb.addWidget(QLabel("Rows:"))
        tb.addWidget(self.per_page_combo)

        tb.addStretch()

        self.add_btn = QPushButton("＋  Add")
        self.add_btn.setObjectName("primaryBtn")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self._on_add)

        self.edit_btn = QPushButton("✎  Edit")
        self.edit_btn.setObjectName("secondaryBtn")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self._on_edit)

        self.del_btn = QPushButton("🗑  Delete")
        self.del_btn.setObjectName("dangerBtn")
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.setEnabled(False)
        self.del_btn.clicked.connect(self._on_delete)

        tb.addWidget(self.edit_btn)
        tb.addWidget(self.del_btn)
        tb.addWidget(self.add_btn)
        root.addWidget(toolbar)

        # ── Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c[0] for c in self.columns])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_edit)
        root.addWidget(self.table, 1)

        # ── Pagination bar
        pag_frame = QFrame()
        pag_frame.setObjectName("toolbar")
        pag_layout = QHBoxLayout(pag_frame)
        pag_layout.setContentsMargins(20, 8, 20, 8)

        self.page_info = QLabel()
        self.page_info.setObjectName("pageInfo")
        pag_layout.addWidget(self.page_info)
        pag_layout.addStretch()

        self.pag_container = QHBoxLayout()
        self.pag_container.setSpacing(4)
        pag_layout.addLayout(self.pag_container)
        root.addWidget(pag_frame)

    # ── Data ──────────────────────────────────────────────────────────────────

    def refresh(self):
        search = self.search_box.text().strip()
        per_page = int(self.per_page_combo.currentText())
        rows, total = self.fetch_fn(
            search=search,
            sort_col=self.sort_col,
            sort_dir=self.sort_dir,
            page=self.current_page,
            per_page=per_page
        )
        self.total_records = total
        self._populate(rows)
        self._update_pagination(total, per_page)

    def _populate(self, rows):
        self.table.setRowCount(0)
        self._selected_row_data = None
        self.edit_btn.setEnabled(False)
        self.del_btn.setEnabled(False)

        for row_data in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c_idx, (header, key) in enumerate(self.columns):
                val = str(row_data.get(key, "") or "")
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, row_data)
                self.table.setItem(r, c_idx, item)
            self.table.setRowHeight(r, 42)

    def _update_pagination(self, total, per_page):
        total_pages = max(1, (total + per_page - 1) // per_page)
        # clamp
        if self.current_page > total_pages:
            self.current_page = total_pages

        start = (self.current_page - 1) * per_page + 1
        end   = min(self.current_page * per_page, total)
        self.page_info.setText(f"Showing {start}–{end} of {total:,} records")

        # clear old buttons
        while self.pag_container.count():
            w = self.pag_container.takeAt(0)
            if w.widget():
                w.widget().deleteLater()

        def make_btn(label, page, active=False):
            b = QPushButton(str(label))
            b.setObjectName("pageBtnActive" if active else "pageBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, p=page: self._go_page(p))
            return b

        self.pag_container.addWidget(make_btn("‹", max(1, self.current_page - 1)))

        pages_to_show = self._page_range(self.current_page, total_pages)
        prev = None
        for p in pages_to_show:
            if prev is not None and p - prev > 1:
                dots = QLabel("…")
                dots.setObjectName("pageInfo")
                dots.setAlignment(Qt.AlignmentFlag.AlignCenter)
                dots.setFixedWidth(28)
                self.pag_container.addWidget(dots)
            self.pag_container.addWidget(make_btn(p, p, active=(p == self.current_page)))
            prev = p

        self.pag_container.addWidget(make_btn("›", min(total_pages, self.current_page + 1)))

    def _page_range(self, cur, total):
        if total <= 7:
            return list(range(1, total + 1))
        pages = set()
        pages.add(1); pages.add(total)
        for d in range(-2, 3):
            p = cur + d
            if 1 <= p <= total:
                pages.add(p)
        return sorted(pages)

    def _go_page(self, page):
        self.current_page = page
        self.refresh()

    # ── Events ────────────────────────────────────────────────────────────────

    def _on_search_changed(self):
        self.current_page = 1
        self._search_timer.start(300)

    def _do_search(self):
        self.refresh()

    def _on_per_page_changed(self):
        self.current_page = 1
        self.refresh()

    def _on_header_clicked(self, idx):
        key = self.columns[idx][1]
        if self.sort_col == key:
            self.sort_dir = "DESC" if self.sort_dir == "ASC" else "ASC"
        else:
            self.sort_col = key
            self.sort_dir = "ASC"
        self.current_page = 1
        self.refresh()

    def _on_selection_changed(self):
        rows = self.table.selectedItems()
        if rows:
            self._selected_row_data = rows[0].data(Qt.ItemDataRole.UserRole)
            self.edit_btn.setEnabled(True)
            self.del_btn.setEnabled(True)
        else:
            self._selected_row_data = None
            self.edit_btn.setEnabled(False)
            self.del_btn.setEnabled(False)

    def _on_add(self):
        dlg = self.add_fn(self)
        if dlg.exec():
            self.refresh()

    def _on_edit(self):
        if not self._selected_row_data:
            return
        dlg = self.edit_fn(self, self._selected_row_data)
        if dlg.exec():
            self.refresh()

    def _on_delete(self):
        if not self._selected_row_data:
            return
        name = self._selected_row_data.get("name") or self._selected_row_data.get("id", "this record")
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete <b>{name}</b>?<br><br>This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, err = self.delete_fn(self._selected_row_data)
            if ok:
                self.refresh()
            else:
                QMessageBox.warning(self, "Cannot Delete", err)


# ─── Delete wrappers (return data dict, not positional args) ──────────────────

def _del_college(row):
    return db.college_delete(row["code"])

def _del_program(row):
    return db.program_delete(row["code"])

def _del_student(row):
    return db.student_delete(row["id"])


# ─── Main Window ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 780)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Header
        header = QFrame()
        header.setObjectName("header")
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(24, 0, 24, 0)

        logo_col = QVBoxLayout()
        logo_col.setSpacing(2)
        t = QLabel("StudentInfoSystem")
        t.setObjectName("appTitle")
        s = QLabel("RDBMS Edition · SQLite")
        s.setObjectName("appSubtitle")
        logo_col.addWidget(t)
        logo_col.addWidget(s)
        hlay.addLayout(logo_col)
        hlay.addStretch()
        root.addWidget(header)

        # ── Stats bar
        stats_bar = QFrame()
        stats_bar.setObjectName("statsBar")
        sb = QHBoxLayout(stats_bar)
        sb.setContentsMargins(24, 12, 24, 12)
        sb.setSpacing(12)

        self.stat_students  = self._stat_card("0", "Students")
        self.stat_programs  = self._stat_card("0", "Programs")
        self.stat_colleges  = self._stat_card("0", "Colleges")

        sb.addWidget(self.stat_students)
        sb.addWidget(self.stat_programs)
        sb.addWidget(self.stat_colleges)
        sb.addStretch()

        refresh_btn = QPushButton("↻  Refresh Stats")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self._refresh_stats)
        sb.addWidget(refresh_btn)
        root.addWidget(stats_bar)

        # ── Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        # Students tab
        student_tab = TableTab(
            columns=[
                ("Student ID", "id"),
                ("First Name", "firstname"),
                ("Last Name",  "lastname"),
                ("Program",    "course"),
                ("Year",       "year"),
                ("Gender",     "gender"),
            ],
            fetch_fn=db.student_list,
            add_fn=lambda p: StudentDialog(p),
            edit_fn=lambda p, row: StudentDialog(p, db.student_get(row["id"])),
            delete_fn=_del_student,
        )

        # Programs tab
        program_tab = TableTab(
            columns=[
                ("Code",        "code"),
                ("Program Name","name"),
                ("College",     "college"),
                ("# Students",  "student_count"),
            ],
            fetch_fn=db.program_list,
            add_fn=lambda p: ProgramDialog(p),
            edit_fn=lambda p, row: ProgramDialog(p, db.program_get(row["code"])),
            delete_fn=_del_program,
        )

        # Colleges tab
        college_tab = TableTab(
            columns=[
                ("Code",       "code"),
                ("College Name","name"),
                ("# Programs", "program_count"),
            ],
            fetch_fn=db.college_list,
            add_fn=lambda p: CollegeDialog(p),
            edit_fn=lambda p, row: CollegeDialog(p, db.college_get(row["code"])),
            delete_fn=_del_college,
        )

        tabs.addTab(student_tab,  "  🎓  Students  ")
        tabs.addTab(program_tab,  "  📚  Programs  ")
        tabs.addTab(college_tab,  "  🏛  Colleges  ")
        tabs.currentChanged.connect(lambda _: self._refresh_stats())
        root.addWidget(tabs, 1)

        self._refresh_stats()

    def _stat_card(self, number, label):
        card = QFrame()
        card.setObjectName("statCard")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        num_lbl = QLabel(number)
        num_lbl.setObjectName("statNumber")
        lbl = QLabel(label)
        lbl.setObjectName("statLabel")
        lay.addWidget(num_lbl)
        lay.addWidget(lbl)
        card._num_lbl = num_lbl
        return card

    def _refresh_stats(self):
        students, programs, colleges = db.get_stats()
        self.stat_students._num_lbl.setText(f"{students:,}")
        self.stat_programs._num_lbl.setText(f"{programs:,}")
        self.stat_colleges._num_lbl.setText(f"{colleges:,}")


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    db.init_db()
    seed()                        # no-op if already seeded

    app = QApplication(sys.argv)
    app.setApplicationName("StudentInfoSystem")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
