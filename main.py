"""
main.py — MSU-IIT Student Information System
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QFrame, QMessageBox,
    QComboBox, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

import database as db
from dialogs import (CollegeDialog, ProgramDialog, StudentDialog,
                     CollegeDetailDialog, ProgramDetailDialog, StudentDetailDialog)
from seed import seed

# ── Palette ────────────────────────────────────────────────────────────────────
# Main:   #F1ECE4  (warm linen)
# Accent: #68191F  (deep crimson)
# Dark:   #3D0B0E  (darker crimson)
# Card:   #E8D8C4  (sandy beige)
# Border: #C9B89E  (warm tan)
# Text:   #2D1A1A  (dark brown-black)
# Muted:  #7A5C5C  (muted rose-brown)

STYLE = """
QMainWindow, QDialog, QWidget {
    background: #F1ECE4;
    color: #2D1A1A;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}

/* ── Header ── */
#header {
    background: #68191F;
    min-height: 68px; max-height: 68px;
}
#appTitle {
    font-size: 19px; font-weight: 700; color: #F1ECE4; letter-spacing: 0.4px;
}
#appSubtitle {
    font-size: 10px; color: #C9A0A3; letter-spacing: 1.8px;
}

/* ── Stats bar ── */
#statsBar { background: #68191F; border-bottom: 1px solid #C9B89E; }
#statCard {
    background: #F1ECE4; border: 1px solid #C9B89E; border-radius: 10px;
    padding: 12px 22px; min-width: 140px;
}
#statNumber { font-size: 26px; font-weight: 700; color: #68191F; }
#statLabel  { font-size: 10px; color: #7A5C5C; text-transform: uppercase; letter-spacing: 1.2px; }

