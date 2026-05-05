#!/usr/bin/env python3
# Copyright © 2026, MrKhaimi Все права защищены.

import secrets
import string
import math

# Список из 300 русских существительных для запоминающихся фраз
WORD_LIST = [
    "август", "авиа", "автор", "агент", "актив", "алмаз", "альфа", "анализ", "арена", "архив",
    "база", "баланс", "банк", "бар", "башня", "бег", "берег", "билет", "блок", "блюдо",
    "бой", "болт", "брат", "буря", "вагон", "валет", "вата", "вектор", "весна", "ветер",
    "вечер", "взлёт", "взрыв", "вилка", "винт", "вирус", "вклад", "волк", "воск", "врач",
    "гавань", "газета", "гамма", "гвоздь", "герой", "гимн", "глаз", "голос", "гора", "град",
    "грамм", "грань", "гриб", "гроза", "груз", "грунт", "гул", "дама", "дверь", "двигатель",
    "дед", "дерево", "диск", "дождь", "док", "доля", "дом", "дракон", "друг", "дуб",
    "дым", "егерь", "еди", "ель", "ёмкость", "жар", "жест", "жила", "журнал", "завод",
    "закат", "залив", "замок", "заря", "звезда", "зверь", "земля", "зерно", "зима", "знак",
    "игрок", "идея", "изгиб", "индекс", "искра", "кадр", "камень", "канал", "капля", "квест",
    "кедр", "кисть", "класс", "клён", "клин", "клуб", "ключ", "книга", "ковёр", "код",
    "кол", "кольцо", "конь", "копьё", "корень", "корт", "костёр", "край", "кран", "крем",
    "круг", "куб", "кулак", "лава", "лань", "легенда", "лён", "лес", "лето", "лимон",
    "линия", "лист", "лоб", "лов", "ложь", "локоть", "лом", "луна", "луч", "лыжа",
    "маг", "май", "мак", "масло", "машина", "медь", "мел", "метод", "мех", "мина",
    "мир", "мозг", "молот", "морж", "мороз", "мост", "мох", "муж", "мыс", "мясо",
    "набор", "налог", "небо", "нитка", "нож", "номер", "нора", "нос", "оба", "обод",
    "овраг", "окно", "олень", "опера", "орёл", "орех", "осень", "осина", "очаг", "палец",
    "пар", "пасть", "пень", "пиво", "пик", "пир", "план", "плод", "плот", "плющ",
    "пол", "поле", "полк", "порт", "пост", "приз", "пруд", "пульт", "пыль", "пята",
    "радар", "рай", "рама", "риф", "рог", "род", "роза", "ром", "рост", "рот",
    "рука", "рысь", "ряд", "сабан", "салат", "сан", "сахар", "сбор", "свет", "свист",
    "село", "семь", "сено", "серп", "сеть", "сигма", "сила", "скала", "скот", "след",
    "слон", "смех", "снег", "сок", "сон", "сорт", "спорт", "ствол", "стол", "стул",
    "суп", "сучок", "сфера", "сын", "таз", "танк", "тара", "тень", "тест", "тигр",
    "ток", "толк", "тор", "точка", "труба", "тыква", "тюль", "угол", "удар", "узел",
    "ум", "ус", "утро", "фаза", "факел", "факт", "фара", "ферзь", "флот", "фон",
    "хвост", "хлеб", "хмель", "холст", "храм", "цвет", "цель", "цикл", "чай", "час",
    "чек", "честь", "чин", "шаг", "шар", "шест", "шкала", "шлем", "шнур", "шок",
    "шорох", "штаб", "шум", "щель", "щит", "эра", "эхо", "юг", "яблоко", "яма"
]

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

    @staticmethod
    def generate_phrase(num_words=4, separator="-"):
        """Генерирует запоминающуюся фразу из нескольких слов."""
        if num_words < 3:
            num_words = 3
        elif num_words > 8:
            num_words = 8
        # криптостойкий выбор слов
        words = [secrets.choice(WORD_LIST) for _ in range(num_words)]
        phrase = separator.join(words)
        # алфавит для оценки – это сами слова плюс разделитель
        char_pool = " " + separator   # для оценки энтропии будем считать длину = количество слов, мощность = размер словаря
        return phrase, char_pool, len(WORD_LIST)   # третий элемент – размер словаря


class StrengthEvaluator:
    @staticmethod
    def evaluate(password, char_pool, wordlist_size=None):
        """Оценка энтропии. Если передан wordlist_size, считаем фразу."""
        if not password:
            return 0.0, "Низкая"
        if wordlist_size:
            # количество слов определяем по числу разделителей + 1
            parts = password.split("-") if "-" in password else [password]
            L = len(parts)
            R = wordlist_size
        else:
            if not char_pool:
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

    @staticmethod
    def crack_time(password, char_pool, wordlist_size=None):
        """Время взлома фразы или пароля."""
        if not password:
            return "Невозможно оценить"
        if wordlist_size:
            parts = password.split("-") if "-" in password else [password]
            L = len(parts)
            combinations = wordlist_size ** L
        else:
            if not char_pool:
                return "Невозможно оценить"
            R = len(char_pool)
            L = len(password)
            combinations = R ** L
        seconds = combinations / 1_000_000_000   # 1 млрд/сек GPU
        if seconds < 60:
            return f"Взлом: → {int(seconds)} сек"
        elif seconds < 3600:
            return f"Взлом: → {int(seconds // 60)} мин"
        elif seconds < 86400:
            return f"Взлом: → {int(seconds // 3600)} ч"
        elif seconds < 31536000:
            return f"Взлом: → {int(seconds // 86400)} дн"
        elif seconds < 31536000 * 100:
            return f"Взлом: → {seconds / 31536000:.1f} лет"
        else:
            if seconds > 1e50:
                return "Взлом: → >> возраста Вселенной"
            elif seconds > 1e30:
                return f"Взлом: → {seconds / 31536000:.0f} лет"
            else:
                return f"Взлом: → {seconds / 31536000:.1f} лет"
