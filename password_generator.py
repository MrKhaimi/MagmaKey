import secrets
import string
import math

class PasswordGenerator:
    @staticmethod
    def generate(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
        length = max(4, min(128, length))
        char_pool = ""
        if use_lower:
            char_pool += string.ascii_lowercase
        if use_upper:
            char_pool += string.ascii_uppercase
        if use_digits:
            char_pool += string.digits
        if use_special:
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not char_pool:
            char_pool = string.ascii_lowercase
            use_lower = True

        password = ''.join(secrets.choice(char_pool) for _ in range(length))
        return password, char_pool


class StrengthEvaluator:
    @staticmethod
    def evaluate(password, char_pool):
        if not password or not char_pool:
            return 0.0, "Низкая"
        R = len(char_pool)
        L = len(password)
        entropy = L * math.log2(R) if R > 0 else 0.0

        if entropy < 40:
            return entropy, "Низкая"
        elif entropy < 60:
            return entropy, "Средняя"
        elif entropy < 80:
            return entropy, "Высокая"
        else:
            return entropy, "Максимальная"