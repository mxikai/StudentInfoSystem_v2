"""
main.py — Simple Student Information System
Dark indigo theme (default) + light mode toggle.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QFrame, QMessageBox,
    QComboBox, QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

import database as db
from dialogs import (CollegeDialog, ProgramDialog, StudentDialog,
                     CollegeDetailDialog, ProgramDetailDialog, StudentDetailDialog)
from seed import seed

# ─────────────────────────────────────────────────────────────────────────────
# Themes
# ─────────────────────────────────────────────────────────────────────────────

DARK = dict(
    bg          = "#0f1117",
    bg2         = "#13151f",
    bg3         = "#1a1d2e",
    border      = "#1e2130",
    border2     = "#2d3352",
    accent      = "#6366f1",
    accent_hov  = "#818cf8",
    accent_press= "#4f46e5",
    danger      = "#ef4444",
    danger_hov  = "#f87171",
    text        = "#e2e8f0",
    text_muted  = "#64748b",
    text_head   = "#f8fafc",
    text_sub    = "#94a3b8",
    sel_bg      = "#1e2237",
    sel_text    = "#f1f5f9",
    alt_row     = "#111420",
    scroll_bg   = "#0f1117",
    scroll_hand = "#2d3352",
    tab_sel_fg  = "#6366f1",
    stat_num    = "#6366f1",
    bulk_bg     = "#1a1d2e",
    bulk_fg     = "#e2e8f0",
    bulk_border = "#2d3352",
    dlg_bg      = "#0f1117",
    dlg_field   = "#1a1d2e",
    toggle_bg   = "#1a1d2e",
    toggle_fg   = "#94a3b8",
    toggle_icon = "☀️",
    toggle_tip  = "Switch to Light Mode",
)

LIGHT = dict(
    bg          = "#f8fafc",
    bg2         = "#ffffff",
    bg3         = "#f1f5f9",
    border      = "#e2e8f0",
    border2     = "#cbd5e1",
    accent      = "#6366f1",
    accent_hov  = "#4f46e5",
    accent_press= "#3730a3",
    danger      = "#ef4444",
    danger_hov  = "#dc2626",
    text        = "#0f172a",
    text_muted  = "#64748b",
    text_head   = "#0f172a",
    text_sub    = "#475569",
    sel_bg      = "#ede9fe",
    sel_text    = "#312e81",
    alt_row     = "#f8fafc",
    scroll_bg   = "#f1f5f9",
    scroll_hand = "#cbd5e1",
    tab_sel_fg  = "#6366f1",
    stat_num    = "#6366f1",
    bulk_bg     = "#ede9fe",
    bulk_fg     = "#3730a3",
    bulk_border = "#c7d2fe",
    dlg_bg      = "#ffffff",
    dlg_field   = "#f1f5f9",
    toggle_bg   = "#e2e8f0",
    toggle_fg   = "#475569",
    toggle_icon = "🌙",
    toggle_tip  = "Switch to Dark Mode",
)

def build_style(t):
    return f"""
* {{
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}
QMainWindow, QDialog {{ background: {t['bg']}; color: {t['text']}; }}
QWidget {{ background: {t['bg']}; color: {t['text']}; }}

/* ── Header ── */
#header {{
    background: {t['bg2']};
    border-bottom: 1px solid {t['border']};
    min-height: 64px; max-height: 64px;
}}
#appTitle {{
    font-size: 18px; font-weight: 700;
    color: {t['text_head']}; letter-spacing: 0.5px;
    background: {t['bg2']};
}}
#appSubtitle {{
    font-size: 10px; color: {t['text_muted']};
    letter-spacing: 1.6px; background: {t['bg2']};
}}

/* ── Theme toggle ── */
#themeToggle {{
    background: {t['toggle_bg']};
    color: {t['toggle_fg']};
    border: 1px solid {t['border2']};
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 13px;
    font-weight: 500;
}}
#themeToggle:hover {{ background: {t['border2']}; }}

/* ── Stats bar ── */
#statsBar {{
    background: {t['bg2']};
    border-bottom: 1px solid {t['border']};
}}
#statCard {{
    background: {t['bg3']};
    border: 1px solid {t['border']};
    border-radius: 10px;
    padding: 12px 20px;
    min-width: 140px;
}}
#statNumber {{ font-size: 26px; font-weight: 700; color: {t['stat_num']}; background: {t['bg3']}; }}
#statLabel  {{ font-size: 10px; color: {t['text_muted']}; letter-spacing: 1.2px; background: {t['bg3']}; }}

