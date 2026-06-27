#!/usr/bin/env python3
import json
import base64
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QTextEdit, QComboBox, QPushButton,
    QSplitter, QLineEdit, QFileDialog,
    QSizePolicy, QFrame, QToolBar, QStatusBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon, QColor, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

CONFIG_DIR  = Path.home() / ".config" / "gpt-image-gen"
CONFIG_FILE = CONFIG_DIR / "config.json"

QUALITIES   = ["auto", "low", "medium", "high"]
FORMATS     = ["png", "jpeg", "webp"]

# ── Palette macOS ──────────────────────────────────────────────────────────────
C = {
    "window":      "#ECECEC",
    "sidebar":     "#F2F2F7",
    "surface":     "#FFFFFF",
    "toolbar_t":   "#F6F6F6",
    "toolbar_b":   "#DCDCDC",
    "border":      "#C7C7CC",
    "border_l":    "#E5E5EA",
    "accent":      "#007AFF",
    "accent_h":    "#0071E3",
    "accent_p":    "#005CC5",
    "accent_dim":  "#E1EDFF",
    "text":        "#1C1C1E",
    "text2":       "#6C6C70",
    "text3":       "#AEAEB2",
    "danger":      "#FF3B30",
    "danger_dim":  "#FFF0EF",
    "success":     "#34C759",
    "btn_grad_t":  "#FFFFFF",
    "btn_grad_b":  "#F0F0F0",
    "input_bg":    "#FFFFFF",
    "section_bg":  "#F2F2F7",
}

APP_STYLE = f"""
* {{
    font-family: "SF Pro Display", "-apple-system", "BlinkMacSystemFont",
                 "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: {C['text']};
}}

QMainWindow {{
    background: {C['window']};
}}

QWidget {{
    background: transparent;
}}

/* ── Toolbar ── */
QToolBar {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['toolbar_t']}, stop:1 {C['toolbar_b']});
    border: none;
    border-bottom: 1px solid {C['border']};
    padding: 6px 14px;
    spacing: 8px;
    min-height: 44px;
}}
QToolBar::separator {{
    background: {C['border']};
    width: 1px;
    margin: 8px 6px;
}}

/* ── Status bar ── */
QStatusBar {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['toolbar_t']}, stop:1 {C['toolbar_b']});
    border-top: 1px solid {C['border']};
    color: {C['text2']};
    font-size: 12px;
    padding: 0 16px;
    min-height: 24px;
}}
QStatusBar::item {{ border: none; }}

/* ── Scrollbar ── */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {C['border']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {C['text3']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Inputs ── */
QTextEdit, QLineEdit {{
    background: {C['input_bg']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 7px;
    padding: 7px 10px;
    selection-background-color: {C['accent_dim']};
    selection-color: {C['text']};
}}
QTextEdit:focus, QLineEdit:focus {{
    border-color: {C['accent']};
    outline: none;
}}

/* ── ComboBox ── */
QComboBox {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['btn_grad_t']}, stop:1 {C['btn_grad_b']});
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 5px 28px 5px 10px;
    min-height: 22px;
}}
QComboBox:hover {{ border-color: {C['text3']}; }}
QComboBox:focus {{ border-color: {C['accent']}; }}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background: {C['surface']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 3px;
    selection-background-color: {C['accent']};
    selection-color: white;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    min-height: 28px;
    padding: 2px 8px;
    border-radius: 5px;
}}

/* ── Buttons — base ── */
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['btn_grad_t']}, stop:1 {C['btn_grad_b']});
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 5px 16px;
    min-height: 24px;
    font-weight: 400;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #F0F0FF, stop:1 #E0E0F5);
    border-color: {C['text3']};
}}
QPushButton:pressed {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #D8D8F0, stop:1 #CCCCEC);
}}
QPushButton:disabled {{
    color: {C['text3']};
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #FAFAFA, stop:1 #F0F0F0);
    border-color: {C['border_l']};
}}

/* Primary (default action) */
QPushButton#primary {{
    background: {C['accent']};
    color: {C['text']};
    border: 1px solid {C['accent_p']};
    font-weight: 600;
    min-height: 28px;
    border-radius: 7px;
    font-size: 14px;
}}
QPushButton#primary:hover {{ background: {C['accent_h']}; }}
QPushButton#primary:pressed {{ background: {C['accent_p']}; }}
QPushButton#primary:disabled {{
    background: {C['border_l']};
    color: {C['text3']};
    border-color: {C['border_l']};
}}

/* Secondary */
QPushButton#secondary {{
    color: {C['accent']};
    font-weight: 400;
}}
QPushButton#secondary:hover {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #EEF5FF, stop:1 #E0EDFF);
}}

/* Danger */
QPushButton#danger {{
    color: {C['danger']};
}}
QPushButton#danger:hover {{
    background: {C['danger_dim']};
    border-color: {C['danger']};
}}

/* Toolbar buttons */
QPushButton#keyBtn {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['btn_grad_t']}, stop:1 {C['btn_grad_b']});
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 12px;
    min-height: 22px;
}}
QPushButton#keyBtn:hover {{ background: #F0F0FF; }}
QPushButton#keyBtn[hasKey=true] {{ color: {C['success']}; }}

QPushButton#lang {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 {C['btn_grad_t']}, stop:1 {C['btn_grad_b']});
    color: {C['text2']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 600;
    min-height: 22px;
}}
QPushButton#lang:hover {{
    background: #F0F0FF;
    color: {C['accent']};
}}

/* ── Splitter ── */
QSplitter::handle:horizontal {{
    background: {C['border']};
    width: 1px;
}}

/* ── Image frame ── */
QFrame#imageFrame {{
    background: {C['surface']};
    border: 1px solid {C['border_l']};
    border-radius: 12px;
}}

/* ── Section label ── */
QLabel#section {{
    color: {C['text2']};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

/* ── Dialog ── */
QDialog {{
    background: {C['sidebar']};
}}
"""

