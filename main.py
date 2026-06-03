"""
main.py — Simple Student Information System
Dark indigo theme (default) + animated pill toggle for light/dark switch.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QLabel, QFrame, QMessageBox,
    QComboBox, QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve,
                           pyqtProperty, QRectF, QPointF)
from PyQt6.QtGui import (QFont, QColor, QPainter, QPainterPath,
                          QBrush, QPen, QLinearGradient)

import database as db
from dialogs import (CollegeDialog, ProgramDialog, StudentDialog,
                     CollegeDetailDialog, ProgramDetailDialog, StudentDetailDialog)
from seed import seed

# ─────────────────────────────────────────────────────────────────────────────
# Themes
# ─────────────────────────────────────────────────────────────────────────────
DARK = dict(
    bg="#0f1117", bg2="#13151f", bg3="#1a1d2e",
    border="#1e2130", border2="#2d3352",
    accent="#6366f1", accent_hov="#818cf8", accent_press="#4f46e5",
    danger="#ef4444", danger_hov="#f87171",
    text="#e2e8f0", text_muted="#64748b", text_head="#f8fafc", text_sub="#94a3b8",
    sel_bg="#1e2237", sel_text="#f1f5f9", alt_row="#111420",
    scroll_bg="#0f1117", scroll_hand="#2d3352",
    tab_sel_fg="#6366f1", stat_num="#6366f1",
    bulk_bg="#1a1d2e", bulk_fg="#e2e8f0", bulk_border="#2d3352",
    dlg_bg="#0f1117", dlg_field="#1a1d2e",
    # toggle pill colours
    pill_track="#2d3352", pill_knob="#e2e8f0",
    pill_text="#94a3b8", pill_icon="🌙",
    pill_label="NIGHT MODE",
)

LIGHT = dict(
    bg="#f8fafc", bg2="#ffffff", bg3="#f1f5f9",
    border="#e2e8f0", border2="#cbd5e1",
    accent="#6366f1", accent_hov="#4f46e5", accent_press="#3730a3",
    danger="#ef4444", danger_hov="#dc2626",
    text="#0f172a", text_muted="#64748b", text_head="#0f172a", text_sub="#475569",
    sel_bg="#ede9fe", sel_text="#312e81", alt_row="#f8fafc",
    scroll_bg="#f1f5f9", scroll_hand="#cbd5e1",
    tab_sel_fg="#6366f1", stat_num="#6366f1",
    bulk_bg="#ede9fe", bulk_fg="#3730a3", bulk_border="#c7d2fe",
    dlg_bg="#ffffff", dlg_field="#f1f5f9",
    pill_track="#e2e8f0", pill_knob="#475569",
    pill_text="#475569", pill_icon="☀️",
    pill_label="DAY MODE",
)

def build_style(t):
    return f"""
* {{ font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; font-size: 13px; }}
QMainWindow, QDialog {{ background: {t['bg']}; color: {t['text']}; }}
QWidget {{ background: {t['bg']}; color: {t['text']}; }}

#header {{
    background: {t['bg2']}; border-bottom: 1px solid {t['border']};
    min-height: 64px; max-height: 64px;
}}
#appTitle {{
    font-size: 18px; font-weight: 700; color: {t['text_head']};
    letter-spacing: 0.5px; background: {t['bg2']};
}}
#appSubtitle {{
    font-size: 10px; color: {t['text_muted']};
    letter-spacing: 1.6px; background: {t['bg2']};
}}

#statsBar {{ background: {t['bg2']}; border-bottom: 1px solid {t['border']}; }}
#statCard {{
    background: {t['bg3']}; border: 1px solid {t['border']};
    border-radius: 10px; padding: 12px 20px; min-width: 140px;
}}
#statNumber {{ font-size: 26px; font-weight: 700; color: {t['stat_num']}; background: {t['bg3']}; }}
#statLabel  {{ font-size: 10px; color: {t['text_muted']}; letter-spacing: 1.2px; background: {t['bg3']}; }}

