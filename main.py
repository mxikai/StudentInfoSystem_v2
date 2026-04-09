"""
main.py — MSU-IIT Student Information System
Redesigned: left sidebar nav + white content area, inspired by modern dashboard UI
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QFrame, QMessageBox,
    QComboBox, QAbstractItemView, QSizePolicy, QSpacerItem,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPen, QLinearGradient

import database as db
from dialogs import (CollegeDialog, ProgramDialog, StudentDialog,
                     CollegeDetailDialog, ProgramDetailDialog, StudentDetailDialog)
from seed import seed

# ─────────────────────────────────────────────────────────────────────────────
# Palette
#   Sidebar bg:   #1E2A4A  (deep navy)
#   Sidebar sel:  #2E3F6E  (medium navy)
#   Accent:       #4B72B8  (cornflower blue)
#   Content bg:   #F0F4FA  (very light blue-grey)
#   Card bg:      #FFFFFF
#   Card border:  #E4EAF5
#   Text primary: #1A2340
#   Text muted:   #7A8BAD
#   Header bg:    #FFFFFF
#   Danger:       #E05252
# ─────────────────────────────────────────────────────────────────────────────

STYLE = """
/* ── Global ── */
* { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }

QMainWindow, QDialog {
    background: #F0F4FA;
}
QWidget {
    background: transparent;
    color: #1A2340;
    font-size: 13px;
}

/* ── Sidebar ── */
#sidebar {
    background: #1E2A4A;
    min-width: 220px; max-width: 220px;
}
#sidebarLogo {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.3px;
}
#sidebarSub {
    color: #6A7FA8;
    font-size: 9px;
    letter-spacing: 1.4px;
}
#sidebarDivider {
    background: #2A3A60;
    max-height: 1px; min-height: 1px;
}
#sidebarSectionLabel {
    color: #4A5E82;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.8px;
    padding: 0 20px;
}

/* Sidebar nav buttons */
#navBtn {
    background: transparent;
    color: #8A9BC0;
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 11px 16px;
    font-size: 13px;
    font-weight: 500;
}
#navBtn:hover { background: #243258; color: #C8D8F0; }
#navBtnActive {
    background: #2E3F6E;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 11px 16px;
    font-size: 13px;
    font-weight: 600;
}
#navBtnActive:hover { background: #354A80; }

/* ── Content area ── */
#contentArea { background: #F0F4FA; }

/* ── Page header ── */
#pageHeader { background: #FFFFFF; border-bottom: 1px solid #E4EAF5; }
#pageTitle { font-size: 20px; font-weight: 700; color: #1A2340; }
#pageSubtitle { font-size: 12px; color: #7A8BAD; }

/* ── Stat cards ── */
#statCard {
    background: #FFFFFF;
    border: 1px solid #E4EAF5;
    border-radius: 14px;
    padding: 0;
}
#statNumber { font-size: 28px; font-weight: 700; color: #1A2340; }
#statLabel  { font-size: 10px; color: #7A8BAD; font-weight: 600; letter-spacing: 1.2px; }
#statIcon   { font-size: 22px; }

/* ── Table card ── */
#tableCard {
    background: #FFFFFF;
    border: 1px solid #E4EAF5;
    border-radius: 14px;
}

/* ── Toolbar inside table card ── */
#cardToolbar { background: #FFFFFF; border-radius: 14px 14px 0 0; }

/* ── Search ── */
QLineEdit {
    background: #F0F4FA;
    border: 1.5px solid #E4EAF5;
    border-radius: 10px;
    color: #1A2340;
    padding: 9px 14px 9px 36px;
    font-size: 13px;
    min-width: 240px;
}
QLineEdit:focus { border-color: #4B72B8; background: #FFFFFF; }

/* ── Buttons ── */
QPushButton {
    border-radius: 10px;
    padding: 9px 20px;
    font-size: 13px;
    font-weight: 600;
    border: none;
    cursor: pointer;
}
#primaryBtn  { background: #4B72B8; color: #FFFFFF; }
#primaryBtn:hover   { background: #3A5EA0; }
#primaryBtn:pressed { background: #2D4B88; }
#dangerBtn   { background: #E05252; color: #FFFFFF; }
#dangerBtn:hover  { background: #C84040; }
#secondaryBtn {
    background: #F0F4FA;
    color: #4B72B8;
    border: 1.5px solid #D0DCEF;
    font-weight: 600;
}
#secondaryBtn:hover { background: #E4EAF5; }
#secondaryBtn:disabled { color: #B0BDD8; border-color: #E4EAF5; }
#dangerBtn:disabled { background: #F5C0C0; color: #FFFFFF; }
#cancelBtn {
    background: #F0F4FA;
    color: #7A8BAD;
    border: 1.5px solid #D0DCEF;
    padding: 9px 18px;
}
#cancelBtn:hover { background: #E4EAF5; color: #1A2340; }