TR = {
    "fr": {
        "key_ok":           "Clé API ✓",
        "key_ok_tip":       "Clé API configurée — cliquer pour modifier",
        "key_missing":      "Clé API…",
        "key_missing_tip":  "Aucune clé API configurée",
        "prompt_heading":   "Prompt",
        "params_heading":   "Paramètres",
        "prompt_hint":      "Décrivez l'image à générer…",
        "quality_label":    "Qualité",
        "format_label":     "Format",
        "quality_tip":      "low = rapide/économique · medium = équilibré · high = meilleure qualité",
        "format_tip":       "png = sans perte · jpeg = compression · webp = moderne",
        "generate":         "Générer l'image",
        "generating":       "Génération en cours…",
        "save":             "Sauvegarder…",
        "reset":            "Réinitialiser",
        "no_key":           "Aucune clé API configurée. Cliquez sur « Clé API… ».",
        "no_prompt":        "Veuillez entrer un prompt.",
        "gen_progress":     "Génération en cours…",
        "gen_success":      "Image générée avec succès.",
        "gen_error":        "Erreur : {}",
        "key_saved":        "Clé API sauvegardée.",
        "img_saved":        "Image sauvegardée : {}",
        "placeholder":      "L'image générée apparaîtra ici",
        "dlg_title":        "Clé API OpenAI",
        "dlg_label":        "Clé API OpenAI",
        "dlg_test":         "Tester",
        "dlg_cancel":       "Annuler",
        "dlg_ok":           "Enregistrer",
        "dlg_enter_key":    "Veuillez entrer une clé.",
        "dlg_testing":      "Test en cours…",
        "dlg_success":      "Connexion réussie ✓",
        "dlg_fail":         "Échec : {}",
        "save_title":       "Sauvegarder l'image",
        "save_filter_png":  "Images PNG (*.png)",
        "save_filter_jpeg": "Images JPEG (*.jpg *.jpeg)",
        "save_filter_webp": "Images WebP (*.webp)",
    },
    "en": {
        "key_ok":           "API Key ✓",
        "key_ok_tip":       "API key configured — click to change",
        "key_missing":      "API Key…",
        "key_missing_tip":  "No API key configured",
        "prompt_heading":   "Prompt",
        "params_heading":   "Parameters",
        "prompt_hint":      "Describe the image to generate…",
        "quality_label":    "Quality",
        "format_label":     "Format",
        "quality_tip":      "low = fast/cheap · medium = balanced · high = best quality",
        "format_tip":       "png = lossless · jpeg = compressed · webp = modern",
        "generate":         "Generate Image",
        "generating":       "Generating…",
        "save":             "Save…",
        "reset":            "Reset",
        "no_key":           "No API key configured. Click « API Key… ».",
        "no_prompt":        "Please enter a prompt.",
        "gen_progress":     "Generating…",
        "gen_success":      "Image generated successfully.",
        "gen_error":        "Error: {}",
        "key_saved":        "API key saved.",
        "img_saved":        "Image saved: {}",
        "placeholder":      "Generated image will appear here",
        "dlg_title":        "OpenAI API Key",
        "dlg_label":        "OpenAI API Key",
        "dlg_test":         "Test",
        "dlg_cancel":       "Cancel",
        "dlg_ok":           "Save",
        "dlg_enter_key":    "Please enter a key.",
        "dlg_testing":      "Testing…",
        "dlg_success":      "Connection successful ✓",
        "dlg_fail":         "Failed: {}",
        "save_title":       "Save Image",
        "save_filter_png":  "PNG images (*.png)",
        "save_filter_jpeg": "JPEG images (*.jpg *.jpeg)",
        "save_filter_webp": "WebP images (*.webp)",
    },
}


