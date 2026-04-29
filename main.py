import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from config import Config
from password_generator import PasswordGenerator, StrengthEvaluator
from lava_animation import LavaBackground

class PasswordField(BoxLayout):
    show_password = BooleanProperty(False)

class StrengthBar(BoxLayout):
    label = StringProperty("Низкая")
    label_color = ObjectProperty((0.75,0.15,0.15,1))
    bar_color = ObjectProperty((0.95,0.6,0.07,1))
    value = NumericProperty(0)

class CheckRow(BoxLayout):
    active = BooleanProperty(False)
    text = StringProperty("")
    callback = ObjectProperty(None)

class Root(BoxLayout):
    pass

class MagmaKeyApp(App):
    def build(self):
        self.config = Config()
        self.generator = PasswordGenerator()
        self.evaluator = StrengthEvaluator()
        self.history = []
        return Root()

    def on_start(self):
        self.load_checks()
        self.generate_passwords()

    def load_checks(self):
        root = self.root
        self.use_upper = self.config.get("use_upper")
        self.use_lower = self.config.get("use_lower")
        self.use_digits = self.config.get("use_digits")
        self.use_special = self.config.get("use_special")

        checks_section = root.ids.checks_section
        checks_section.add_widget(CheckRow(active=self.use_upper, text="Заглавные буквы (A-Z)", callback=self.set_upper))
        checks_section.add_widget(CheckRow(active=self.use_lower, text="Строчные буквы (a-z)", callback=self.set_lower))
        checks_section.add_widget(CheckRow(active=self.use_digits, text="Цифры (0-9)", callback=self.set_digits))
        checks_section.add_widget(CheckRow(active=self.use_special, text="Спецсимволы (!@#...)", callback=self.set_special))

        self.length_slider = root.ids.length_slider
        self.length_slider.value = self.config.get("length")
        self.length_label = root.ids.length_label
        self.update_length_label(self.length_slider.value)

        self.password_fields = []
        passwords_section = root.ids.passwords_section
        for i in range(3):
            pf = PasswordField()
            pf.index = i
            passwords_section.add_widget(pf)
            bar = StrengthBar()
            passwords_section.add_widget(bar)
            self.password_fields.append((pf.ids.pwd_input, bar))

        self.lava = root.ids.lava

    def set_upper(self, val):
        self.use_upper = val
        self.config.set("use_upper", val)

    def set_lower(self, val):
        self.use_lower = val
        self.config.set("use_lower", val)

    def set_digits(self, val):
        self.use_digits = val
        self.config.set("use_digits", val)

    def set_special(self, val):
        self.use_special = val
        self.config.set("use_special", val)

    def update_length_label(self, value):
        self.length_label.text = str(int(value))
        self.config.set("length", int(value))

    def copy_password(self, field):
        if field.text:
            Clipboard.copy(field.text)
            field.background_color = (0.95,0.6,0.07,1)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: setattr(field, 'background_color', (0.08,0.08,0.1,1)), 0.3)

    def generate_passwords(self):
        length = int(self.length_slider.value)
        self.lava.trigger_glow()
        for field, bar in self.password_fields:
            pwd, pool = self.generator.generate(length, self.use_upper, self.use_lower, self.use_digits, self.use_special)
            field.text = pwd
            self.history.append(pwd)
            if len(self.history) > 12:
                self.history.pop(0)
            entropy, label = self.evaluator.evaluate(pwd, pool)
            p = {"Низкая":25,"Средняя":50,"Высокая":75,"Максимальная":100}[label]
            c = {"Низкая":(0.75,0.15,0.15,1),"Средняя":(0.95,0.75,0.07,1),"Высокая":(0.95,0.6,0.07,1),"Максимальная":(0.15,0.6,0.15,1)}[label]
            bar.value = p
            bar.label = label
            bar.label_color = c
            bar.bar_color = c

    def show_history(self):
        if not self.history:
            content = Label(text="История пуста.")
        else:
            recent = self.history[-3:]
            content = Label(text="Последние пароли:\n\n" + "\n".join(recent))
        popup = Popup(title="История паролей", content=content, size_hint=(0.8, 0.4))
        popup.open()

    def open_password_checker(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Label(text="Введите ваш пароль для проверки", color=(0.95,0.6,0.07,1)))
        entry = TextInput(password=True, background_color=(0.08,0.08,0.1,1), foreground_color=(0.95,0.6,0.07,1))
        content.add_widget(entry)
        result_label = Label(text="")
        content.add_widget(result_label)

        def check(instance):
            pw = entry.text
            has_lower = any(c.islower() for c in pw)
            has_upper = any(c.isupper() for c in pw)
            has_digit = any(c.isdigit() for c in pw)
            has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pw)
            pool = ""
            if has_lower: pool += "abcdefghijklmnopqrstuvwxyz"
            if has_upper: pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if has_digit: pool += "0123456789"
            if has_special: pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            entropy, label = self.evaluator.evaluate(pw, pool)
            result_label.text = f"Сложность: {label}"
            result_label.color = {"Низкая":(0.75,0.15,0.15,1),"Средняя":(0.95,0.75,0.07,1),"Высокая":(0.95,0.6,0.07,1),"Максимальная":(0.15,0.6,0.15,1)}[label]

        check_btn = Button(text="Проверить", background_color=(0.08,0.08,0.1,1), color=(0.95,0.6,0.07,1))
        check_btn.bind(on_press=check)
        content.add_widget(check_btn)
        popup = Popup(title="Проверка пароля", content=content, size_hint=(0.8, 0.5))
        popup.open()

    def export_passwords(self):
        passwords = [field.text for field, _ in self.password_fields]
        filename = "/storage/emulated/0/Download/passwords.txt" if os.name == 'posix' else os.path.join(os.path.expanduser("~"), "Desktop/passwords.txt")
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                for i, p in enumerate(passwords, 1):
                    f.write(f"Пароль {i}: {p}\n")
            popup = Popup(title="Экспорт", content=Label(text=f"Пароли сохранены в {filename}"), size_hint=(0.8, 0.4))
            popup.open()
        except Exception as e:
            popup = Popup(title="Ошибка", content=Label(text=str(e)), size_hint=(0.8, 0.4))
            popup.open()

if __name__ == '__main__':
    MagmaKeyApp().run()