/* ── Table ── */
QTableWidget {
    background: #FFFFFF;
    border: none;
    gridline-color: transparent;
    color: #1A2340;
    font-size: 13px;
    selection-background-color: #EDF2FC;
    alternate-background-color: #F8FAFD;
    outline: none;
}
QTableWidget::item {
    padding: 0 16px;
    border-bottom: 1px solid #F0F4FA;
    color: #1A2340;
}
QTableWidget::item:selected {
    background: #EDF2FC;
    color: #1A2340;
}
QHeaderView::section {
    background: #F8FAFD;
    color: #7A8BAD;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.7px;
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid #E4EAF5;
    text-transform: uppercase;
}
QHeaderView { background: #F8FAFD; border-radius: 0; }

/* ── Scrollbars ── */
QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #D0DCEF;
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #4B72B8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 0; }

/* ── Pagination ── */
#pageBtn {
    background: #F0F4FA;
    color: #7A8BAD;
    border: 1.5px solid #E4EAF5;
    border-radius: 8px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0;
    font-size: 13px;
    font-weight: 500;
}
#pageBtn:hover { background: #E4EAF5; color: #1A2340; }
#pageBtnActive {
    background: #4B72B8;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0;
    font-size: 13px;
    font-weight: 700;
}
#pageInfo { color: #7A8BAD; font-size: 12px; }

/* ── Combo / Spin ── */
QComboBox, QSpinBox {
    background: #F0F4FA;
    border: 1.5px solid #E4EAF5;
    border-radius: 10px;
    color: #1A2340;
    padding: 8px 14px;
    font-size: 13px;
    min-width: 80px;
}
QComboBox:focus, QSpinBox:focus { border-color: #4B72B8; background: #FFFFFF; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView {
    background: #FFFFFF;
    border: 1px solid #E4EAF5;
    color: #1A2340;
    selection-background-color: #EDF2FC;
    outline: none;
}
QSpinBox::up-button, QSpinBox::down-button { width: 0; }

/* ── Bulk banner ── */
#bulkBanner {
    background: #FFF3E0;
    border-bottom: 1px solid #FFD180;
    min-height: 44px; max-height: 44px;
}
#bulkBannerLabel { color: #E65100; font-size: 13px; font-weight: 600; background: transparent; }