# ── Workers ────────────────────────────────────────────────────────────────────

class ApiTestWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, key: str, lang: str):
        super().__init__()
        self.key  = key
        self.lang = lang

    def run(self):
        t = TR[self.lang]
        try:
            from openai import OpenAI
            OpenAI(api_key=self.key).models.list()
            self.done.emit(True, t["dlg_success"])
        except Exception as exc:
            self.done.emit(False, t["dlg_fail"].format(exc))


class GenerateWorker(QThread):
    success = pyqtSignal(bytes, str)
    error   = pyqtSignal(str)

    def __init__(self, api_key: str, prompt: str, params: dict):
        super().__init__()
        self.api_key = api_key
        self.prompt  = prompt
        self.params  = params

    def run(self):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            kwargs: dict = {
                "model":         "gpt-image-2",
                "prompt":        self.prompt,
                "n":             1,
                "output_format": self.params["fmt"],
            }
            if self.params["quality"] != "auto": kwargs["quality"] = self.params["quality"]

            response = client.images.generate(**kwargs)
            data = base64.b64decode(response.data[0].b64_json)
            self.success.emit(data, self.params["fmt"])
        except Exception as exc:
            self.error.emit(str(exc))


# ── API key dialog ─────────────────────────────────────────────────────────────

class ApiKeyDialog(QDialog):
    saved = pyqtSignal(str)

    def __init__(self, parent, config: dict, lang: str):
        super().__init__(parent)
        self.setFixedWidth(440)
        self.setModal(True)
        self._config = config
        self._lang   = lang
        self._worker = None
        self._build_ui()

    def _t(self, key: str) -> str:
        return TR[self._lang][key]

    def _build_ui(self):
        self.setWindowTitle(self._t("dlg_title"))

        root = QWidget(self)
        root.setStyleSheet(f"background: {C['surface']};")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)

        layout = QVBoxLayout(root)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 20)

        self._label = QLabel()
        self._label.setStyleSheet(
            f"color: {C['text']}; font-size: 14px; font-weight: 600;"
        )
        layout.addWidget(self._label)

        key_row = QHBoxLayout()
        key_row.setSpacing(8)
        self._entry = QLineEdit()
        self._entry.setEchoMode(QLineEdit.EchoMode.Password)
        self._entry.returnPressed.connect(self._on_ok)
        if "api_key" in self._config:
            self._entry.setText(self._config["api_key"])
        key_row.addWidget(self._entry)

        self._show_btn = QPushButton("👁")
        self._show_btn.setFixedSize(34, 34)
        self._show_btn.setCheckable(True)
        self._show_btn.toggled.connect(self._toggle_visibility)
        key_row.addWidget(self._show_btn)
        layout.addLayout(key_row)

        self._status_lbl = QLabel("")
        self._status_lbl.setWordWrap(True)
        self._status_lbl.setStyleSheet(
            f"color: {C['text2']}; font-size: 12px;"
        )
        self._status_lbl.setMinimumHeight(18)
        layout.addWidget(self._status_lbl)

        layout.addSpacing(4)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(
            f"background: {C['border_l']}; border: none; max-height: 1px;"
        )
        layout.addWidget(sep)
        layout.addSpacing(4)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._test_btn = QPushButton()
        self._test_btn.setObjectName("secondary")
        self._test_btn.clicked.connect(self._on_test)
        btn_row.addWidget(self._test_btn)
        btn_row.addStretch()

        self._cancel_btn = QPushButton()
        self._cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self._cancel_btn)

        self._ok_btn = QPushButton()
        self._ok_btn.setObjectName("primary")
        self._ok_btn.setDefault(True)
        self._ok_btn.clicked.connect(self._on_ok)
        btn_row.addWidget(self._ok_btn)

        layout.addLayout(btn_row)
        self._retranslate()

    def _retranslate(self):
        self._label.setText(self._t("dlg_label"))
        self._test_btn.setText(self._t("dlg_test"))
        self._cancel_btn.setText(self._t("dlg_cancel"))
        self._ok_btn.setText(self._t("dlg_ok"))

    def _toggle_visibility(self, checked: bool):
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self._entry.setEchoMode(mode)

    def _on_test(self):
        key = self._entry.text().strip()
        if not key:
            self._status_lbl.setText(self._t("dlg_enter_key"))
            return
        self._test_btn.setEnabled(False)
        self._status_lbl.setStyleSheet(f"color: {C['text2']}; font-size: 12px;")
        self._status_lbl.setText(self._t("dlg_testing"))
        self._worker = ApiTestWorker(key, self._lang)
        self._worker.done.connect(self._on_test_done)
        self._worker.start()

    def _on_test_done(self, ok: bool, msg: str):
        self._test_btn.setEnabled(True)
        color = C["success"] if ok else C["danger"]
        self._status_lbl.setStyleSheet(f"color: {color}; font-size: 12px;")
        self._status_lbl.setText(msg)

    def _on_ok(self):
        key = self._entry.text().strip()
        if key:
            self.saved.emit(key)
        self.accept()


