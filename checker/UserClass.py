import random
import string


class User:
    def __init__(self, username: str, login: str, password: str):
        self.username = username
        self.login = login
        self.password = password

    @staticmethod
    def read_words_from_file(filename):
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    @staticmethod
    def transliterate(text):
        # Таблица замены русских букв на английские аналоги
        translit_map = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "e",
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
            result += translit_map[char]
        return result

    @classmethod
    def generate_login(cls, name, surname):
        base_login = cls.transliterate(name + surname)

        # Случайно решаем, добавлять ли цифры/год
        add_number = random.choice([True, False])
        if add_number:
            choice = random.choice(["digits", "year"])
            if choice == "digits":
                # Добавляем от 1 до 4 случайных цифр
                digits_count = random.randint(1, 4)
                digits = "".join(random.choices(string.digits, k=digits_count))
                login = base_login + digits
            else:
                # Добавляем случайный год из диапазона 1950-2025
                year = str(random.randint(1950, 2025))
                login = base_login + year
        else:
            login = base_login

        return login

    @classmethod
    def generate(cls):
        male_names = cls.read_words_from_file("Data_for_generations/male_names_rus.txt")
        male_surnames = cls.read_words_from_file(
            "Data_for_generations/male_surnames_rus.txt"
        )
        female_names = cls.read_words_from_file(
            "Data_for_generations/female_names_rus.txt"
        )
        female_surnames = cls.read_words_from_file(
            "Data_for_generations/female_surnames_rus.txt"
        )

        gender = random.choice(["male", "female"])

        if gender == "male":
            name = random.choice(male_names)
            surname = random.choice(male_surnames)
        elif gender == "female":
            name = random.choice(female_names)
            surname = random.choice(female_surnames)

        username = f"{name} {surname}"
        login = cls.generate_login(name, surname)

        password_chars = string.ascii_letters + string.digits
        password = "".join(random.choice(password_chars) for _ in range(8))

        return cls(username, login, password)

    def printLogs(self):
        print(
            f"username: {self.username}\nlogin: {self.login}\npassword: {self.password}"
        )


print("Debug start1")
user = User.generate()

User.printLogs(user)
