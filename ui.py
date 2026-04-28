import sys, os, ctypes
from datetime import datetime
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
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
        self.setMinimumWidth(500)
        self.resize(500, 250)
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
        layout.setSpacing(15)

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

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.evaluator = StrengthEvaluator()

    def evaluate_password(self, text):
        if not text:
            self.strength_bar.setValue(0)
            self.strength_bar.setFormat("Введите пароль")
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
        self.strength_bar.setValue(p)
        self.strength_bar.setFormat(label)
        self.strength_bar.setStyleSheet(
            f"QProgressBar {{ background: rgba(20,20,25,200); border: 1px solid #f39c12; "
            f"color: #ecf0f1; text-align: center; border-radius: 4px; }}"
            f"QProgressBar::chunk {{ background: {c}; border-radius: 4px; }}"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MrKhaimi.MagmaKey.1.0")

        self.config = Config()
        self.generator = PasswordGenerator()

        self.setWindowTitle("MagmaKey")
        self.setMinimumSize(680, 800)
        self.setWindowIcon(QIcon("magmakey.ico"))

        self.background = LavaBackground()
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
        content_layout.setSpacing(12)

        title = QLabel("MAGMAKEY")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #f39c12; background: transparent; border: none;")
        content_layout.addWidget(title)

        subtitle = QLabel("Надёжные пароли для вашей безопасности")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #e67e22; background: transparent; font-size: 14px; border: none;")
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
            copy_btn.clicked.connect(lambda _, f=field: f.copy_to_clipboard())

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
            self.password_widgets.append((field, strength_bar, vis_btn))

        length_layout = QHBoxLayout()
        length_lbl = QLabel("Длина:")
        length_lbl.setStyleSheet("color: #ecf0f1; background: transparent; border: none;")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(4, 128)
        self.length_slider.setValue(int(self.config.get("length", int)))
        self.length_slider.valueChanged.connect(self.on_length_changed)
        self.length_value = QLabel(str(self.length_slider.value()))
        self.length_value.setStyleSheet("color: #f39c12; background: transparent; border: none;")
        self.length_slider.valueChanged.connect(lambda v: self.length_value.setText(str(v)))

        length_layout.addWidget(length_lbl)
        length_layout.addWidget(self.length_slider)
        length_layout.addWidget(self.length_value)
        content_layout.addLayout(length_layout)

        checks_layout = QVBoxLayout()
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
            checks_layout.addWidget(cb)

        self.use_upper_cb.setObjectName("use_upper")
        self.use_lower_cb.setObjectName("use_lower")
        self.use_digits_cb.setObjectName("use_digits")
        self.use_special_cb.setObjectName("use_special")

        self.use_upper_cb.setChecked(self.config.get("use_upper", bool))
        self.use_lower_cb.setChecked(self.config.get("use_lower", bool))
        self.use_digits_cb.setChecked(self.config.get("use_digits", bool))
        self.use_special_cb.setChecked(self.config.get("use_special", bool))
        content_layout.addLayout(checks_layout)

        btn_row1 = QHBoxLayout()
        gen_btn = QPushButton("ГЕНЕРИРОВАТЬ")
        gen_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #f39c12; border: 2px solid #f39c12; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #f39c12; color: #0b0c10; }"
        )
        gen_btn.clicked.connect(self.generate_passwords)

        refresh_btn = QPushButton("ОБНОВИТЬ")
        refresh_btn.setStyleSheet(
            "background: rgba(20, 20, 25, 180); color: #e67e22; border: 2px solid #e67e22; "
            "padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px;"
            "QPushButton:hover { background: #e67e22; color: #0b0c10; }"
        )
        refresh_btn.clicked.connect(self.refresh_animation)

        btn_row1.addWidget(gen_btn)
        btn_row1.addWidget(refresh_btn)
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
        content_layout.addWidget(signature, alignment=Qt.AlignmentFlag.AlignRight)

        self.generate_passwords()

        self.show()
        self.hide()
        self.show()

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
        passwords = [field.text() for field, _, _ in self.password_widgets]
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
        length = self.length_slider.value()
        use_upper = self.use_upper_cb.isChecked()
        use_lower = self.use_lower_cb.isChecked()
        use_digits = self.use_digits_cb.isChecked()
        use_special = self.use_special_cb.isChecked()

        self.background.trigger_glow()
        evaluator = StrengthEvaluator()

        for field, strength_bar, _ in self.password_widgets:
            password, char_pool = self.generator.generate(
                length, use_upper, use_lower, use_digits, use_special
            )
            field.setText(password)
            self.add_to_history(password)

            entropy, label = evaluator.evaluate(password, char_pool)
            p = {"Низкая":25, "Средняя":50, "Высокая":75, "Максимальная":100}[label]
            c = {"Низкая":"#c0392b", "Средняя":"#f1c40f", "Высокая":"#f39c12", "Максимальная":"#27ae60"}[label]
            strength_bar.setValue(p)
            strength_bar.setFormat(label)
            strength_bar.setStyleSheet(
                f"QProgressBar {{ background: rgba(20,20,25,180); border: 1px solid #f39c12; "
                f"color: #ecf0f1; text-align: center; border-radius: 4px; }}"
                f"QProgressBar::chunk {{ background: {c}; border-radius: 4px; }}"
            )

    def refresh_animation(self):
        self.generate_passwords()
        self.background.trigger_glow()
