# 🔥 MagmaKey

**Генератор надёжных паролей с лавовой анимацией и неоновым дизайном.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue?logo=windows)](../../releases/latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/MrKhaimi/MagmaKey?label=latest%20release)](../../releases/latest)
[![Downloads](https://img.shields.io/github/downloads/MrKhaimi/MagmaKey/total?label=downloads)](../../releases)

---

## ✨ Возможности

- 🌋 Гипнотическая анимация в стиле «лавовая лампа» (янтарная и холодная темы)
- 🔐 Три криптостойких пароля генерируются одновременно
- 🧩 Два режима: классические пароли и запоминающиеся фразы (Diceware)
- 📊 Оценка сложности: Низкая / Средняя / Высокая / Максимальная
- 🔍 Детальный анализ слабых мест (подсказки: нет заглавных, цифр, спецсимволов и т.д.)
- ⏱ Оценка времени взлома под каждым паролем
- 🧪 Проверка паролей по офлайн-словарю распространённых утечек (ТОП-100)
- 📲 QR-код для каждого пароля — можно мгновенно перенести на телефон
- 👁 Переключение видимости пароля (показать / скрыть)
- 🔊 Звуковое подтверждение при копировании
- 📋 Копирование пароля в буфер обмена одним кликом
- 🔍 Встроенная проверка надёжности любого своего пароля
- 📜 История последних сгенерированных паролей (до 12 записей)
- 💾 Сохранение паролей в текстовый файл на рабочий стол
- ⚙️ Гибкие настройки: длина пароля (4–128), заглавные / строчные буквы, цифры, спецсимволы
- 🔒 Режим Инкогнито — автоматическая очистка паролей и истории при выходе
- 💾 Автосохранение настроек между запусками
- 🖼️ Собственная иконка в окне и на панели задач
- 🛡 Защита исходного кода (PyArmor) и водяной знак «by MrKhaimi»
- 🔒 **Полностью офлайн** — программа никогда не подключается к интернету

---

## 📥 Скачать

Последняя версия доступна в разделе [Releases](https://github.com/MrKhaimi/MagmaKey/releases).

- 🛠 **MagmaKey_Setup.exe** — установщик для Windows (с ярлыками)
- 🟢 **MagmaKey.exe** — портативная версия (без установки)


## 🖥️ Технологии

- **Python 3.12+**
- **PyQt6** — графический интерфейс и анимация
- **PyInstaller** — сборка в EXE
- **PyArmor** — обфускация и защита кода
- **Inno Setup** — создание установщика

Данный проект будет подписан с использованием сертификата, предоставленного фондом SignPath Foundation.
---

In English --
# 🔥 MagmaKey

**A reliable password generator with lava lamp animation and neon design.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue?logo=windows)](../../releases/latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/MrKhaimi/MagmaKey?label=latest%20release)](../../releases/latest)
[![Downloads](https://img.shields.io/github/downloads/MrKhaimi/MagmaKey/total?label=downloads)](../../releases)

---

## ✨ Features

- 🌋 Hypnotic "lava lamp" animation (amber and cold themes)
- 🔐 Generates three cryptographically strong passwords at once
- 🧩 Two modes: classic passwords and memorable phrases (Diceware)
- 📊 Strength evaluation: Weak / Medium / Strong / Maximum
- 🔍 Detailed weak‑spot analysis (missing uppercase, digits, special chars, etc.)
- ⏱ Crack time estimation for each password
- 🧪 Offline check against a list of common leaked passwords (Top 100)
- 📲 QR code for each password – instantly transfer to your phone
- 👁 Toggle password visibility (show / hide)
- 🔊 Sound confirmation on copy
- 📋 One‑click copy to clipboard
- 🔍 Built‑in password strength checker for any custom password
- 📜 History of the last 12 generated passwords
- 💾 Save passwords to a text file on your desktop
- ⚙️ Flexible settings: password length (4–128), uppercase / lowercase letters, digits, special characters
- 🔒 Incognito mode – automatically clears passwords and history on exit
- 💾 Settings are automatically saved between sessions
- 🖼️ Custom icon in the window and on the taskbar
- 🛡️ Source code protection (PyArmor) and watermark "by MrKhaimi"
- 🔒 **Fully offline** – never connects to the internet

---

## 📥 Download

The latest version is available in the [Releases](https://github.com/MrKhaimi/MagmaKey/releases) section.

- 🛠 **MagmaKey_Setup.exe** – Windows installer (with shortcuts)
- 🟢 **MagmaKey.exe** – portable version (no installation required)

---

## 🖥️ Technologies

- **Python 3.12+**
- **PyQt6** – GUI and animation
- **PyInstaller** – EXE packaging
- **PyArmor** – obfuscation and code protection
- **Inno Setup** – installer creation

This project will be signed using a certificate provided by the SignPath Foundation.
---

## 🛠 Build from source

```bash
git clone https://github.com/MrKhaimi/MagmaKey.git
cd MagmaKey
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
