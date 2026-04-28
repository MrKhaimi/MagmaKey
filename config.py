from PyQt6.QtCore import QSettings

class Config:
    def __init__(self):
        self.settings = QSettings("MagmaKey", "MagmaKeyApp")
        self.defaults = {
            "length": 16,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True
        }

    def get(self, key, type=str):
        val = self.settings.value(key, self.defaults.get(key))
        if type == bool:
            if isinstance(val, str):
                return val.lower() == 'true'
            return bool(val)
        if type == int:
            return int(val)
        return val

    def set(self, key, value):
        self.settings.setValue(key, value)

    def save_checkbox(self, key, state):
        self.set(key, bool(state))

    def save_slider(self, key, value):
        self.set(key, int(value))