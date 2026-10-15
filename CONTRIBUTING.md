# Contributing to MagmaKey

Thank you for your interest in contributing to MagmaKey! 🎉
We welcome bug reports, feature requests, documentation improvements, and code contributions.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [License](#license)

---

## Code of Conduct

Be respectful and constructive. We are all here to learn and build something useful together.
Harassment, trolling, or offensive behavior will not be tolerated.

---

## How Can I Contribute?

### 🐞 Reporting Bugs

Before creating a bug report, please check the [existing issues](https://github.com/MrKhaimi/MagmaKey/issues)
to avoid duplicates.

When reporting a bug, please include:
- Your OS version (Windows 7 / 10 / 11)
- MagmaKey version
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots or logs (if applicable)

### 💡 Suggesting Features

Open an issue with the label `enhancement` and describe:
- What problem the feature solves
- How you imagine it working
- Any alternatives you considered

### 📝 Improving Documentation

Typos, unclear explanations, or missing examples — all welcome! Just open a PR.

### 💻 Contributing Code

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Test locally (`python main.py`).
5. Commit: `git commit -m "Add: short description"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request.

---

## Development Setup

### Requirements
- Python 3.12+ (for the main version)
- Python 3.8+ (for the Windows 7 version)
- PyQt6 (main) or PyQt5 (Windows 7)

### Installation

```bash
git clone https://github.com/MrKhaimi/MagmaKey.git
cd MagmaKey
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
