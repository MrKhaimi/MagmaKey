from kivy.storage.jsonstore import JsonStore

class Config:
    def __init__(self):
        self.store = JsonStore('magmakey_config.json')
        self.defaults = {
            "length": 16,
            "use_upper": True,
            "use_lower": True,
            "use_digits": True,
            "use_special": True
        }

    def get(self, key):
        if self.store.exists(key):
            val = self.store.get(key)[key]
            return val
        return self.defaults.get(key)

    def set(self, key, value):
        self.store.put(key, **{key: value})