/* ── Tabs ── */
QTabWidget::pane {{ border: none; background: {t['bg']}; }}
QTabBar {{ background: {t['bg2']}; }}
QTabBar::tab {{
    background: transparent;
    color: {t['text_muted']};
    padding: 13px 28px;
    font-size: 13px; font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-right: 2px;
}}
QTabBar::tab:selected  {{ color: {t['tab_sel_fg']}; border-bottom: 2px solid {t['tab_sel_fg']}; }}
QTabBar::tab:hover:!selected {{ color: {t['text_sub']}; }}

/* ── Toolbar ── */
#toolbar {{
    background: {t['bg2']};
    border-bottom: 1px solid {t['border']};
    min-height: 56px; max-height: 56px;
}}

/* ── Search ── */
QLineEdit {{
    background: {t['bg3']};
    border: 1px solid {t['border']};
    border-radius: 8px;
    color: {t['text']};
    padding: 8px 14px;
    font-size: 13px;
    min-width: 260px;
}}
QLineEdit:focus {{ border-color: {t['accent']}; }}

/* ── Buttons ── */
QPushButton {{
    border-radius: 8px; padding: 8px 18px;
    font-size: 13px; font-weight: 500; border: none;
}}
#primaryBtn  {{ background: {t['accent']}; color: #fff; padding: 8px 22px; }}
#primaryBtn:hover   {{ background: {t['accent_hov']}; }}
#primaryBtn:pressed {{ background: {t['accent_press']}; }}
#dangerBtn   {{ background: {t['danger']}; color: #fff; }}
#dangerBtn:hover  {{ background: {t['danger_hov']}; }}
#dangerBtn:disabled {{ background: {t['bg3']}; color: {t['text_muted']}; }}
#secondaryBtn {{
    background: {t['bg3']};
    color: {t['text_sub']};
    border: 1px solid {t['border2']};
}}
#secondaryBtn:hover {{ background: {t['border']}; color: {t['text']}; }}
#secondaryBtn:disabled {{ color: {t['text_muted']}; }}
#cancelBtn {{
    background: {t['bg3']};
    color: {t['text_sub']};
    border: 1px solid {t['border2']};
    padding: 8px 18px;
}}
#cancelBtn:hover {{ background: {t['border']}; color: {t['text']}; }}

/* ── Table ── */
QTableWidget {{
    background: {t['bg']};
    border: none;
    gridline-color: {t['bg3']};
    color: {t['text']};
    font-size: 13px;
    selection-background-color: {t['sel_bg']};
    alternate-background-color: {t['alt_row']};
    outline: none;
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {t['bg3']};
}}
QTableWidget::item:selected {{
    background: {t['sel_bg']};
    color: {t['sel_text']};
}}
QHeaderView::section {{
    background: {t['bg2']};
    color: {t['text_muted']};
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.8px;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid {t['border']};
    border-right: 1px solid {t['border']};
    text-transform: uppercase;
}}
QHeaderView::section:hover {{ color: {t['text']}; background: {t['bg3']}; }}
QHeaderView {{ background: {t['bg2']}; }}

/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: {t['scroll_bg']}; width: 8px; border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {t['scroll_hand']}; border-radius: 4px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {t['accent']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Pagination ── */
#pageBtn {{
    background: {t['bg3']};
    color: {t['text_muted']};
    border: 1px solid {t['border2']};
    border-radius: 6px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px;
}}
#pageBtn:hover {{ background: {t['border']}; color: {t['text']}; }}
#pageBtnActive {{
    background: {t['accent']}; color: #fff;
    border: none; border-radius: 6px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px; font-weight: 700;
}}
#pageInfo {{ color: {t['text_muted']}; font-size: 12px; background: {t['bg2']}; }}

/* ── Combo / Spin ── */
QComboBox, QSpinBox {{
    background: {t['bg3']};
    border: 1px solid {t['border']};
    border-radius: 8px;
    color: {t['text']};
    padding: 7px 14px;
    font-size: 13px;
}}
QComboBox:focus, QSpinBox:focus {{ border-color: {t['accent']}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    background: {t['bg3']};
    border: 1px solid {t['border2']};
    color: {t['text']};
    selection-background-color: {t['accent']};
    outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 0; border: none; }}

/* ── Bulk banner ── */
#bulkBanner {{
    background: {t['bulk_bg']};
    border-bottom: 1px solid {t['bulk_border']};
    min-height: 44px; max-height: 44px;
}}
#bulkBannerLabel {{
    color: {t['bulk_fg']};
    font-size: 13px; font-weight: 500;
    background: {t['bulk_bg']};
}}