QTabWidget::pane {{ border: none; background: {t['bg']}; }}
QTabBar {{ background: {t['bg2']}; }}
QTabBar::tab {{
    background: transparent; color: {t['text_muted']};
    padding: 13px 28px; font-size: 13px; font-weight: 500;
    border-bottom: 2px solid transparent; margin-right: 2px;
}}
QTabBar::tab:selected  {{ color: {t['tab_sel_fg']}; border-bottom: 2px solid {t['tab_sel_fg']}; }}
QTabBar::tab:hover:!selected {{ color: {t['text_sub']}; }}

#toolbar {{
    background: {t['bg2']}; border-bottom: 1px solid {t['border']};
    min-height: 56px; max-height: 56px;
}}

QLineEdit {{
    background: {t['bg3']}; border: 1px solid {t['border']};
    border-radius: 8px; color: {t['text']};
    padding: 8px 14px; font-size: 13px; min-width: 260px;
}}
QLineEdit:focus {{ border-color: {t['accent']}; }}

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
    background: {t['bg3']}; color: {t['text_sub']};
    border: 1px solid {t['border2']};
}}
#secondaryBtn:hover {{ background: {t['border']}; color: {t['text']}; }}
#secondaryBtn:disabled {{ color: {t['text_muted']}; }}
#cancelBtn {{
    background: {t['bg3']}; color: {t['text_sub']};
    border: 1px solid {t['border2']}; padding: 8px 18px;
}}
#cancelBtn:hover {{ background: {t['border']}; color: {t['text']}; }}

QTableWidget {{
    background: {t['bg']}; border: none;
    gridline-color: {t['bg3']}; color: {t['text']};
    font-size: 13px;
    selection-background-color: {t['sel_bg']};
    alternate-background-color: {t['alt_row']};
    outline: none;
}}
QTableWidget::item {{ padding: 10px 14px; border-bottom: 1px solid {t['bg3']}; }}
QTableWidget::item:selected {{ background: {t['sel_bg']}; color: {t['sel_text']}; }}
QHeaderView::section {{
    background: {t['bg2']}; color: {t['text_muted']};
    font-size: 11px; font-weight: 600; letter-spacing: 0.8px;
    padding: 10px 14px; border: none;
    border-bottom: 1px solid {t['border']};
    border-right: 1px solid {t['border']};
    text-transform: uppercase;
}}
QHeaderView::section:hover {{ color: {t['text']}; background: {t['bg3']}; }}
QHeaderView {{ background: {t['bg2']}; }}

QScrollBar:vertical {{ background: {t['scroll_bg']}; width: 8px; border-radius: 4px; }}
QScrollBar::handle:vertical {{
    background: {t['scroll_hand']}; border-radius: 4px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {t['accent']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

#pageBtn {{
    background: {t['bg3']}; color: {t['text_muted']};
    border: 1px solid {t['border2']}; border-radius: 6px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px;
}}
#pageBtn:hover {{ background: {t['border']}; color: {t['text']}; }}
#pageBtnActive {{
    background: {t['accent']}; color: #fff; border: none; border-radius: 6px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0; font-size: 13px; font-weight: 700;
}}
#pageInfo {{ color: {t['text_muted']}; font-size: 12px; background: {t['bg2']}; }}

QComboBox, QSpinBox {{
    background: {t['bg3']}; border: 1px solid {t['border']};
    border-radius: 8px; color: {t['text']};
    padding: 7px 14px; font-size: 13px;
}}
QComboBox:focus, QSpinBox:focus {{ border-color: {t['accent']}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    background: {t['bg3']}; border: 1px solid {t['border2']};
    color: {t['text']}; selection-background-color: {t['accent']};
    outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 0; border: none; }}

#bulkBanner {{
    background: {t['bulk_bg']}; border-bottom: 1px solid {t['bulk_border']};
    min-height: 44px; max-height: 44px;
}}
#bulkBannerLabel {{
    color: {t['bulk_fg']}; font-size: 13px; font-weight: 500;
    background: {t['bulk_bg']};
}}

