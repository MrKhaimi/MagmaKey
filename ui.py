#!/usr/bin/env python3
# Copyright © 2026, MrKhaimi Все права защищены.

import sys, os, ctypes, winsound, io
from datetime import datetime
import qrcode
from PIL import Image

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QCheckBox,
    QProgressBar, QWidget, QFrame, QMessageBox, QDialog,
    QDialogButtonBox
)
from config import Config
from password_generator import PasswordGenerator, StrengthEvaluator
from lava_animation import LavaBackground


class ClickableLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_timer = QTimer()
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.reset_style)
        self.default_style = self.styleSheet()
        self.setEchoMode(QLineEdit.EchoMode.Normal)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.copy_to_clipboard()
        super().mouseReleaseEvent(event)

    def copy_to_clipboard(self):
        text = self.text()
        if text:
            QApplication.clipboard().setText(text)
            self.setStyleSheet(
                "background: #f39c12; color: #0b0c10; "
                "border: 1px solid #e67e22; border-radius: 6px; padding: 6px; font-size: 16px;"
            )
            self.click_timer.start(400)

    def reset_style(self):
        self.setStyleSheet(self.default_style)


class PasswordCheckerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Проверка пароля")
        self.setMinimumWidth(550)
        self.resize(550, 350)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #14161a, stop:1 #0b0c10);
                border: 2px solid #f39c12;
                border-radius: 10px;
            }
            QLabel { color: #ecf0f1; background: transparent; }
            QLineEdit {
                background: rgba(20, 20, 25, 200);
                color: #f39c12;
                border: 1px solid #f39c12;
                border-radius: 6px;
                padding: 8px;
                font-size: 16px;
            }
            QPushButton {
                background: rgba(20, 20, 25, 200);
                color: #f39c12;
                border: 1px solid #f39c12;
                padding: 8px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover { background: #f39c12; color: #0b0c10; }
            QProgressBar {
                background: rgba(20,20,25,200);
                border: 1px solid #f39c12;
                color: #ecf0f1;
                text-align: center;
                border-radius: 4px;
            }
            QProgressBar::chunk { background: #f39c12; border-radius: 4px; }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Введите ваш пароль для проверки")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12;")
        layout.addWidget(title)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль...")
        self.password_input.textChanged.connect(self.evaluate_password)
        layout.addWidget(self.password_input)

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setTextVisible(True)
        self.strength_bar.setValue(0)
        self.strength_bar.setFormat("Введите пароль")
        layout.addWidget(self.strength_bar)

        self.analysis_label = QLabel("")
        self.analysis_label.setWordWrap(True)
        self.analysis_label.setStyleSheet("font-size: 13px; padding: 6px;")
        layout.addWidget(self.analysis_label)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.evaluator = StrengthEvaluator()

    def evaluate_password(self, text):
        if not text:
            self.strength_bar.setValue(0)
            self.strength_bar.setFormat("Введите пароль")
            self.analysis_label.setText("")
            return
        has_lower = any(c.islower() for c in text)
        has_upper = any(c.isupper() for c in text)
        has_digit = any(c.isdigit() for c in text)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in text)

        import string
        pool = ""
        if has_lower: pool += string.ascii_lowercase
        if has_upper: pool += string.ascii_uppercase
        if has_digit: pool += string.digits
        if has_special: pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        entropy, label = self.evaluator.evaluate(text, pool)
        p = {"Низкая":25, "Средняя":50, "Высокая":75, "Максимальная":100}[label]
        c = {"Низкая":"#c0392b", "Средняя":"#f1c40f", "Высокая":"#f39c12", "Максимальная":"#27ae60"}[label]

        if PasswordGenerator.is_common(text):
            label = "В словаре утечек!"
            p = 0
            c = "#ff4444"

        self.strength_bar.setValue(p)
        self.strength_bar.setFormat(label)
        self.strength_bar.setStyleSheet(
            f"QProgressBar {{ background: rgba(20,20,25,200); border: 1px solid #f39c12; "
            f"color: #ecf0f1; text-align: center; border-radius: 4px; }}"
            f"QProgressBar::chunk {{ background: {c}; border-radius: 4px; }}"
        )

        issues = self.evaluator.analyze(text)
        if issues:
            lines = ["<span style='color:#ff6666;'>⚠</span> " + issue for issue in issues]
            analysis_text = "<br>".join(lines)
        else:
            analysis_text = "<span style='color:#27ae60; font-weight:bold;'>✓ Пароль надёжный</span>"
        self.analysis_label.setText(analysis_text)
        self.analysis_label.setStyleSheet(
            "font-size: 13px; padding: 6px; background: transparent;"
            "border: 1px solid #f39c12; border-radius: 4px;"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MrKhaimi.MagmaKey.1.0")

        self.config = Config()
        self.generator = PasswordGenerator()
        self.current_theme = self.config.get("theme")
        self.sound_enabled = self.config.get("sound", bool)
        self.phrase_mode = False
        self.incognito_mode = self.config.get("incognito", bool)   # ← загрузка инкогнито

        self.setWindowTitle("MagmaKey")
        self.setMinimumSize(700, 950)
        self.setWindowIcon(QIcon("magmakey.ico"))

        self.background = LavaBackground()
        self.background.set_theme(self.current_theme)
        self.setCentralWidget(self.background)

        base_layout = QVBoxLayout(self.background)
        base_layout.setContentsMargins(20, 20, 20, 20)

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background: rgba(11, 12, 16, 190);
                border-radius: 20px;
                border: 1px solid #f39c12;
            }
        """)
        self.content_frame.setContentsMargins(20, 15, 20, 15)
        base_layout.addWidget(self.content_frame)

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setSpacing(8)

        title = QLabel("MAGMAKEY")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f39c12; background: transparent; border: none;")
        self.title_label = title
        content_layout.addWidget(title)

        subtitle = QLabel("Надёжные пароли для вашей безопасности")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #e67e22; background: transparent; font-size: 14px; border: none;")
        self.subtitle_label = subtitle
        content_layout.addWidget(subtitle)

        self.history = []
        self.password_widgets = []

        for i in range(3):
            hbox = QHBoxLayout()
            label = QLabel(f"Пароль {i+1}:")
            label.setStyleSheet("color: #ecf0f1; background: transparent; font-weight: bold; border: none;")

            field = ClickableLineEdit()
            field.setReadOnly(True)
            field.default_style = (
                "background: rgba(20, 20, 25, 180); color: #f39c12; "
                "border: 1px solid #f39c12; border-radius: 6px; padding: 6px; font-size: 16px;"
            )
            field.setStyleSheet(field.default_style)

            copy_btn = QPushButton("📋")
            copy_btn.setToolTip("Копировать в буфер обмена")
            copy_btn.setFixedWidth(40)
            copy_btn.setStyleSheet(
                "background: rgba(20, 20, 25, 180); color: #f39c12; border: 1px solid #f39c12; "
                "font-size: 16px; border-radius: 6px;"
                "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
            )
            copy_btn.clicked.connect(lambda _, f=field: self.copy_with_sound(f))

            qr_btn = QPushButton("QR")
            qr_btn.setToolTip("Показать QR‑код этого пароля")
            qr_btn.setFixedWidth(40)
            qr_btn.setStyleSheet(
                "background: rgba(20, 20, 25, 180); color: #f39c12; border: 1px solid #f39c12; "
                "font-size: 14px; font-weight: bold; border-radius: 6px;"
                "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
            )
            qr_btn.clicked.connect(lambda _, f=field: self.show_qr(f))

            vis_btn = QPushButton("🙈")
            vis_btn.setToolTip("Скрыть / показать пароль")
            vis_btn.setFixedWidth(40)
            vis_btn.setStyleSheet(
                "background: rgba(20, 20, 25, 180); color: #f39c12; border: 1px solid #f39c12; "
                "font-size: 16px; border-radius: 6px;"
                "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
            )
            vis_btn.clicked.connect(lambda _, f=field, b=vis_btn: self.toggle_password_visibility(f, b))

            hbox.addWidget(label)
            hbox.addWidget(field, 1)
            hbox.addWidget(copy_btn)
            hbox.addWidget(qr_btn)
            hbox.addWidget(vis_btn)
            content_layout.addLayout(hbox)

            strength_bar = QProgressBar()
            strength_bar.setRange(0, 100)
            strength_bar.setTextVisible(True)
            strength_bar.setStyleSheet(
                "QProgressBar { background: rgba(20, 20, 25, 180); border: 1px solid #f39c12; "
                "color: #ecf0f1; text-align: center; border-radius: 4px; }"
                "QProgressBar::chunk { background: #f39c12; border-radius: 4px; }"
            )
            content_layout.addWidget(strength_bar)

            crack_label = QLabel("")
            crack_label.setStyleSheet(
                "color: #ecf0f1; background: transparent; font-size: 12px; padding: 2px; border: none;"
            )
            content_layout.addWidget(crack_label)

            self.password_widgets.append((field, strength_bar, vis_btn, crack_label))

        # Переключатель режима
        mode_switch_layout = QHBoxLayout()
        self.mode_label = QLabel("Режим:")
        self.mode_label.setStyleSheet("color: #ecf0f1; background: transparent; border: none;")
        self.mode_btn = QPushButton("Фразы")
        self.mode_btn.setCheckable(True)
        self.mode_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #f39c12; border: 2px solid #f39c12; "
            "padding: 8px; font-size: 14px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
            "QPushButton:checked { background: #f39c12; color: #0b0c10; }"
        )
        self.mode_btn.clicked.connect(self.toggle_mode)
        mode_switch_layout.addWidget(self.mode_label)
        mode_switch_layout.addWidget(self.mode_btn)
        mode_switch_layout.addStretch()
        content_layout.addLayout(mode_switch_layout)

        # Длина (обычный режим)
        self.length_layout = QHBoxLayout()
        length_lbl = QLabel("Длина:")
        length_lbl.setStyleSheet("color: #ecf0f1; background: transparent; border: none;")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(4, 128)
        self.length_slider.setValue(int(self.config.get("length", int)))
        self.length_slider.valueChanged.connect(self.on_length_changed)
        self.length_value = QLabel(str(self.length_slider.value()))
        self.length_value.setStyleSheet("color: #f39c12; background: transparent; border: none;")
        self.length_slider.valueChanged.connect(lambda v: self.length_value.setText(str(v)))
        self.length_layout.addWidget(length_lbl)
        self.length_layout.addWidget(self.length_slider)
        self.length_layout.addWidget(self.length_value)
        content_layout.addLayout(self.length_layout)

        # Слова (режим фраз)
        self.phrase_layout = QHBoxLayout()
        phrase_lbl = QLabel("Слов:")
        phrase_lbl.setStyleSheet("color: #ecf0f1; background: transparent; border: none;")
        self.phrase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phrase_slider.setRange(3, 8)
        self.phrase_slider.setValue(4)
        self.phrase_slider.valueChanged.connect(lambda v: self.phrase_count_label.setText(str(v)))
        self.phrase_count_label = QLabel("4")
        self.phrase_count_label.setStyleSheet("color: #f39c12; background: transparent; border: none;")
        self.phrase_layout.addWidget(phrase_lbl)
        self.phrase_layout.addWidget(self.phrase_slider)
        self.phrase_layout.addWidget(self.phrase_count_label)
        self.phrase_layout.setEnabled(False)
        content_layout.addLayout(self.phrase_layout)

        # Чекбоксы
        self.checks_layout = QVBoxLayout()
        self.use_upper_cb = QCheckBox("Заглавные буквы (A-Z)")
        self.use_lower_cb = QCheckBox("Строчные буквы (a-z)")
        self.use_digits_cb = QCheckBox("Цифры (0-9)")
        self.use_special_cb = QCheckBox("Спецсимволы (!@#...)")

        checkbox_style = """
            QCheckBox {
                color: #ecf0f1;
                background: transparent;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #f39c12;
                border-radius: 4px;
                background: rgba(20, 20, 25, 180);
            }
            QCheckBox::indicator:checked {
                background: #f39c12;
                border-color: #e67e22;
            }
            QCheckBox::indicator:hover {
                border-color: #e67e22;
            }
        """

        for cb in (self.use_upper_cb, self.use_lower_cb, self.use_digits_cb, self.use_special_cb):
            cb.setStyleSheet(checkbox_style)
            cb.stateChanged.connect(self.save_checkbox_state)
            self.checks_layout.addWidget(cb)

        self.use_upper_cb.setObjectName("use_upper")
        self.use_lower_cb.setObjectName("use_lower")
        self.use_digits_cb.setObjectName("use_digits")
        self.use_special_cb.setObjectName("use_special")

        self.use_upper_cb.setChecked(self.config.get("use_upper", bool))
        self.use_lower_cb.setChecked(self.config.get("use_lower", bool))
        self.use_digits_cb.setChecked(self.config.get("use_digits", bool))
        self.use_special_cb.setChecked(self.config.get("use_special", bool))

        # ---------- ЧЕКБОКС ИНКОГНИТО ----------
        self.incognito_cb = QCheckBox("Режим Инкогнито (очищать пароли при выходе)")
        self.incognito_cb.setStyleSheet(checkbox_style)
        self.incognito_cb.stateChanged.connect(self.save_incognito_state)
        self.incognito_cb.setChecked(self.incognito_mode)
        self.checks_layout.addWidget(self.incognito_cb)

        content_layout.addLayout(self.checks_layout)
        content_layout.addSpacing(10)

        # Кнопки
        btn_row1 = QHBoxLayout()
        gen_btn = QPushButton("ГЕНЕРИРОВАТЬ")
        gen_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #f39c12; border: 2px solid #f39c12; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
        )
        gen_btn.clicked.connect(self.generate_passwords)
        self.gen_btn = gen_btn

        refresh_btn = QPushButton("ОБНОВИТЬ")
        refresh_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #e67e22; border: 2px solid #e67e22; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #e67e22; color: #0b0c10; }"
        )
        refresh_btn.clicked.connect(self.refresh_animation)
        self.refresh_btn = refresh_btn

        theme_btn_text = "🌙 Холод" if self.current_theme == "amber" else "🔥 Янтарь"
        theme_btn = QPushButton(theme_btn_text)
        theme_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #f39c12; border: 2px solid #f39c12; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
        )
        theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn = theme_btn

        btn_row1.addWidget(gen_btn)
        btn_row1.addWidget(refresh_btn)
        btn_row1.addWidget(theme_btn)
        content_layout.addLayout(btn_row1)

        btn_row2 = QHBoxLayout()
        history_btn = QPushButton("ИСТОРИЯ")
        history_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #f39c12; border: 2px solid #f39c12; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
        )
        history_btn.clicked.connect(self.show_history)

        check_btn = QPushButton("ПРОВЕРИТЬ СВОЙ ПАРОЛЬ")
        check_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #e67e22; border: 2px solid #e67e22; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #e67e22; color: #0b0c10; }"
        )
        check_btn.clicked.connect(self.open_password_checker)

        export_btn = QPushButton("💾 СОХРАНИТЬ")
        export_btn.setToolTip("Сохранить все три пароля в файл на рабочий стол")
        export_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #27ae60; border: 2px solid #27ae60; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #27ae60; color: #0b0c10; }"
        )
        export_btn.clicked.connect(self.export_passwords)

        btn_row2.addWidget(history_btn)
        btn_row2.addWidget(check_btn)
        btn_row2.addWidget(export_btn)
        content_layout.addLayout(btn_row2)

        # Водяной знак
        signature = QLabel("by MrKhaimi")
        signature.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        signature.setStyleSheet("""
            QLabel {
                color: #f39c12;
                background: transparent;
                font-size: 16px;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
        """)
        self.watermark = signature
        content_layout.addWidget(signature, alignment=Qt.AlignmentFlag.AlignRight)

        self.generate_passwords()

        if not hasattr(self, 'watermark') or self.watermark.text() != "by MrKhaimi":
            QMessageBox.critical(self, "Ошибка целостности",
                                 "Обнаружено нарушение защиты. Программа не может быть запущена.")
            sys.exit(1)

        self.show()
        self.hide()
        self.show()

    # ---------- QR‑КОД ----------
    def show_qr(self, field):
        password = field.text()
        if not password:
            return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(password)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#f39c12", back_color="#0b0c10")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())

        dlg = QDialog(self)
        dlg.setWindowTitle("QR‑код пароля")
        dlg.setMinimumSize(300, 300)
        dlg.setStyleSheet("QDialog { background: #0b0c10; }")
        layout = QVBoxLayout()
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        dlg.setLayout(layout)
        dlg.exec()

    # ---------- РЕЖИМ ИНКОГНИТО ----------
    def save_incognito_state(self, state):
        self.incognito_mode = bool(state)
        self.config.save_checkbox("incognito", self.incognito_mode)

    def closeEvent(self, event):
        if self.incognito_mode:
            for field, _, _, _ in self.password_widgets:
                field.setText("")
            self.history.clear()
        event.accept()

    # ---------- ОСТАЛЬНЫЕ МЕТОДЫ ----------
    def toggle_mode(self, checked):
        self.phrase_mode = checked
        if checked:
            self.mode_btn.setText("Обычный")
            self.length_layout.setEnabled(False)
            self.checks_layout.setEnabled(False)
            self.phrase_layout.setEnabled(True)
        else:
            self.mode_btn.setText("Фразы")
            self.length_layout.setEnabled(True)
            self.checks_layout.setEnabled(True)
            self.phrase_layout.setEnabled(False)

    def copy_with_sound(self, field):
        field.copy_to_clipboard()
        if self.sound_enabled:
            winsound.Beep(1000, 100)

    def toggle_theme(self):
        self.current_theme = "cold" if self.current_theme == "amber" else "amber"
        self.config.set("theme", self.current_theme)
        self.theme_btn.setText("🌙 Холод" if self.current_theme == "amber" else "🔥 Янтарь")
        if self.current_theme == "cold":
            accent = "#5dade2"
            accent2 = "#3498db"
            text_color = "#d6eaf8"
        else:
            accent = "#f39c12"
            accent2 = "#e67e22"
            text_color = "#ecf0f1"
        self.title_label.setStyleSheet(f"color: {accent}; background: transparent; border: none;")
        self.subtitle_label.setStyleSheet(f"color: {accent2}; background: transparent; font-size: 14px; border: none;")
        for btn in [self.gen_btn, self.refresh_btn, self.theme_btn]:
            btn.setStyleSheet(
                f"background: rgba(20, 20, 25, 180); color: {accent}; border: 2px solid {accent}; "
                "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
                f"QPushButton:hover {{ background: {accent}; color: #0b0c10; }}"
            )
        for _, _, _, crack_label in self.password_widgets:
            crack_label.setStyleSheet(
                f"color: {text_color}; background: transparent; font-size: 12px; padding: 2px; border: none;"
            )
        self.background.set_theme(self.current_theme)

    def on_length_changed(self, value):
        self.config.save_slider("length", value)

    def save_checkbox_state(self, state):
        cb = self.sender()
        if cb:
            self.config.save_checkbox(cb.objectName(), cb.isChecked())

    def toggle_password_visibility(self, field, button):
        if field.echoMode() == QLineEdit.EchoMode.Normal:
            field.setEchoMode(QLineEdit.EchoMode.Password)
            button.setText("👁")
            button.setToolTip("Показать пароль")
        else:
            field.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setText("🙈")
            button.setToolTip("Скрыть пароль")

    def add_to_history(self, password):
        self.history.append(password)
        if len(self.history) > 12:
            self.history.pop(0)

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "История", "История пуста. Сгенерируйте пароли.")
            return
        recent = self.history[-3:]
        history_text = "Последние пароли:\n\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(recent, 1))
        QMessageBox.information(self, "История паролей", history_text)

    def open_password_checker(self):
        dialog = PasswordCheckerDialog(self)
        dialog.exec()

    def export_passwords(self):
        passwords = [field.text() for field, _, _, _ in self.password_widgets]
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = os.path.join(desktop, "passwords.txt")
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                for i, p in enumerate(passwords, 1):
                    f.write(f"Пароль {i}: {p}\n")
            QMessageBox.information(self, "Экспорт", f"Пароли сохранены в файл:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def generate_passwords(self):
        evaluator = StrengthEvaluator()
        self.background.trigger_glow()
        for field, strength_bar, vis_btn, crack_label in self.password_widgets:
            if self.phrase_mode:
                num_words = self.phrase_slider.value()
                password, char_pool, wordlist_size = self.generator.generate_phrase(num_words)
                entropy, label = evaluator.evaluate(password, char_pool, wordlist_size)
                crack_text = evaluator.crack_time(password, char_pool, wordlist_size)
            else:
                length = self.length_slider.value()
                use_upper = self.use_upper_cb.isChecked()
                use_lower = self.use_lower_cb.isChecked()
                use_digits = self.use_digits_cb.isChecked()
                use_special = self.use_special_cb.isChecked()
                password, char_pool = self.generator.generate(length, use_upper, use_lower, use_digits, use_special)
                entropy, label = evaluator.evaluate(password, char_pool)
                crack_text = evaluator.crack_time(password, char_pool)

            field.setText(password)
            self.add_to_history(password)

            if self.generator.is_common(password):
                crack_text = "Внимание: пароль найден в словаре утечек!"
                crack_label.setStyleSheet(
                    "color: #ff4444; background: transparent; font-size: 12px; padding: 2px; border: none;"
                )
            else:
                if self.current_theme == "cold":
                    crack_label.setStyleSheet(
                        "color: #d6eaf8; background: transparent; font-size: 12px; padding: 2px; border: none;"
                    )
                else:
                    crack_label.setStyleSheet(
                        "color: #ecf0f1; background: transparent; font-size: 12px; padding: 2px; border: none;"
                    )

            p = {"Низкая":25, "Средняя":50, "Высокая":75, "Максимальная":100}[label]
            c = {"Низкая":"#c0392b", "Средняя":"#f1c40f", "Высокая":"#f39c12", "Максимальная":"#27ae60"}[label]
            strength_bar.setValue(p)
            strength_bar.setFormat(label)
            strength_bar.setStyleSheet(
                f"QProgressBar {{ background: rgba(20,20,25,180); border: 1px solid #f39c12; "
                f"color: #ecf0f1; text-align: center; border-radius: 4px; }}"
                f"QProgressBar::chunk {{ background: {c}; border-radius: 4px; }}"
            )

            crack_label.setText(crack_text)

    def refresh_animation(self):
        self.generate_passwords()
        self.background.trigger_glow()