# ── Image display ──────────────────────────────────────────────────────────────

class ImageView(QLabel):
    def __init__(self):
        super().__init__()
        self._raw_pixmap: QPixmap | None = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_image(self, data: bytes):
        img = QImage()
        img.loadFromData(data)
        self._raw_pixmap = QPixmap.fromImage(img)
        self.setText("")
        self.setStyleSheet("")
        self._refresh()

    def set_placeholder(self, text: str):
        self._raw_pixmap = None
        super().setPixmap(QPixmap())
        self.setText(text)
        self.setStyleSheet(f"color: {C['text3']}; font-size: 14px;")

    def _refresh(self):
        if self._raw_pixmap:
            scaled = self._raw_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            super().setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh()


# ── Main window ────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPT Image Generator")
        self.resize(1280, 780)

        self._image_data: bytes | None = None
        self._image_fmt:  str          = "png"
        self._config = self._load_config()
        self._lang   = self._config.get("lang", "en")
        self._worker = None

        self._build_ui()
        self._retranslate()

    # ── Config ─────────────────────────────────────────────────────────────

    def _load_config(self) -> dict:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except Exception:
                pass
        return {}

    def _save_config(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(self._config, indent=2))

    def _t(self, key: str) -> str:
        return TR[self._lang][key]

    # ── UI ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        app_lbl = QLabel("GPT Image Generator")
        app_lbl.setStyleSheet(
            f"color: {C['text']}; font-size: 13px; font-weight: 600;"
            f" padding: 0 10px 0 2px;"
        )
        toolbar.addWidget(app_lbl)
        toolbar.addSeparator()

        self._key_btn = QPushButton()
        self._key_btn.setObjectName("keyBtn")
        self._key_btn.clicked.connect(self._on_open_key_dialog)
        toolbar.addWidget(self._key_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        self._lang_btn = QPushButton()
        self._lang_btn.setObjectName("lang")
        self._lang_btn.setFixedWidth(40)
        self._lang_btn.clicked.connect(self._on_toggle_lang)
        toolbar.addWidget(self._lang_btn)

        # Central: sidebar + content
        central = QWidget()
        central.setStyleSheet(f"background: {C['window']};")
        h = QHBoxLayout(central)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self._build_sidebar())
        splitter.addWidget(self._build_canvas())
        splitter.setSizes([360, 920])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        h.addWidget(splitter)
        self.setCentralWidget(central)

        # Status bar
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(
            f"QWidget#sidebar {{ background: {C['sidebar']};"
            f" border-right: 1px solid {C['border']}; }}"
        )
        sidebar.setMinimumWidth(300)
        sidebar.setMaximumWidth(460)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        # ── Prompt ──
        self._prompt_lbl = self._section_label()
        layout.addWidget(self._prompt_lbl)
        layout.addSpacing(6)

        self._prompt = QTextEdit()
        self._prompt.setMinimumHeight(140)
        self._prompt.setMaximumHeight(200)
        layout.addWidget(self._prompt)
        layout.addSpacing(20)

        # ── Separator ──
        layout.addWidget(self._hsep())
        layout.addSpacing(16)

        # ── Params ──
        self._params_lbl = self._section_label()
        layout.addWidget(self._params_lbl)
        layout.addSpacing(10)

        self._build_params(layout)
        layout.addSpacing(20)

        # ── Separator ──
        layout.addWidget(self._hsep())
        layout.addSpacing(16)

        # ── Buttons ──
        self._gen_btn = QPushButton()
        self._gen_btn.setObjectName("primary")
        self._gen_btn.setMinimumHeight(34)
        self._gen_btn.clicked.connect(self._on_generate)
        layout.addWidget(self._gen_btn)
        layout.addSpacing(8)

        row = QHBoxLayout()
        row.setSpacing(8)
        self._save_btn = QPushButton()
        self._save_btn.setObjectName("secondary")
        self._save_btn.setEnabled(False)
        self._save_btn.clicked.connect(self._on_save_image)
        row.addWidget(self._save_btn)

        self._reset_btn = QPushButton()
        self._reset_btn.setObjectName("danger")
        self._reset_btn.clicked.connect(self._on_reset)
        row.addWidget(self._reset_btn)
        layout.addLayout(row)

        layout.addStretch()
        return sidebar

    def _section_label(self) -> QLabel:
        lbl = QLabel()
        lbl.setObjectName("section")
        return lbl

    def _hsep(self) -> QFrame:
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(
            f"background: {C['border_l']}; border: none; max-height: 1px;"
        )
        return sep

    def _build_params(self, parent: QVBoxLayout):
        grid = QGridLayout()
        grid.setVerticalSpacing(9)
        grid.setHorizontalSpacing(12)
        grid.setContentsMargins(0, 0, 0, 0)

        self._quality_lbl = QLabel()
        self._format_lbl  = QLabel()

        for lbl in (self._quality_lbl, self._format_lbl):
            lbl.setStyleSheet(f"color: {C['text']}; font-size: 13px;")
            lbl.setMinimumWidth(80)

        self._quality_cb = QComboBox(); self._quality_cb.addItems(QUALITIES)
        self._format_cb  = QComboBox(); self._format_cb.addItems(FORMATS)

        for cb in (self._quality_cb, self._format_cb):
            cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        for i, (lbl, cb) in enumerate([
            (self._quality_lbl, self._quality_cb),
            (self._format_lbl,  self._format_cb),
        ]):
            grid.addWidget(lbl, i, 0)
            grid.addWidget(cb,  i, 1)

        grid.setColumnStretch(1, 1)
        parent.addLayout(grid)

    def _build_canvas(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setStyleSheet(f"background: {C['window']};")
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(16, 16, 16, 16)

        frame = QFrame()
        frame.setObjectName("imageFrame")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 45))
        frame.setGraphicsEffect(shadow)

        inner = QVBoxLayout(frame)
        inner.setContentsMargins(0, 0, 0, 0)
        self._image_view = ImageView()
        inner.addWidget(self._image_view)

        layout.addWidget(frame)
        return wrapper

    # ── Translation ────────────────────────────────────────────────────────

    def _retranslate(self):
        t = TR[self._lang]
        self._lang_btn.setText("EN" if self._lang == "fr" else "FR")
        self._lang_btn.setToolTip(
            "Switch to English" if self._lang == "fr" else "Passer en français"
        )
        self._refresh_key_btn()
        self._prompt_lbl.setText(t["prompt_heading"].upper())
        self._params_lbl.setText(t["params_heading"].upper())
        self._prompt.setPlaceholderText(t["prompt_hint"])
        self._quality_lbl.setText(t["quality_label"])
        self._format_lbl.setText(t["format_label"])
        for lbl, tip_key in [
            (self._quality_lbl, "quality_tip"),
            (self._format_lbl,  "format_tip"),
            (self._quality_cb,  "quality_tip"),
            (self._format_cb,   "format_tip"),
        ]:
            lbl.setToolTip(t[tip_key])
        is_busy = not self._gen_btn.isEnabled()
        self._gen_btn.setText(t["generating"] if is_busy else t["generate"])
        self._save_btn.setText(t["save"])
        self._reset_btn.setText(t["reset"])
        if self._image_data is None:
            self._image_view.set_placeholder(t["placeholder"])

    def _refresh_key_btn(self):
        t = TR[self._lang]
        has_key = bool(self._config.get("api_key"))
        self._key_btn.setProperty("hasKey", has_key)
        self._key_btn.style().unpolish(self._key_btn)
        self._key_btn.style().polish(self._key_btn)
        self._key_btn.setText(t["key_ok"] if has_key else t["key_missing"])
        self._key_btn.setToolTip(t["key_ok_tip"] if has_key else t["key_missing_tip"])

    def _on_toggle_lang(self):
        self._lang = "en" if self._lang == "fr" else "fr"
        self._config["lang"] = self._lang
        self._save_config()
        self._retranslate()

    # ── Callbacks ──────────────────────────────────────────────────────────

    def _on_open_key_dialog(self):
        dlg = ApiKeyDialog(self, self._config, self._lang)
        dlg.saved.connect(self._on_key_saved)
        dlg.exec()

    def _on_key_saved(self, key: str):
        self._config["api_key"] = key
        self._save_config()
        self._refresh_key_btn()
        self._show_status(self._t("key_saved"))

    def _on_generate(self):
        if not self._config.get("api_key"):
            self._show_status(self._t("no_key"))
            return
        prompt = self._prompt.toPlainText().strip()
        if not prompt:
            self._show_status(self._t("no_prompt"))
            return

        params = {
            "quality": self._quality_cb.currentText(),
            "fmt":     self._format_cb.currentText(),
        }
        self._set_busy(True)
        self._show_status(self._t("gen_progress"))
        self._worker = GenerateWorker(self._config["api_key"], prompt, params)
        self._worker.success.connect(self._on_success)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_success(self, data: bytes, fmt: str):
        self._image_data = data
        self._image_fmt  = fmt
        self._image_view.set_image(data)
        self._set_busy(False)
        self._show_status(self._t("gen_success"), C["success"])

    def _on_error(self, msg: str):
        self._set_busy(False)
        self._show_status(self._t("gen_error").format(msg), C["danger"])

    def _on_save_image(self):
        if not self._image_data:
            return
        ext = self._image_fmt
        t = TR[self._lang]
        filters = {
            "png":  t["save_filter_png"],
            "jpeg": t["save_filter_jpeg"],
            "webp": t["save_filter_webp"],
        }
        path, _ = QFileDialog.getSaveFileName(
            self, t["save_title"], f"image.{ext}",
            filters.get(ext, f"*.{ext}"),
        )
        if path:
            Path(path).write_bytes(self._image_data)
            self._show_status(self._t("img_saved").format(path))

    def _on_reset(self):
        self._prompt.clear()
        self._image_view.set_placeholder(self._t("placeholder"))
        self._image_data = None
        for cb in (self._quality_cb, self._format_cb):
            cb.setCurrentIndex(0)
        self._save_btn.setEnabled(False)
        self._show_status("")

    def _set_busy(self, busy: bool):
        self._gen_btn.setEnabled(not busy)
        self._gen_btn.setText(self._t("generating") if busy else self._t("generate"))
        self._save_btn.setEnabled(not busy and self._image_data is not None)

    def _show_status(self, text: str, color: str = ""):
        style_extra = f"color: {color};" if color else f"color: {C['text2']};"
        self._statusbar.setStyleSheet(
            f"QStatusBar {{ background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f" stop:0 {C['toolbar_t']}, stop:1 {C['toolbar_b']});"
            f" border-top: 1px solid {C['border']}; {style_extra}"
            f" font-size: 12px; padding: 0 16px; }}"
        )
        self._statusbar.showMessage(text)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("GPT Image Generator")
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)

    icon_path = Path(__file__).parent.parent / "gpt-image-gen" / "icone.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