/* ── Tabs ── */
QTabWidget::pane { border: none; background: #F1ECE4; }
QTabBar::tab {
    background: transparent; color: #7A5C5C;
    padding: 12px 30px; font-size: 13px; font-weight: 500;
    border-bottom: 2px solid transparent; margin-right: 4px;
}
QTabBar::tab:selected  { color: #68191F; border-bottom: 2px solid #68191F; }
QTabBar::tab:hover:!selected { color: #3D0B0E; }

/* ── Toolbar ── */
#toolbar {
    background: #EAE2D6; border-bottom: 1px solid #C9B89E;
    padding: 10px 20px; min-height: 58px; max-height: 58px;
}

/* ── Search ── */
QLineEdit {
    background: #F1ECE4; border: 1.5px solid #C9B89E; border-radius: 8px;
    color: #2D1A1A; padding: 8px 14px; font-size: 13px; min-width: 260px;
}
QLineEdit:focus { border-color: #68191F; }

/* ── Buttons ── */
QPushButton { border-radius: 8px; padding: 8px 18px; font-size: 13px; font-weight: 500; border: none; }
#primaryBtn  { background: #68191F; color: #F1ECE4; padding: 8px 22px; }
#primaryBtn:hover  { background: #8B2329; }
#primaryBtn:pressed{ background: #3D0B0E; }
#dangerBtn   { background: #C0392B; color: #fff; }
#dangerBtn:hover { background: #E74C3C; }
#secondaryBtn{ background: #E0D6C8; color: #2D1A1A; border: 1px solid #C9B89E; }
#secondaryBtn:hover { background: #D0C4B0; }
#cancelBtn   { background: #E0D6C8; color: #2D1A1A; border: 1px solid #C9B89E; padding: 8px 18px; }
#cancelBtn:hover { background: #D0C4B0; }

/* ── Table ── */
QTableWidget {
    background: #F1ECE4; border: none; gridline-color: #E0D6C8;
    color: #2D1A1A; font-size: 13px;
    selection-background-color: #F5DDD9;
    alternate-background-color: #EAE2D6;
}
QTableWidget::item { padding: 10px 14px; border-bottom: 1px solid #E0D6C8; }
QTableWidget::item:selected { background: #F5DDD9; color: #3D0B0E; }
QHeaderView::section {
    background: #EAE2D6; color: #7A5C5C; font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.8px;
    padding: 10px 14px; border: none; border-bottom: 1.5px solid #C9B89E;
    border-right: 1px solid #C9B89E;
}
QHeaderView::section:hover { color: #2D1A1A; background: #DDD4C5; }

/* ── Scrollbars ── */
QScrollBar:vertical { background: #F1ECE4; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #C9B89E; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #68191F; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Pagination ── */
#pageBtn {
    background: #E0D6C8; color: #7A5C5C; border: 1px solid #C9B89E;
    border-radius: 6px; min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px;
}
#pageBtn:hover { background: #D0C4B0; color: #2D1A1A; }
#pageBtnActive {
    background: #68191F; color: #F1ECE4; border: none;
    border-radius: 6px; min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px; font-weight: 600;
}
#pageInfo { color: #7A5C5C; font-size: 12px; }

/* ── Combo / Spin ── */
QComboBox, QSpinBox {
    background: #F1ECE4; border: 1.5px solid #C9B89E; border-radius: 8px;
    color: #2D1A1A; padding: 7px 14px; font-size: 13px;
}
QComboBox:focus, QSpinBox:focus { border-color: #68191F; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView {
    background: #F1ECE4; border: 1px solid #C9B89E;
    color: #2D1A1A; selection-background-color: #F5DDD9;
}

/* ── Dialog ── */
#dlgTitle  { font-size: 16px; font-weight: 700; color: #3D0B0E; }
#dlgSep    { color: #C9B89E; background: #C9B89E; max-height: 1px; }
#detailCode{ font-size: 20px; font-weight: 700; color: #68191F; }
#detailVal { color: #2D1A1A; font-size: 13px; }
#hintLabel { color: #7A5C5C; font-size: 11px; font-style: italic; }
QFormLayout QLabel { color: #7A5C5C; font-size: 12px; font-weight: 500; }

/* ── Bulk banner ── */
#bulkBanner {
    background: #3D0B0E; color: #F1ECE4;
    padding: 8px 20px; font-size: 13px; font-weight: 500;
}
#bulkBannerLabel { color: #F1ECE4; font-size: 13px; font-weight: 500; }
"""


# ── Table tab ─────────────────────────────────────────────────────────────────

class TableTab(QWidget):
    PER_PAGE = 25

    def __init__(self, columns, fetch_fn, add_fn, edit_fn, delete_fn,
                 detail_fn, delete_label="record", parent=None):
        super().__init__(parent)
        self.columns      = columns
        self.fetch_fn     = fetch_fn
        self.add_fn       = add_fn
        self.edit_fn      = edit_fn
        self.delete_fn    = delete_fn
        self.detail_fn    = detail_fn
        self.delete_label = delete_label

        self.current_page = 1
        self.total_records = 0
        self.sort_col  = columns[0][1]
        self.sort_dir  = "ASC"
        self._rows_data = []

        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_search)

        self._build_ui()
        self.refresh()

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(0); root.setContentsMargins(0, 0, 0, 0)

        # toolbar
        toolbar = QFrame(); toolbar.setObjectName("toolbar")
        tb = QHBoxLayout(toolbar); tb.setContentsMargins(20, 0, 20, 0); tb.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Search…")
        self.search_box.textChanged.connect(self._on_search_changed)
        tb.addWidget(self.search_box)

        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["10", "25", "50", "100"])
        self.per_page_combo.setCurrentText("25")
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        tb.addWidget(QLabel("Rows:")); tb.addWidget(self.per_page_combo)
        tb.addStretch()

        self.add_btn  = self._mk_btn("＋  Add",    "primaryBtn",   self._on_add)
        self.edit_btn = self._mk_btn("✎  Edit",    "secondaryBtn", self._on_edit,  False)
        self.del_btn  = self._mk_btn("🗑  Delete",  "dangerBtn",    self._on_delete, False)

        tb.addWidget(self.edit_btn); tb.addWidget(self.del_btn); tb.addWidget(self.add_btn)
        root.addWidget(toolbar)

        # bulk banner (hidden by default)
        self.bulk_banner = QFrame(); self.bulk_banner.setObjectName("bulkBanner")
        bb = QHBoxLayout(self.bulk_banner); bb.setContentsMargins(20, 0, 20, 0)
        self.bulk_label = QLabel(); self.bulk_label.setObjectName("bulkBannerLabel")
        bulk_del = self._mk_btn("🗑  Delete Selected", "dangerBtn", self._on_bulk_delete)
        bulk_clr = self._mk_btn("✕  Clear Selection",  "cancelBtn", self._clear_selection)
        bb.addWidget(self.bulk_label); bb.addStretch()
        bb.addWidget(bulk_del); bb.addWidget(bulk_clr)
        self.bulk_banner.setVisible(False)
        root.addWidget(self.bulk_banner)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c[0] for c in self.columns])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_double_click)
        root.addWidget(self.table, 1)

        # pagination bar
        pag_frame = QFrame(); pag_frame.setObjectName("toolbar")
        pl = QHBoxLayout(pag_frame); pl.setContentsMargins(20, 8, 20, 8)
        self.page_info = QLabel(); self.page_info.setObjectName("pageInfo")
        pl.addWidget(self.page_info); pl.addStretch()
        self.pag_container = QHBoxLayout(); self.pag_container.setSpacing(4)
        pl.addLayout(self.pag_container)
        root.addWidget(pag_frame)

    def _mk_btn(self, text, obj, slot, enabled=True):
        b = QPushButton(text); b.setObjectName(obj)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setEnabled(enabled)
        b.clicked.connect(slot)
        return b

    # ── Data ──────────────────────────────────────────────────────────────────

    def refresh(self):
        search   = self.search_box.text().strip()
        per_page = int(self.per_page_combo.currentText())
        rows, total = self.fetch_fn(search=search, sort_col=self.sort_col,
                                    sort_dir=self.sort_dir, page=self.current_page,
                                    per_page=per_page)
        self.total_records = total
        self._populate(rows)
        self._update_pagination(total, per_page)

    def _populate(self, rows):
        self.table.setRowCount(0)
        self._rows_data = rows
        self._update_selection_ui()

        for row_data in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for ci, (header, key) in enumerate(self.columns):
                val = str(row_data.get(key, "") if row_data.get(key) is not None else "N/A")
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, row_data)
                self.table.setItem(r, ci, item)
            self.table.setRowHeight(r, 42)

    def _update_pagination(self, total, per_page):
        total_pages = max(1, (total + per_page - 1) // per_page)
        if self.current_page > total_pages: self.current_page = total_pages

        start = (self.current_page - 1) * per_page + 1
        end   = min(self.current_page * per_page, total)
        self.page_info.setText(f"Showing {start}–{end} of {total:,} records")

        while self.pag_container.count():
            w = self.pag_container.takeAt(0)
            if w.widget(): w.widget().deleteLater()

        def mkb(label, page, active=False):
            b = QPushButton(str(label))
            b.setObjectName("pageBtnActive" if active else "pageBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, p=page: self._go_page(p))
            return b

        self.pag_container.addWidget(mkb("‹", max(1, self.current_page - 1)))
        prev = None
        for p in self._page_range(self.current_page, total_pages):
            if prev is not None and p - prev > 1:
                d = QLabel("…"); d.setObjectName("pageInfo")
                d.setAlignment(Qt.AlignmentFlag.AlignCenter); d.setFixedWidth(28)
                self.pag_container.addWidget(d)
            self.pag_container.addWidget(mkb(p, p, active=(p == self.current_page)))
            prev = p
        self.pag_container.addWidget(mkb("›", min(total_pages, self.current_page + 1)))

    def _page_range(self, cur, total):
        if total <= 7: return list(range(1, total + 1))
        pages = {1, total}
        for d in range(-2, 3):
            p = cur + d
            if 1 <= p <= total: pages.add(p)
        return sorted(pages)

    def _go_page(self, page):
        self.current_page = page; self.refresh()

    # ── Events ────────────────────────────────────────────────────────────────

    def _on_search_changed(self):
        self.current_page = 1; self._search_timer.start(300)

    def _do_search(self): self.refresh()

    def _on_per_page_changed(self):
        self.current_page = 1; self.refresh()

    def _on_header_clicked(self, idx):
        key = self.columns[idx][1]
        if self.sort_col == key:
            self.sort_dir = "DESC" if self.sort_dir == "ASC" else "ASC"
        else:
            self.sort_col = key; self.sort_dir = "ASC"
        self.current_page = 1; self.refresh()

    def _on_selection_changed(self):
        self._update_selection_ui()

    def _update_selection_ui(self):
        sel = self._selected_rows()
        n = len(sel)
        single = n == 1

        self.edit_btn.setEnabled(single)
        self.del_btn.setEnabled(single)

        if n > 1:
            self.bulk_banner.setVisible(True)
            self.bulk_label.setText(f"{n} rows selected — bulk delete enabled")
        else:
            self.bulk_banner.setVisible(False)

    def _selected_rows(self):
        seen = set()
        rows = []
        for item in self.table.selectedItems():
            r = item.row()
            if r not in seen:
                seen.add(r)
                rows.append(item.data(Qt.ItemDataRole.UserRole))
        return rows

    def _clear_selection(self):
        self.table.clearSelection()

    def _on_add(self):
        dlg = self.add_fn(self)
        if dlg.exec(): self.refresh()

    def _on_edit(self):
        rows = self._selected_rows()
        if not rows: return
        dlg = self.edit_fn(self, rows[0])
        if dlg.exec(): self.refresh()

    def _on_double_click(self, index):
        item = self.table.item(index.row(), 0)
        if not item: return
        row_data = item.data(Qt.ItemDataRole.UserRole)
        self.detail_fn(self, row_data).exec()

    def _on_delete(self):
        rows = self._selected_rows()
        if not rows: return
        self._confirm_and_delete(rows)

    def _on_bulk_delete(self):
        rows = self._selected_rows()
        if not rows: return
        self._confirm_and_delete(rows)

    def _confirm_and_delete(self, rows):
        n = len(rows)
        name = (rows[0].get("name") or rows[0].get("id") or "this record") if n == 1 else f"{n} {self.delete_label}s"
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"<b>Delete {name}?</b><br><br>This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if reply != QMessageBox.StandardButton.Yes: return

        errors = []
        for row in rows:
            ok, err = self.delete_fn(row)
            if not ok: errors.append(err)

        if errors:
            QMessageBox.warning(self, "Some deletions failed",
                                "\n".join(set(errors)))
        self.refresh()


# ── DB delete wrappers ────────────────────────────────────────────────────────

def _del_college(row): return db.college_delete(row["code"])
def _del_program(row): return db.program_delete(row["code"])
def _del_student(row): return db.student_delete(row["id"])


# ── Main Window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSU-IIT Student Information System")
        self.setMinimumSize(1100, 700); self.resize(1300, 800)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central); root.setSpacing(0); root.setContentsMargins(0,0,0,0)

        # ── Header
        header = QFrame(); header.setObjectName("header")
        hl = QHBoxLayout(header); hl.setContentsMargins(28, 0, 28, 0)
        col = QVBoxLayout(); col.setSpacing(2)
        t = QLabel("MSU-IIT Student Information System"); t.setObjectName("appTitle")
        s = QLabel("MINDANAO STATE UNIVERSITY · ILIGAN INSTITUTE OF TECHNOLOGY"); s.setObjectName("appSubtitle")
        col.addWidget(t); col.addWidget(s)
        hl.addLayout(col); hl.addStretch()
        root.addWidget(header)

        # ── Stats bar
        sb_frame = QFrame(); sb_frame.setObjectName("statsBar")
        sb = QHBoxLayout(sb_frame); sb.setContentsMargins(28, 14, 28, 14); sb.setSpacing(14)
        self.stat_students = self._stat_card("0", "Students")
        self.stat_programs = self._stat_card("0", "Programs")
        self.stat_colleges = self._stat_card("0", "Colleges")
        sb.addWidget(self.stat_students); sb.addWidget(self.stat_programs); sb.addWidget(self.stat_colleges)
        sb.addStretch()
        refresh_btn = QPushButton("↻  Refresh"); refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self._refresh_stats)
        sb.addWidget(refresh_btn)
        root.addWidget(sb_frame)

        # ── Tabs
        tabs = QTabWidget(); tabs.setDocumentMode(True)

        student_tab = TableTab(
            columns=[
                ("Student ID", "id"), ("First Name", "firstname"), ("Last Name", "lastname"),
                ("Program", "course"), ("Year", "year"), ("Gender", "gender"),
            ],
            fetch_fn=db.student_list,
            add_fn=lambda p: StudentDialog(p),
            edit_fn=lambda p, row: StudentDialog(p, db.student_get(row["id"])),
            delete_fn=_del_student,
            detail_fn=lambda p, row: StudentDetailDialog(p, db.student_get(row["id"])),
            delete_label="student",
        )

        program_tab = TableTab(
            columns=[
                ("Code", "code"), ("Program Name", "name"),
                ("College", "college"), ("# Students", "student_count"),
            ],
            fetch_fn=db.program_list,
            add_fn=lambda p: ProgramDialog(p),
            edit_fn=lambda p, row: ProgramDialog(p, db.program_get(row["code"])),
            delete_fn=_del_program,
            detail_fn=lambda p, row: ProgramDetailDialog(p, db.program_get_detail(row["code"])),
            delete_label="program",
        )

        college_tab = TableTab(
            columns=[
                ("Code", "code"), ("College Name", "name"), ("# Programs", "program_count"),
            ],
            fetch_fn=db.college_list,
            add_fn=lambda p: CollegeDialog(p),
            edit_fn=lambda p, row: CollegeDialog(p, db.college_get(row["code"])),
            delete_fn=_del_college,
            detail_fn=lambda p, row: CollegeDetailDialog(p, db.college_get_detail(row["code"])),
            delete_label="college",
        )

        tabs.addTab(student_tab,  "  🎓  Students  ")
        tabs.addTab(program_tab,  "  📚  Programs  ")
        tabs.addTab(college_tab,  "  🏛  Colleges  ")
        tabs.currentChanged.connect(lambda _: self._refresh_stats())
        root.addWidget(tabs, 1)
        self._refresh_stats()

    def _stat_card(self, number, label):
        card = QFrame(); card.setObjectName("statCard")
        lay = QVBoxLayout(card); lay.setContentsMargins(0,0,0,0); lay.setSpacing(2)
        n = QLabel(number); n.setObjectName("statNumber")
        l = QLabel(label);  l.setObjectName("statLabel")
        lay.addWidget(n); lay.addWidget(l)
        card._num_lbl = n
        return card

    def _refresh_stats(self):
        students, programs, colleges = db.get_stats()
        self.stat_students._num_lbl.setText(f"{students:,}")
        self.stat_programs._num_lbl.setText(f"{programs:,}")
        self.stat_colleges._num_lbl.setText(f"{colleges:,}")


def main():
    db.init_db()
    seed()
    app = QApplication(sys.argv)
    app.setApplicationName("MSU-IIT SIS")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