/* ── Dialogs ── */
QDialog {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QDialog QWidget {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QDialog QLineEdit {{ background: {t['dlg_field']}; padding-left: 14px; }}
QDialog QComboBox {{ background: {t['dlg_field']}; }}
QDialog QSpinBox  {{ background: {t['dlg_field']}; }}
#dlgTitle  {{ font-size: 16px; font-weight: 700; color: {t['text_head']}; background: {t['dlg_bg']}; }}
#dlgSep    {{ background: {t['border']}; max-height: 1px; min-height: 1px; border: none; color: {t['border']}; }}
#detailCode{{ font-size: 20px; font-weight: 700; color: {t['accent']}; background: {t['dlg_bg']}; }}
#detailVal {{ color: {t['text']}; font-size: 13px; background: {t['dlg_bg']}; }}
#hintLabel {{ color: {t['text_muted']}; font-size: 11px; font-style: italic; background: {t['dlg_bg']}; }}
QFormLayout QLabel {{ color: {t['text_muted']}; font-size: 12px; font-weight: 500; background: {t['dlg_bg']}; }}

/* ── Message boxes ── */
QMessageBox {{ background: {t['dlg_bg']}; }}
QMessageBox QLabel {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QMessageBox QPushButton {{ min-width: 80px; }}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Table Tab
# ─────────────────────────────────────────────────────────────────────────────

class TableTab(QWidget):
    def __init__(self, columns, fetch_fn, add_fn, edit_fn,
                 delete_fn, detail_fn, delete_label="record", parent=None):
        super().__init__(parent)
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

        row_lbl = QLabel("Rows:")
        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["10", "25", "50", "100"])
        self.per_page_combo.setCurrentText("25")
        self.per_page_combo.setFixedWidth(72)
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        tb.addWidget(row_lbl); tb.addWidget(self.per_page_combo)
        tb.addStretch()

        self.add_btn  = self._mk_btn("＋  Add",   "primaryBtn",   self._on_add)
        self.edit_btn = self._mk_btn("✎  Edit",   "secondaryBtn", self._on_edit,  False)
        self.del_btn  = self._mk_btn("🗑  Delete", "dangerBtn",    self._on_delete, False)
        tb.addWidget(self.edit_btn); tb.addWidget(self.del_btn); tb.addWidget(self.add_btn)
        root.addWidget(toolbar)

        # bulk banner
        self.bulk_banner = QFrame(); self.bulk_banner.setObjectName("bulkBanner")
        bb = QHBoxLayout(self.bulk_banner); bb.setContentsMargins(20, 0, 20, 0); bb.setSpacing(10)
        self.bulk_label = QLabel(); self.bulk_label.setObjectName("bulkBannerLabel")
        b_del = self._mk_btn("🗑  Delete Selected", "dangerBtn",  self._on_bulk_delete)
        b_clr = self._mk_btn("✕  Clear",            "cancelBtn",  self._clear_selection)
        bb.addWidget(self.bulk_label); bb.addStretch()
        bb.addWidget(b_del); bb.addWidget(b_clr)
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
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_double_click)
        root.addWidget(self.table, 1)

        # pagination
        pag_frame = QFrame(); pag_frame.setObjectName("toolbar")
        pl = QHBoxLayout(pag_frame); pl.setContentsMargins(20, 8, 20, 8); pl.setSpacing(4)
        self.page_info = QLabel(); self.page_info.setObjectName("pageInfo")
        pl.addWidget(self.page_info); pl.addStretch()
        self.pag_container = QHBoxLayout(); self.pag_container.setSpacing(4)
        pl.addLayout(self.pag_container)
        root.addWidget(pag_frame)

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
            self.table.setRowHeight(r, 44)

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
            self.bulk_label.setText(f"  {n} rows selected — bulk operations enabled")

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
        name = (rows[0].get("name") or rows[0].get("id") or "this record") if n == 1 \
               else f"{n} {self.delete_label}s"
        if QMessageBox.question(
                self, "Confirm Delete",
                f"<b>Delete {name}?</b><br><br>This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        ) != QMessageBox.StandardButton.Yes:
            return
        errors = [err for row in rows
                  for ok, err in [self.delete_fn(row)] if not ok]
        if errors:
            QMessageBox.warning(self, "Some deletions failed", "\n".join(set(errors)))
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
        self.setMinimumSize(1100, 680); self.resize(1300, 800)
        self._dark = True
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central); root.setSpacing(0); root.setContentsMargins(0, 0, 0, 0)

        # ── Header
        header = QFrame(); header.setObjectName("header")
        hl = QHBoxLayout(header); hl.setContentsMargins(24, 0, 24, 0); hl.setSpacing(0)

        title_col = QVBoxLayout(); title_col.setSpacing(2)
        self.app_title = QLabel("MSU-IIT Student Information System")
        self.app_title.setObjectName("appTitle")
        self.app_sub = QLabel("MINDANAO STATE UNIVERSITY  ·  ILIGAN INSTITUTE OF TECHNOLOGY")
        self.app_sub.setObjectName("appSubtitle")
        title_col.addWidget(self.app_title); title_col.addWidget(self.app_sub)
        hl.addLayout(title_col); hl.addStretch()

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("themeToggle")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setFixedHeight(34)
        self.theme_btn.clicked.connect(self._toggle_theme)
        hl.addWidget(self.theme_btn)
        root.addWidget(header)

        # ── Stats bar
        stats_bar = QFrame(); stats_bar.setObjectName("statsBar")
        sb = QHBoxLayout(stats_bar); sb.setContentsMargins(24, 12, 24, 12); sb.setSpacing(12)
        self.stat_students = self._make_stat_card("0", "Students")
        self.stat_programs = self._make_stat_card("0", "Programs")
        self.stat_colleges = self._make_stat_card("0", "Colleges")
        sb.addWidget(self.stat_students); sb.addWidget(self.stat_programs)
        sb.addWidget(self.stat_colleges); sb.addStretch()
        refresh_btn = QPushButton("↻  Refresh Stats")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self._refresh_stats)
        sb.addWidget(refresh_btn)
        root.addWidget(stats_bar)

        # ── Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.student_tab = TableTab(
            columns=[("Student ID","id"),("First Name","firstname"),("Last Name","lastname"),
                     ("Program","course"),("Year","year"),("Gender","gender")],
            fetch_fn=db.student_list,
            add_fn=lambda p: StudentDialog(p),
            edit_fn=lambda p, r: StudentDialog(p, db.student_get(r["id"])),
            delete_fn=_del_student,
            detail_fn=lambda p, r: StudentDetailDialog(p, db.student_get(r["id"])),
            delete_label="student",
        )
        self.program_tab = TableTab(
            columns=[("Code","code"),("Program Name","name"),
                     ("College","college"),("# Students","student_count")],
            fetch_fn=db.program_list,
            add_fn=lambda p: ProgramDialog(p),
            edit_fn=lambda p, r: ProgramDialog(p, db.program_get(r["code"])),
            delete_fn=_del_program,
            detail_fn=lambda p, r: ProgramDetailDialog(p, db.program_get_detail(r["code"])),
            delete_label="program",
        )
        self.college_tab = TableTab(
            columns=[("Code","code"),("College Name","name"),("# Programs","program_count")],
            fetch_fn=db.college_list,
            add_fn=lambda p: CollegeDialog(p),
            edit_fn=lambda p, r: CollegeDialog(p, db.college_get(r["code"])),
            delete_fn=_del_college,
            detail_fn=lambda p, r: CollegeDetailDialog(p, db.college_get_detail(r["code"])),
            delete_label="college",
        )

        self.tabs.addTab(self.student_tab,  "  🎓  Students  ")
        self.tabs.addTab(self.program_tab,  "  📚  Programs  ")
        self.tabs.addTab(self.college_tab,  "  🏛  Colleges  ")
        self.tabs.currentChanged.connect(lambda _: self._refresh_stats())
        root.addWidget(self.tabs, 1)

        self._refresh_stats()

    def _make_stat_card(self, number, label):
        card = QFrame(); card.setObjectName("statCard")
        lay = QVBoxLayout(card); lay.setContentsMargins(0, 0, 0, 0); lay.setSpacing(2)
        num = QLabel(number); num.setObjectName("statNumber")
        lbl = QLabel(label.upper()); lbl.setObjectName("statLabel")
        lay.addWidget(num); lay.addWidget(lbl)
        card._num_lbl = num
        return card

    def _refresh_stats(self):
        s, p, c = db.get_stats()
        self.stat_students._num_lbl.setText(f"{s:,}")
        self.stat_programs._num_lbl.setText(f"{p:,}")
        self.stat_colleges._num_lbl.setText(f"{c:,}")

    def _toggle_theme(self):
        self._dark = not self._dark
        self._apply_theme()

    def _apply_theme(self):
        t = DARK if self._dark else LIGHT
        style = build_style(t)
        self.setStyleSheet(style)
        QApplication.instance().setStyleSheet(style)
        icon = t["toggle_icon"]
        label = "Light mode" if self._dark else "Dark mode"
        self.theme_btn.setText(f"{icon}  {label}")
        self.theme_btn.setToolTip(t["toggle_tip"])


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