/* ── Dialog ── */
QDialog { background: #FFFFFF; }
#dlgTitle  { font-size: 16px; font-weight: 700; color: #1A2340; background: transparent; }
#dlgSep    { background: #E4EAF5; max-height: 1px; min-height: 1px; border: none; }
#detailCode{ font-size: 22px; font-weight: 700; color: #1A2340; background: transparent; }
#detailVal { color: #1A2340; font-size: 13px; background: transparent; }
#hintLabel { color: #7A8BAD; font-size: 11px; font-style: italic; background: transparent; }
QFormLayout QLabel { color: #7A8BAD; font-size: 12px; font-weight: 600; background: transparent; }
QDialog QWidget { background: #FFFFFF; }
QDialog QLineEdit { background: #F0F4FA; padding-left: 14px; }
QDialog QComboBox { background: #F0F4FA; }
QDialog QSpinBox  { background: #F0F4FA; }

/* ── Message boxes ── */
QMessageBox { background: #FFFFFF; }
QMessageBox QLabel { background: transparent; color: #1A2340; }
QMessageBox QPushButton { min-width: 80px; }
"""

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar nav button
# ─────────────────────────────────────────────────────────────────────────────

class NavButton(QPushButton):
    def __init__(self, icon, label, parent=None):
        super().__init__(f"  {icon}   {label}", parent)
        self.setObjectName("navBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(False)
        self._active = False

    def set_active(self, active: bool):
        self._active = active
        self.setObjectName("navBtnActive" if active else "navBtn")
        self.style().unpolish(self)
        self.style().polish(self)


# ─────────────────────────────────────────────────────────────────────────────
# Search box with search icon painted inside
# ─────────────────────────────────────────────────────────────────────────────

class SearchBox(QLineEdit):
    def __init__(self, placeholder="Search…", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)

    def paintEvent(self, e):
        super().paintEvent(e)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QColor("#7A8BAD"))
        p.setFont(QFont("Segoe UI", 11))
        p.drawText(12, 0, 20, self.height(), Qt.AlignmentFlag.AlignCenter, "🔍")
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# Table tab  (the main content pane for each section)
# ─────────────────────────────────────────────────────────────────────────────

class TableTab(QWidget):
    def __init__(self, title, subtitle, stat_icon,
                 columns, fetch_fn, add_fn, edit_fn,
                 delete_fn, detail_fn, delete_label="record", parent=None):
        super().__init__(parent)
        self.title        = title
        self.subtitle     = subtitle
        self.stat_icon    = stat_icon
        self.columns      = columns
        self.fetch_fn     = fetch_fn
        self.add_fn       = add_fn
        self.edit_fn      = edit_fn
        self.delete_fn    = delete_fn
        self.detail_fn    = detail_fn
        self.delete_label = delete_label

        self.current_page  = 1
        self.total_records = 0
        self.sort_col      = columns[0][1]
        self.sort_dir      = "ASC"

        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_search)

        self._build_ui()
        self.refresh()

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── page header
        hdr = QFrame(); hdr.setObjectName("pageHeader")
        hdr.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        hl = QHBoxLayout(hdr); hl.setContentsMargins(28, 18, 28, 18); hl.setSpacing(0)
        titles = QVBoxLayout(); titles.setSpacing(2)
        t = QLabel(self.title); t.setObjectName("pageTitle"); t.setStyleSheet("background:transparent;")
        s = QLabel(self.subtitle); s.setObjectName("pageSubtitle"); s.setStyleSheet("background:transparent;")
        titles.addWidget(t); titles.addWidget(s)
        hl.addLayout(titles)
        root.addWidget(hdr)

        # ── scrollable content
        content = QWidget(); content.setObjectName("contentArea")
        cl = QVBoxLayout(content); cl.setContentsMargins(24, 20, 24, 20); cl.setSpacing(16)

        # stats row
        stats_row = QHBoxLayout(); stats_row.setSpacing(14)
        self._total_card = self._make_stat_card(self.stat_icon, "0", "Total " + self.title)
        stats_row.addWidget(self._total_card)
        stats_row.addStretch()
        cl.addLayout(stats_row)

        # table card
        table_card = QFrame(); table_card.setObjectName("tableCard")
        tc = QVBoxLayout(table_card); tc.setSpacing(0); tc.setContentsMargins(0, 0, 0, 0)

        # toolbar inside card
        toolbar = QFrame(); toolbar.setObjectName("cardToolbar")
        toolbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        tb = QHBoxLayout(toolbar); tb.setContentsMargins(16, 14, 16, 14); tb.setSpacing(10)

        self.search_box = SearchBox(f"Search {self.title.lower()}…")
        self.search_box.textChanged.connect(self._on_search_changed)
        tb.addWidget(self.search_box)

        row_lbl = QLabel("Rows:"); row_lbl.setStyleSheet("color:#7A8BAD; font-size:12px; background:transparent;")
        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["10", "25", "50", "100"])
        self.per_page_combo.setCurrentText("25")
        self.per_page_combo.setFixedWidth(80)
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        tb.addWidget(row_lbl); tb.addWidget(self.per_page_combo)
        tb.addStretch()

        self.add_btn  = self._mk_btn("＋  Add",   "primaryBtn",   self._on_add)
        self.edit_btn = self._mk_btn("✎  Edit",   "secondaryBtn", self._on_edit,  False)
        self.del_btn  = self._mk_btn("🗑  Delete", "dangerBtn",    self._on_delete, False)
        tb.addWidget(self.edit_btn); tb.addWidget(self.del_btn); tb.addWidget(self.add_btn)
        tc.addWidget(toolbar)

        # bulk banner
        self.bulk_banner = QFrame(); self.bulk_banner.setObjectName("bulkBanner")
        bb = QHBoxLayout(self.bulk_banner); bb.setContentsMargins(16, 0, 16, 0); bb.setSpacing(10)
        self.bulk_label = QLabel(); self.bulk_label.setObjectName("bulkBannerLabel")
        b_del = self._mk_btn("Delete Selected", "dangerBtn",    self._on_bulk_delete)
        b_clr = self._mk_btn("Clear",           "cancelBtn",    self._clear_selection)
        bb.addWidget(self.bulk_label); bb.addStretch(); bb.addWidget(b_del); bb.addWidget(b_clr)
        self.bulk_banner.setVisible(False)
        tc.addWidget(self.bulk_banner)

        # separator
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: #E4EAF5; max-height:1px; border:none;")
        tc.addWidget(sep)

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
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_double_click)
        tc.addWidget(self.table, 1)

        # pagination footer
        pag_frame = QFrame()
        pag_frame.setStyleSheet("background:#FFFFFF; border-top: 1px solid #F0F4FA; border-radius: 0 0 14px 14px;")
        pl = QHBoxLayout(pag_frame); pl.setContentsMargins(16, 10, 16, 10); pl.setSpacing(6)
        self.page_info = QLabel(); self.page_info.setObjectName("pageInfo")
        self.page_info.setStyleSheet("background:transparent;")
        pl.addWidget(self.page_info); pl.addStretch()
        self.pag_container = QHBoxLayout(); self.pag_container.setSpacing(4)
        pl.addLayout(self.pag_container)
        tc.addWidget(pag_frame)

        cl.addWidget(table_card, 1)
        root.addWidget(content, 1)

    def _make_stat_card(self, icon, number, label):
        card = QFrame(); card.setObjectName("statCard")
        card.setFixedHeight(88); card.setFixedWidth(200)
        lay = QHBoxLayout(card); lay.setContentsMargins(18, 0, 18, 0); lay.setSpacing(14)

        icon_lbl = QLabel(icon); icon_lbl.setObjectName("statIcon")
        icon_lbl.setStyleSheet("background: #EDF2FC; border-radius: 10px; padding: 8px; background: transparent;")
        lay.addWidget(icon_lbl)

        txt = QVBoxLayout(); txt.setSpacing(2)
        self._stat_num = QLabel(number); self._stat_num.setObjectName("statNumber")
        self._stat_num.setStyleSheet("background:transparent;")
        lbl = QLabel(label.upper()); lbl.setObjectName("statLabel")
        lbl.setStyleSheet("background:transparent;")
        txt.addWidget(self._stat_num); txt.addWidget(lbl)
        lay.addLayout(txt)
        card._num_lbl = self._stat_num
        return card

    def _mk_btn(self, text, obj, slot, enabled=True):
        b = QPushButton(text); b.setObjectName(obj)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setEnabled(enabled); b.clicked.connect(slot)
        return b

    # ── data ──────────────────────────────────────────────────────────────────
    def refresh(self):
        search   = self.search_box.text().strip()
        per_page = int(self.per_page_combo.currentText())
        rows, total = self.fetch_fn(search=search, sort_col=self.sort_col,
                                    sort_dir=self.sort_dir, page=self.current_page,
                                    per_page=per_page)
        self.total_records = total
        self._total_card._num_lbl.setText(f"{total:,}")
        self._populate(rows)
        self._update_pagination(total, per_page)

    def _populate(self, rows):
        self.table.setRowCount(0)
        self._update_selection_ui()
        for row_data in rows:
            r = self.table.rowCount(); self.table.insertRow(r)
            for ci, (_, key) in enumerate(self.columns):
                val = str(row_data.get(key) if row_data.get(key) is not None else "N/A")
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, row_data)
                self.table.setItem(r, ci, item)
            self.table.setRowHeight(r, 46)

    def _update_pagination(self, total, per_page):
        total_pages = max(1, (total + per_page - 1) // per_page)
        if self.current_page > total_pages: self.current_page = total_pages
        start = (self.current_page - 1) * per_page + 1
        end   = min(self.current_page * per_page, total)
        self.page_info.setText(f"Showing {start}–{end} of {total:,}")

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
                d.setStyleSheet("background:transparent;")
                d.setAlignment(Qt.AlignmentFlag.AlignCenter); d.setFixedWidth(24)
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

    def _go_page(self, page): self.current_page = page; self.refresh()

    # ── events ────────────────────────────────────────────────────────────────
    def _on_search_changed(self): self.current_page = 1; self._search_timer.start(300)
    def _do_search(self): self.refresh()
    def _on_per_page_changed(self): self.current_page = 1; self.refresh()

    def _on_header_clicked(self, idx):
        key = self.columns[idx][1]
        self.sort_dir = "DESC" if self.sort_col == key and self.sort_dir == "ASC" else "ASC"
        self.sort_col = key; self.current_page = 1; self.refresh()

    def _on_selection_changed(self): self._update_selection_ui()

    def _update_selection_ui(self):
        sel = self._selected_rows(); n = len(sel)
        self.edit_btn.setEnabled(n == 1)
        self.del_btn.setEnabled(n == 1)
        self.bulk_banner.setVisible(n > 1)
        if n > 1:
            self.bulk_label.setText(f"  {n} rows selected")

    def _selected_rows(self):
        seen, rows = set(), []
        for item in self.table.selectedItems():
            r = item.row()
            if r not in seen:
                seen.add(r); rows.append(item.data(Qt.ItemDataRole.UserRole))
        return rows

    def _clear_selection(self): self.table.clearSelection()

    def _on_add(self):
        if self.add_fn(self).exec(): self.refresh()

    def _on_edit(self):
        rows = self._selected_rows()
        if rows and self.edit_fn(self, rows[0]).exec(): self.refresh()

    def _on_double_click(self, index):
        item = self.table.item(index.row(), 0)
        if item: self.detail_fn(self, item.data(Qt.ItemDataRole.UserRole)).exec()

    def _on_delete(self): self._confirm_and_delete(self._selected_rows())
    def _on_bulk_delete(self): self._confirm_and_delete(self._selected_rows())

    def _confirm_and_delete(self, rows):
        if not rows: return
        n = len(rows)
        name = (rows[0].get("name") or rows[0].get("id") or "this record") if n == 1 else f"{n} {self.delete_label}s"
        if QMessageBox.question(self, "Confirm Delete",
                                f"<b>Delete {name}?</b><br><br>This cannot be undone.",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
                                ) != QMessageBox.StandardButton.Yes:
            return
        errors = [err for row in rows for ok, err in [self.delete_fn(row)] if not ok]
        if errors: QMessageBox.warning(self, "Some deletions failed", "\n".join(set(errors)))
        self.refresh()


# ─────────────────────────────────────────────────────────────────────────────
# DB wrappers
# ─────────────────────────────────────────────────────────────────────────────
def _del_college(row): return db.college_delete(row["code"])
def _del_program(row): return db.program_delete(row["code"])
def _del_student(row): return db.student_delete(row["id"])


# ─────────────────────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSU-IIT Student Information System")
        self.setMinimumSize(1100, 680); self.resize(1340, 820)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        root_widget = QWidget()
        root_widget.setStyleSheet("background: #F0F4FA;")
        self.setCentralWidget(root_widget)
        root = QHBoxLayout(root_widget)
        root.setSpacing(0); root.setContentsMargins(0, 0, 0, 0)

        # ── Sidebar ────────────────────────────────────────────────────────────
        sidebar = QFrame(); sidebar.setObjectName("sidebar")
        sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sl = QVBoxLayout(sidebar); sl.setSpacing(0); sl.setContentsMargins(12, 0, 12, 20)

        # logo block
        logo_block = QWidget(); logo_block.setStyleSheet("background:transparent;")
        ll = QVBoxLayout(logo_block); ll.setContentsMargins(10, 22, 10, 18); ll.setSpacing(3)
        logo_title = QLabel("MSU-IIT SIS"); logo_title.setObjectName("sidebarLogo")
        logo_title.setStyleSheet("background:transparent;")
        logo_sub = QLabel("STUDENT INFORMATION SYSTEM"); logo_sub.setObjectName("sidebarSub")
        logo_sub.setStyleSheet("background:transparent;")
        logo_sub.setWordWrap(True)
        ll.addWidget(logo_title); ll.addWidget(logo_sub)
        sl.addWidget(logo_block)

        div = QFrame(); div.setObjectName("sidebarDivider"); sl.addWidget(div)
        sl.addSpacing(18)

        sect = QLabel("MANAGE"); sect.setObjectName("sidebarSectionLabel")
        sect.setStyleSheet("background:transparent;")
        sl.addWidget(sect); sl.addSpacing(8)

        # nav buttons
        self._nav_btns = []
        nav_items = [
            ("🎓", "Students"),
            ("📚", "Programs"),
            ("🏛", "Colleges"),
        ]
        for icon, label in nav_items:
            btn = NavButton(icon, label)
            btn.setFixedHeight(42)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            sl.addWidget(btn)
            self._nav_btns.append(btn)

        sl.addStretch()

        # version footer
        ver = QLabel("v2.0  ·  SQLite"); ver.setObjectName("sidebarSub")
        ver.setStyleSheet("background:transparent; padding: 0 10px;")
        sl.addWidget(ver)
        root.addWidget(sidebar)

        # ── Stacked content ────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setObjectName("contentArea")

        student_tab = TableTab(
            title="Students", subtitle="Manage enrolled students",
            stat_icon="🎓",
            columns=[("Student ID","id"),("First Name","firstname"),("Last Name","lastname"),
                     ("Program","course"),("Year","year"),("Gender","gender")],
            fetch_fn=db.student_list,
            add_fn=lambda p: StudentDialog(p),
            edit_fn=lambda p, row: StudentDialog(p, db.student_get(row["id"])),
            delete_fn=_del_student,
            detail_fn=lambda p, row: StudentDetailDialog(p, db.student_get(row["id"])),
            delete_label="student",
        )
        program_tab = TableTab(
            title="Programs", subtitle="Manage academic programs",
            stat_icon="📚",
            columns=[("Code","code"),("Program Name","name"),("College","college"),("# Students","student_count")],
            fetch_fn=db.program_list,
            add_fn=lambda p: ProgramDialog(p),
            edit_fn=lambda p, row: ProgramDialog(p, db.program_get(row["code"])),
            delete_fn=_del_program,
            detail_fn=lambda p, row: ProgramDetailDialog(p, db.program_get_detail(row["code"])),
            delete_label="program",
        )
        college_tab = TableTab(
            title="Colleges", subtitle="Manage colleges and faculties",
            stat_icon="🏛",
            columns=[("Code","code"),("College Name","name"),("# Programs","program_count")],
            fetch_fn=db.college_list,
            add_fn=lambda p: CollegeDialog(p),
            edit_fn=lambda p, row: CollegeDialog(p, db.college_get(row["code"])),
            delete_fn=_del_college,
            detail_fn=lambda p, row: CollegeDetailDialog(p, db.college_get_detail(row["code"])),
            delete_label="college",
        )

        self._tabs = [student_tab, program_tab, college_tab]
        for tab in self._tabs:
            self._stack.addWidget(tab)

        root.addWidget(self._stack, 1)

        # wire nav buttons
        for i, btn in enumerate(self._nav_btns):
            btn.clicked.connect(lambda _, idx=i: self._switch_tab(idx))

        self._switch_tab(0)

    def _switch_tab(self, idx):
        self._stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._nav_btns):
            btn.set_active(i == idx)


# ─────────────────────────────────────────────────────────────────────────────
def main():
    db.init_db()
    seed()
    app = QApplication(sys.argv)
    app.setApplicationName("MSU-IIT SIS")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
