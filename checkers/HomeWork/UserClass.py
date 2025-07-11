import random
import string
import sys
import os


def get_base_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class User:
    def __init__(self, realname: str, username: str, password: str):
        self.realname = realname
        self.username = username
        self.password = password

    @staticmethod
    def read_words_from_file(filename):
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    @staticmethod
    def transliterate(text):
        translit_map = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "Є": "e",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "y",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "kh",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
        }
        result = ""
        for char in text.lower():
            result += str(translit_map.get(char, char))
        return result

    @classmethod
    def generate_username(cls, name, surname):
        base_username = cls.transliterate(name + surname)
        add_number = random.choice([True, False])
        if add_number:
            choice = random.choice(["digits", "year"])
            if choice == "digits":
                digits_count = random.randint(1, 4)
                digits = "".join(random.choices(string.digits, k=digits_count))
                username = base_username + digits
            else:
                year = str(random.randint(1950, 2025))
                username = base_username + year
        else:
            username = base_username
        return username

    @classmethod
    def generate(cls):
        BASE_DIR = get_base_path()
        DATA_DIR = os.path.join(BASE_DIR, "Data_for_generations")

        male_names_path = os.path.join(DATA_DIR, "male_names_rus.txt")
        male_names = cls.read_words_from_file(
            os.path.join(DATA_DIR, "male_names_rus.txt")
        )
        male_surnames = cls.read_words_from_file(
            os.path.join(DATA_DIR, "male_surnames_rus.txt")
        )
        female_names = cls.read_words_from_file(
            os.path.join(DATA_DIR, "female_names_rus.txt")
        )
        female_surnames = cls.read_words_from_file(
            os.path.join(DATA_DIR, "female_surnames_rus.txt")
        )

        gender = random.choice(["male", "female"])
        if gender == "male":
            name = random.choice(male_names)
            surname = random.choice(male_surnames)
        else:
            name = random.choice(female_names)
            surname = random.choice(female_surnames)

        realname = f"{name} {surname}"
        username = cls.generate_username(name, surname)
        password_chars = string.ascii_letters + string.digits
        password = "".join(
            random.choice(password_chars) for _ in range(12)
        )

        return cls(realname, username, password)

    def print_logs(self):
        print(
            f"realname: {self.realname}\nusername: {self.username}\npassword: {self.password}"
        )