QDialog {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QDialog QWidget {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QDialog QLineEdit {{ background: {t['dlg_field']}; padding-left: 14px; }}
QDialog QComboBox {{ background: {t['dlg_field']}; }}
QDialog QSpinBox  {{ background: {t['dlg_field']}; }}
#dlgTitle  {{ font-size: 16px; font-weight: 700; color: {t['text_head']}; background: {t['dlg_bg']}; }}
#dlgSep    {{ background: {t['border']}; max-height: 1px; min-height: 1px; border: none; }}
#detailCode{{ font-size: 20px; font-weight: 700; color: {t['accent']}; background: {t['dlg_bg']}; }}
#detailVal {{ color: {t['text']}; font-size: 13px; background: {t['dlg_bg']}; }}
#hintLabel {{ color: {t['text_muted']}; font-size: 11px; font-style: italic; background: {t['dlg_bg']}; }}
QFormLayout QLabel {{ color: {t['text_muted']}; font-size: 12px; font-weight: 500; background: {t['dlg_bg']}; }}
QMessageBox {{ background: {t['dlg_bg']}; }}
QMessageBox QLabel {{ background: {t['dlg_bg']}; color: {t['text']}; }}
QMessageBox QPushButton {{ min-width: 80px; }}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Animated pill toggle widget
# ─────────────────────────────────────────────────────────────────────────────

class PillToggle(QWidget):
    """
    A sliding pill toggle — icon on the active side, label on the other.
    Dark mode  → moon on LEFT,  "NIGHT MODE" on right.
    Light mode → sun  on RIGHT, "DAY MODE"   on left.
    Knob slides smoothly with a QPropertyAnimation.
    """
    toggled = __import__("PyQt6.QtCore", fromlist=["pyqtSignal"]).pyqtSignal(bool)

    PILL_W = 160
    PILL_H = 40
    KNOB_D = 34   # knob diameter

    def __init__(self, dark=True, parent=None):
        super().__init__(parent)
        self._dark  = dark              # True = dark/night mode active
        self._anim_t = 0.0 if dark else 1.0   # 0.0 = left, 1.0 = right

        self.setFixedSize(self.PILL_W, self.PILL_H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Animation: float 0→1 drives knob position
        self._anim = QPropertyAnimation(self, b"knob_pos", self)
        self._anim.setDuration(480)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    # pyqtProperty so QPropertyAnimation can drive it
    def _get_knob_pos(self): return self._anim_t
    def _set_knob_pos(self, v): self._anim_t = v; self.update()
    knob_pos = pyqtProperty(float, _get_knob_pos, _set_knob_pos)

    def set_dark(self, dark):
        self._dark = dark
        self._anim.stop()
        self._anim.setStartValue(self._anim_t)
        # knob on LEFT (0) = night/dark (moon)   knob on RIGHT (1) = day/light (sun)
        self._anim.setEndValue(0.0 if dark else 1.0)
        self._anim.start()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._dark = not self._dark
            self.set_dark(self._dark)
            self.toggled.emit(self._dark)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        W, H, KD = self.PILL_W, self.PILL_H, self.KNOB_D
        radius = H / 2

        # ── track colours depend on mode
        if self._dark:
            track_c = QColor("#2d3352")
            knob_c  = QColor("#e2e8f0")
            text_c  = QColor("#94a3b8")
            icon    = "🌙"
        else:
            track_c = QColor("#e2e8f0")
            knob_c  = QColor("#475569")
            text_c  = QColor("#475569")
            icon    = "☀️"

        # ── draw track (pill background)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, W, H), radius, radius)
        p.fillPath(path, QBrush(track_c))

        # ── draw label text
        label = "NIGHT MODE" if self._dark else "DAY MODE"
        p.setPen(text_c)
        f = QFont("Segoe UI", 8, QFont.Weight.Bold)
        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.2)
        p.setFont(f)

        # text on the side opposite the knob
        margin = KD + 6
        if self._dark:
            # knob on left → text on right
            text_rect = QRectF(margin, 0, W - margin - 4, H)
        else:
            # knob on right → text on left
            text_rect = QRectF(4, 0, W - margin - 4, H)
        p.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label)

        # ── compute knob x (interpolated)
        pad = (H - KD) / 2
        knob_x_min = pad                    # leftmost
        knob_x_max = W - KD - pad           # rightmost
        knob_x = knob_x_min + self._anim_t * (knob_x_max - knob_x_min)

        # ── draw knob shadow (soft)
        p.setPen(Qt.PenStyle.NoPen)
        shadow_c = QColor(0, 0, 0, 40)
        p.setBrush(QBrush(shadow_c))
        p.drawEllipse(QRectF(knob_x + 1, pad + 2, KD, KD))

        # ── draw knob
        p.setBrush(QBrush(knob_c))
        p.drawEllipse(QRectF(knob_x, pad, KD, KD))

        # ── draw icon on knob
        p.setPen(QColor(track_c))
        fi = QFont("Segoe UI Emoji", 14)
        p.setFont(fi)
        icon_rect = QRectF(knob_x, pad, KD, KD)
        p.drawText(icon_rect, Qt.AlignmentFlag.AlignCenter, icon)

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
# Fade overlay — covers the whole window while theme transitions
# ─────────────────────────────────────────────────────────────────────────────

class FadeOverlay(QWidget):
    """
    A semi-transparent black (or white) overlay that fades in then out,
    giving a smooth blur-fade illusion when the theme switches.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._opacity = 0.0
        self._dark_to_light = True
        self.hide()

    def set_opacity(self, v):
        self._opacity = v
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        # Use white flash for dark→light, dark flash for light→dark
        if self._dark_to_light:
            c = QColor(255, 255, 255, int(self._opacity * 255))
        else:
            c = QColor(0, 0, 0, int(self._opacity * 255))
        p.fillRect(self.rect(), c)
        p.end()

    def run(self, dark_to_light: bool, on_midpoint):
        """
        Fade in to full opacity, call on_midpoint (apply new theme),
        then fade back out.
        """
        self._dark_to_light = dark_to_light
        self._opacity = 0.0
        self.resize(self.parent().size())
        self.raise_()
        self.show()

        STEPS     = 18
        FADE_MS   = 12   # ms per step 

        self._step     = 0
        self._total    = STEPS
        self._midpoint = on_midpoint
        self._fired    = False

        self._timer = QTimer(self)
        self._timer.setInterval(FADE_MS)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _tick(self):
        self._step += 1
        half = self._total

        if self._step <= half:
            # fade in
            self._opacity = self._step / half
        else:
            # past peak — fire midpoint callback once at peak
            if not self._fired:
                self._fired = True
                self._midpoint()
            rel = self._step - half
            self._opacity = max(0.0, 1.0 - rel / half)

        if self._step >= self._total * 2:
            self._timer.stop()
            self._opacity = 0.0
            self.hide()

        self.update()


# ─────────────────────────────────────────────────────────────────────────────
# Table Tab
# ─────────────────────────────────────────────────────────────────────────────

class TableTab(QWidget):
    def __init__(self, columns, fetch_fn, add_fn, edit_fn,
                 delete_fn, detail_fn, delete_label="record", parent=None):
        super().__init__(parent)
        self.columns=columns; self.fetch_fn=fetch_fn; self.add_fn=add_fn
        self.edit_fn=edit_fn; self.delete_fn=delete_fn
        self.detail_fn=detail_fn; self.delete_label=delete_label
        self.current_page=1; self.total_records=0
        self.sort_col=columns[0][1]; self.sort_dir="ASC"
        self._search_timer=QTimer(); self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_search)
        self._build_ui(); self.refresh()

    def _build_ui(self):
        root=QVBoxLayout(self); root.setSpacing(0); root.setContentsMargins(0,0,0,0)

        # toolbar
        tb_frame=QFrame(); tb_frame.setObjectName("toolbar")
        tb=QHBoxLayout(tb_frame); tb.setContentsMargins(20,0,20,0); tb.setSpacing(10)
        self.search_box=QLineEdit(); self.search_box.setPlaceholderText("🔍  Search…")
        self.search_box.textChanged.connect(self._on_search_changed)
        tb.addWidget(self.search_box)
        tb.addWidget(QLabel("Rows:"))
        self.per_page_combo=QComboBox()
        self.per_page_combo.addItems(["10","25","50","100"])
        self.per_page_combo.setCurrentText("25"); self.per_page_combo.setFixedWidth(72)
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        tb.addWidget(self.per_page_combo); tb.addStretch()
        self.add_btn =self._mk_btn("＋  Add",  "primaryBtn",  self._on_add)
        self.edit_btn=self._mk_btn("✎  Edit",  "secondaryBtn",self._on_edit,  False)
        self.del_btn =self._mk_btn("🗑  Delete","dangerBtn",   self._on_delete,False)
        tb.addWidget(self.edit_btn); tb.addWidget(self.del_btn); tb.addWidget(self.add_btn)
        root.addWidget(tb_frame)

        # bulk banner
        self.bulk_banner=QFrame(); self.bulk_banner.setObjectName("bulkBanner")
        bb=QHBoxLayout(self.bulk_banner); bb.setContentsMargins(20,0,20,0); bb.setSpacing(10)
        self.bulk_label=QLabel(); self.bulk_label.setObjectName("bulkBannerLabel")
        b_del=self._mk_btn("🗑  Delete Selected","dangerBtn",self._on_bulk_delete)
        b_clr=self._mk_btn("✕  Clear","cancelBtn",self._clear_selection)
        bb.addWidget(self.bulk_label); bb.addStretch(); bb.addWidget(b_del); bb.addWidget(b_clr)
        self.bulk_banner.setVisible(False); root.addWidget(self.bulk_banner)

        # table
        self.table=QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c[0] for c in self.columns])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True); self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_double_click)
        root.addWidget(self.table,1)

        # pagination
        pag=QFrame(); pag.setObjectName("toolbar")
        pl=QHBoxLayout(pag); pl.setContentsMargins(20,8,20,8); pl.setSpacing(4)
        self.page_info=QLabel(); self.page_info.setObjectName("pageInfo")
        pl.addWidget(self.page_info); pl.addStretch()
        self.pag_container=QHBoxLayout(); self.pag_container.setSpacing(4)
        pl.addLayout(self.pag_container)
        root.addWidget(pag)

    def _mk_btn(self,text,obj,slot,enabled=True):
        b=QPushButton(text); b.setObjectName(obj)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setEnabled(enabled); b.clicked.connect(slot); return b

    def refresh(self):
        search=self.search_box.text().strip()
        per_page=int(self.per_page_combo.currentText())
        rows,total=self.fetch_fn(search=search,sort_col=self.sort_col,
                                 sort_dir=self.sort_dir,page=self.current_page,
                                 per_page=per_page)
        self.total_records=total
        self._populate(rows); self._update_pagination(total,per_page)

    def _populate(self,rows):
        self.table.setRowCount(0); self._update_selection_ui()
        for row_data in rows:
            r=self.table.rowCount(); self.table.insertRow(r)
            for ci,(_,key) in enumerate(self.columns):
                val=str(row_data.get(key) if row_data.get(key) is not None else "N/A")
                item=QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole,row_data)
                self.table.setItem(r,ci,item)
            self.table.setRowHeight(r,44)

    def _update_pagination(self,total,per_page):
        total_pages=max(1,(total+per_page-1)//per_page)
        if self.current_page>total_pages: self.current_page=total_pages
        start=(self.current_page-1)*per_page+1
        end=min(self.current_page*per_page,total)
        self.page_info.setText(f"Showing {start}–{end} of {total:,} records")
        while self.pag_container.count():
            w=self.pag_container.takeAt(0)
            if w.widget(): w.widget().deleteLater()
        def mkb(label,page,active=False):
            b=QPushButton(str(label))
            b.setObjectName("pageBtnActive" if active else "pageBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _,p=page:self._go_page(p)); return b
        self.pag_container.addWidget(mkb("‹",max(1,self.current_page-1)))
        prev=None
        for p in self._page_range(self.current_page,total_pages):
            if prev is not None and p-prev>1:
                d=QLabel("…"); d.setObjectName("pageInfo")
                d.setAlignment(Qt.AlignmentFlag.AlignCenter); d.setFixedWidth(24)
                self.pag_container.addWidget(d)
            self.pag_container.addWidget(mkb(p,p,active=(p==self.current_page)))
            prev=p
        self.pag_container.addWidget(mkb("›",min(total_pages,self.current_page+1)))

    def _page_range(self,cur,total):
        if total<=7: return list(range(1,total+1))
        pages={1,total}
        for d in range(-2,3):
            p=cur+d
            if 1<=p<=total: pages.add(p)
        return sorted(pages)

    def _go_page(self,page): self.current_page=page; self.refresh()
    def _on_search_changed(self): self.current_page=1; self._search_timer.start(300)
    def _do_search(self): self.refresh()
    def _on_per_page_changed(self): self.current_page=1; self.refresh()
    def _on_header_clicked(self,idx):
        key=self.columns[idx][1]
        self.sort_dir="DESC" if self.sort_col==key and self.sort_dir=="ASC" else "ASC"
        self.sort_col=key; self.current_page=1; self.refresh()
    def _on_selection_changed(self): self._update_selection_ui()
    def _update_selection_ui(self):
        sel=self._selected_rows(); n=len(sel)
        self.edit_btn.setEnabled(n==1); self.del_btn.setEnabled(n==1)
        self.bulk_banner.setVisible(n>1)
        if n>1: self.bulk_label.setText(f"  {n} rows selected — bulk operations enabled")
    def _selected_rows(self):
        seen,rows=set(),[]
        for item in self.table.selectedItems():
            r=item.row()
            if r not in seen: seen.add(r); rows.append(item.data(Qt.ItemDataRole.UserRole))
        return rows
    def _clear_selection(self): self.table.clearSelection()
    def _on_add(self):
        if self.add_fn(self).exec(): self.refresh()
    def _on_edit(self):
        rows=self._selected_rows()
        if rows and self.edit_fn(self,rows[0]).exec(): self.refresh()
    def _on_double_click(self,index):
        item=self.table.item(index.row(),0)
        if item: self.detail_fn(self,item.data(Qt.ItemDataRole.UserRole)).exec()
    def _on_delete(self): self._confirm_and_delete(self._selected_rows())
    def _on_bulk_delete(self): self._confirm_and_delete(self._selected_rows())
    def _confirm_and_delete(self,rows):
        if not rows: return
        n=len(rows)
        name=(rows[0].get("name") or rows[0].get("id") or "this record") if n==1 \
             else f"{n} {self.delete_label}s"
        if QMessageBox.question(self,"Confirm Delete",
            f"<b>Delete {name}?</b><br><br>This action cannot be undone.",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.Cancel
        )!=QMessageBox.StandardButton.Yes: return
        errors=[err for row in rows for ok,err in [self.delete_fn(row)] if not ok]
        if errors: QMessageBox.warning(self,"Some deletions failed","\n".join(set(errors)))
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
        self.setWindowTitle("Simple Student Information System")
        self.setMinimumSize(1100,680); self.resize(1300,800)
        self._dark=True
        self._build_ui()
        self._apply_theme(animate=False)

    def _build_ui(self):
        central=QWidget(); self.setCentralWidget(central)
        root=QVBoxLayout(central); root.setSpacing(0); root.setContentsMargins(0,0,0,0)

        # ── Header
        header=QFrame(); header.setObjectName("header")
        hl=QHBoxLayout(header); hl.setContentsMargins(24,0,24,0); hl.setSpacing(0)
        title_col=QVBoxLayout(); title_col.setSpacing(2)
        self.app_title=QLabel("Simple Student Information System")
        self.app_title.setObjectName("appTitle")
        self.app_sub=QLabel("MINDANAO STATE UNIVERSITY  ·  ILIGAN INSTITUTE OF TECHNOLOGY")
        self.app_sub.setObjectName("appSubtitle")
        title_col.addWidget(self.app_title); title_col.addWidget(self.app_sub)
        hl.addLayout(title_col); hl.addStretch()

        self.pill_toggle=PillToggle(dark=True)
        self.pill_toggle.toggled.connect(self._on_toggle)
        hl.addWidget(self.pill_toggle)
        root.addWidget(header)

        # ── Stats bar
        sb_frame=QFrame(); sb_frame.setObjectName("statsBar")
        sb=QHBoxLayout(sb_frame); sb.setContentsMargins(24,12,24,12); sb.setSpacing(12)
        self.stat_students=self._make_stat_card("0","Students")
        self.stat_programs=self._make_stat_card("0","Programs")
        self.stat_colleges=self._make_stat_card("0","Colleges")
        sb.addWidget(self.stat_students); sb.addWidget(self.stat_programs)
        sb.addWidget(self.stat_colleges); sb.addStretch()
        refresh_btn=QPushButton("↻  Refresh Stats")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self._refresh_stats)
        sb.addWidget(refresh_btn)
        root.addWidget(sb_frame)

        # ── Tabs
        self.tabs=QTabWidget(); self.tabs.setDocumentMode(True)

        self.student_tab=TableTab(
            columns=[("Student ID","id"),("First Name","firstname"),("Last Name","lastname"),
                     ("Program","course"),("Year","year"),("Gender","gender")],
            fetch_fn=db.student_list,
            add_fn=lambda p:StudentDialog(p),
            edit_fn=lambda p,r:StudentDialog(p,db.student_get(r["id"])),
            delete_fn=_del_student,
            detail_fn=lambda p,r:StudentDetailDialog(p,db.student_get(r["id"])),
            delete_label="student",
        )
        self.program_tab=TableTab(
            columns=[("Code","code"),("Program Name","name"),
                     ("College","college"),("# Students","student_count")],
            fetch_fn=db.program_list,
            add_fn=lambda p:ProgramDialog(p),
            edit_fn=lambda p,r:ProgramDialog(p,db.program_get(r["code"])),
            delete_fn=_del_program,
            detail_fn=lambda p,r:ProgramDetailDialog(p,db.program_get_detail(r["code"])),
            delete_label="program",
        )
        self.college_tab=TableTab(
            columns=[("Code","code"),("College Name","name"),("# Programs","program_count")],
            fetch_fn=db.college_list,
            add_fn=lambda p:CollegeDialog(p),
            edit_fn=lambda p,r:CollegeDialog(p,db.college_get(r["code"])),
            delete_fn=_del_college,
            detail_fn=lambda p,r:CollegeDetailDialog(p,db.college_get_detail(r["code"])),
            delete_label="college",
        )
        self.tabs.addTab(self.student_tab,"  🎓  Students  ")
        self.tabs.addTab(self.program_tab,"  📚  Programs  ")
        self.tabs.addTab(self.college_tab,"  🏛  Colleges  ")
        
        # Refresh stats AND refresh the active tab's table whenever a tab is clicked
        def _on_tab_changed(idx):
            self._refresh_stats()
            current_tab = self.tabs.widget(idx)
            if hasattr(current_tab, 'refresh'):
                current_tab.refresh()
                
        self.tabs.currentChanged.connect(_on_tab_changed)
        
        root.addWidget(self.tabs,1)

        # ── Fade overlay (on top of everything)
        self._overlay=FadeOverlay(central)

        self._refresh_stats()

    def resizeEvent(self,e):
        super().resizeEvent(e)
        if hasattr(self,"_overlay"):
            self._overlay.resize(self.centralWidget().size())

    def _make_stat_card(self,number,label):
        card=QFrame(); card.setObjectName("statCard")
        lay=QVBoxLayout(card); lay.setContentsMargins(0,0,0,0); lay.setSpacing(2)
        num=QLabel(number); num.setObjectName("statNumber")
        lbl=QLabel(label.upper()); lbl.setObjectName("statLabel")
        lay.addWidget(num); lay.addWidget(lbl)
        card._num_lbl=num; return card

    def _refresh_stats(self):
        s,p,c=db.get_stats()
        self.stat_students._num_lbl.setText(f"{s:,}")
        self.stat_programs._num_lbl.setText(f"{p:,}")
        self.stat_colleges._num_lbl.setText(f"{c:,}")

    def _on_toggle(self, dark: bool):
        self._dark=dark
        self._apply_theme(animate=True)

    def _apply_theme(self, animate=True):
        t = DARK if self._dark else LIGHT
        style = build_style(t)

        if not animate:
            QApplication.instance().setStyleSheet(style)
            self.setStyleSheet(style)
            return

        going_light = not self._dark

        def apply_now():
            QApplication.instance().setStyleSheet(style)
            self.setStyleSheet(style)

        self._overlay.run(dark_to_light=going_light, on_midpoint=apply_now)


# ─────────────────────────────────────────────────────────────────────────────
def main():
    db.init_db(); seed()
    app=QApplication(sys.argv)
    app.setApplicationName("MSU-IIT SIS")
    win=MainWindow(); win.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()
