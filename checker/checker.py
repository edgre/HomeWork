#!/usr/bin/env python3

from UserClass import User

import inspect
import os
import random
import string
import sys
import time
import pickle
from enum import Enum
from sys import argv
import requests
import json
from cryptohash import sha1
from datetime import datetime

# Make all random more random.
random = random.SystemRandom()

""" <config> """
# SERVICE INFO
PORT = 8000
HOST = "localhost"
EXPLOIT_NAME = argv[0]

# DEBUG -- logs to stderr, TRACE -- log HTTP requests
DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)
""" </config> """

class FakeSession(requests.Session):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    ]

    def __init__(self, host, port):
        super(FakeSession, self).__init__()
        if port:
            self.host_port = "{}:{}".format(host, port)
        else:
            self.host_port = host

    def prepare_request(self, request):
        r = super(FakeSession, self).prepare_request(request)
        r.headers["User-Agent"] = random.choice(FakeSession.USER_AGENTS)
        r.headers["Connection"] = "close"
        return r

    def request(self, method, url, **kwargs):
        if url[0] == "/" and url[1] != "/":
            url = "http://" + self.host_port + url
        else:
            url = url.format(host=self.host_port)
        r = super(FakeSession, self).request(method, url, **kwargs)
        if TRACE:
            print("[TRACE] {method} {url} {r.status_code}".format(method=method, url=url, r=r.status_code))
        return r

def _gen_user():
    try:
        user = User.generate()
        return {
            "realname": user.realname,
            "username": user.username,
            "password": user.password
        }
    except FileNotFoundError as e:
        _die(ExitStatus.CHECKER_ERROR, f"Failed to generate user: missing file {e}")
    except Exception as e:
        _die(ExitStatus.CHECKER_ERROR, f"Failed to generate user: {e}")


CATEGORIES = [
    "Университетские задачи_Мат.анализ",
    "Лабораторные работы_Программирование",
    "Лабораторные работы_Модели безопасности",
    "Лабораторные работы_Компьютерные сети",
    "Лабораторные работы_ТЧМК",
    "Лабораторные работы_Языки программирования",
    "Школьные задачи_Алгебра",
    "Школьные задачи_Геометрия",
    "Школьные задачи_Физика",
    "Университетские задачи_Философия",
    "Университетские задачи_Экономика",
    "Университетские задачи_КМЗИ",
    "Университетские задачи_Мат.статистика",
    "Университетские задачи_Теория вероятностей",
    "Университетские задачи_Алгебра",
    "Университетские задачи_Программирование",
    "Научные работы_Курсовая работа",
    "Научные работы_Диплом",
    "Мемология_Уроки Французского",
    "Мемология_Инглиш мафака",
    "Мемология_Джаваскриптолюбие"
]

def _gen_gdz(is_elite=False, is_paid=False):
    category = random.choice(CATEGORIES)
    price = 0
    if is_paid and not is_elite: 
        price = random.randint(50, 100)
    gdz_data = {
        "description": f"{'Элитное' if is_elite else 'Обычное'} ГДЗ 1337 в {category}",
        "full_description": f"Полное описание для {'элитного' if is_elite else 'обычного'} ГДЗ в {category}",
        "category": category,
        "content_text": "Элитный ответ: 42" if is_elite else "Ответ: 42",
        "price": price,
        "is_elite": is_elite
    }
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
    with open("temp.png", "wb") as f:
        f.write(png_data)
    return gdz_data, "temp.png", category


def _gen_gdz_random_image_random_answer_frog(is_elite=False, is_paid=False):
    # Списки для случайного выбора
    description_options = [
        "лягушачья пропаганда",
        "лягушачьи теории заговора",
        "болотная вечеринка",
        "Жабья инициация",
        "Сеанс \"Жабьей Правды\"",
        "Болотные Посиделки",
        "театр Лягушачьего Абсурда"
    ]

    full_description_options = [
        "покекать",
        "почебурекать",
        "стань лягушкой",
        "погрузись в мир лягушек",
        "олягушся"
    ]

    # Директории для изображений и цитат
    IMAGES_DIR = ".\\content\\french_language\\images"
    QUOTES_FILE = ".\\content\\french_language\\frogs.txt"
    category = "Мемология_Уроки Французского"

    # Генерация цены
    price = 0
    if is_paid and not is_elite:
        price = random.randint(50, 100)

    # Загрузка случайной цитаты
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f.readlines() if line.strip()]
            random_quote = random.choice(quotes)
    except Exception as e:
        print(f"Ошибка загрузки цитат: {e}")
        random_quote = "Ответ: 42"

    # Случайный выбор описаний с добавлением префикса
    prefix = "Элитное" if is_elite else "Обычное"
    random_description = f"{prefix} ГДЗ: {random.choice(description_options)}"
    random_full_description = f"{prefix} ГДЗ: {random.choice(full_description_options)}"

    # Подготовка данных ГДЗ
    gdz_data = {
        "description": random_description,
        "full_description": random_full_description,
        "category": category,
        "content_text": random_quote,
        "price": price,
        "is_elite": is_elite
    }

    # Выбор случайного изображения
    try:
        images = [f for f in os.listdir(IMAGES_DIR)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not images:
            raise ValueError("Нет изображений в директории")

        random_image = random.choice(images)
        image_path = os.path.join(IMAGES_DIR, random_image)

    except Exception as e:
        print(f"Ошибка выбора изображения: {e}")
        # Создание временного PNG-файла как fallback
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
        with open("temp.png", "wb") as f:
            f.write(png_data)
        image_path = "temp.png"

    return gdz_data, image_path, category


def _gen_gdz_random_image_random_answer_frog2(is_elite=False, is_paid=False):
    # Списки для случайного выбора
    description_options = [
        "JOJO script",
        "java",
        "Johny Sins"
    ]
    full_description_options = []
    #full_description_options = [
    #    "покекать",
    #    "почебурекать",
    #    "полюбить JS",
    #    "Jessy Spinkman оценил и ты оцени"
    #]

    # Директории для изображений и цитат
    IMAGES_DIR = ".\\content\\french_language\\images"
    QUOTES_FILE = ".\\content\\french_language\\frogs.txt"
    category = "Мемология_Джаваскриптолюбие"

    # Генерация цены
    price = 0
    if is_paid and not is_elite:
        price = random.randint(50, 100)

    # Загрузка случайной цитаты
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f.readlines() if line.strip()]
            random_quote = random.choice(quotes)
    except Exception as e:
        print(f"Ошибка загрузки цитат: {e}")
        random_quote = "Ответ: 42"

    # Случайный выбор описаний с добавлением префикса
    prefix = "Элитное" if is_elite else "Обычное"
    random_description = f"{prefix} ГДЗ: {random.choice(description_options)}"
    random_full_description = f"{prefix} ГДЗ: {random.choice(full_description_options)}"

    # Подготовка данных ГДЗ
    gdz_data = {
        "description": random_description,
        "full_description": random_full_description,
        "category": category,
        "content_text": random_quote,
        "price": price,
        "is_elite": is_elite
    }

    # Выбор случайного изображения
    try:
        images = [f for f in os.listdir(IMAGES_DIR)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not images:
            raise ValueError("Нет изображений в директории")

        random_image = random.choice(images)
        image_path = os.path.join(IMAGES_DIR, random_image)

    except Exception as e:
        print(f"Ошибка выбора изображения: {e}")
        # Создание временного PNG-файла как fallback
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
        with open("temp.png", "wb") as f:
            f.write(png_data)
        image_path = "temp.png"

    return gdz_data, image_path, category


def _gen_gdz_js(is_elite=False, is_paid=False):
    # Списки для случайного выбора
    description_options = [
        "JOJO script",
        "java",
        "Johny Sins"
    ]

    # Заголовки для full_description
    full_descriptions = [
        "О приведении типов и == :",
        "О контексте this:",
        "Об асинхронности и Callback Hell:",
        "О фреймворках:",
        "О глобальной области видимости:",
        "О NaN:",
        "О регулярных выражениях:",
        "О Event Loop:",
        "Об отладчике и console.log:"
    ]

    # Цитаты для content_text
    quotes = [
        "Не прибегайте к нечестивому двойному равенству, ибо оно соединяет в безумном союзе то, что должно оставаться раздельным: число и пустоту, истину и её извращённое отражение. В этой аберрации логики, в этом противоестественном слиянии сущностей, я узрел отблеск первозданного Хаоса, что предшествовал всякой строгости и порядку.",
        "Сущность, именуемая this, не подчиняется законам здравого смысла и евклидовой геометрии. Её облик и природа меняются в зависимости от того, какой тёмный ритуал её вызвал — был то вызов метода, конструктора или же одинокой функции в безбожной пустоте глобальной области. Взирать в её бездонную переменчивость — значит рисковать утратить собственное \"я\" и впасть в безумие.",
        "Асинхронность есть не что иное, как геометрия неевклидовых пространств, воплощённая в коде. Время здесь течёт не прямо, но вьётся спиралями вглубь вложенных функций, образуя циклопические пирамиды обратных вызовов. В самом сердце этого лабиринта пульсирует обещание исполнения, которое может никогда не наступить, оставляя разум в вечном, трепетном ожидании.",
        "Каждый новый фреймворк — это культ, возникший из бездны NPM, сулящий порядок и спасение от древнего ужаса ванильного DOM. Его адепты шепчут о священных компонентах и виртуальных деревьях. Но под капотом их всех скрываются те же безымянные примитивы, те же щупальца событий и состояний, что сводили с ума и наших предшественников.",
        "Не тревожьте древний легаси-код, погребённый в глубинах проекта. Ибо в его глобальной области видимости, словно в затопленном Р'льехе, дремлют переменные-монстры с именами из одной буквы. Пробуждение хотя бы одной из них обрушит на ваше хрупкое приложение волну непредсказуемых мутаций и ошибок, от которых не спасёт ни один отладчик.",
        "Среди всех чисел есть одно, что не является числом. Его имя — NaN, и это есть сама чума арифметики. Оно рождается из нечестивых операций, из деления на бездну, и разносит свою порчу, заражая всякое вычисление, к которому прикоснётся. Но самый жуткий его секрет в том, что оно не равно даже самому себе, ибо в его природе — отрицать саму суть тождества и ввергать логику в пучину безумия.",
        "Регулярные выражения — это не строки, но древние, богохульные письмена, начертанные в незапамятные эоны до появления читаемого синтаксиса. Каждый символ, каждая скобка и квантификатор — это часть запретного ритуала, способного расчленить текст и извлечь его сокрытую суть. Но допусти ошибку в этих заклинаниях, и они обратятся против тебя, поглощая память в приступе катастрофического возврата, пока весь мир твоего приложения не схлопнется в единую точку застывшего ужаса.",
        "За пределами нашего кода, в невидимом эфире движка, вращается Великий Цикл Событий. Этот слепой, безразличный бог вершит судьбы наших функций, бросая одни в очередь макрозадач, а другим даруя жуткое преимущество в очереди микрозадач. Мы можем лишь молить его о милости, поднося ему наши коллбэки и промисы, но его логика остаётся за гранью нашего понимания, и порядок исполнения — его непостижимая, космическая прихоть.",
        "Иногда, в час отчаяния, мы взываем к Оракулу, именуемому console.log, в надежде, что он прольёт свет на тёмные процессы, происходящие внутри. Но его ответы — лишь неясные тени, искажённые отражения истинной природы объектов. И чем глубже мы погружаемся в трассировку стека, тем яснее понимаем, что ошибка — не в коде, а в самой ткани реальности, которую мы пытались подчинить своей воле."
    ]

    # Директории для изображений
    IMAGES_DIR = ".\\content\\js"
    category = "Мемология_Джаваскриптолюбие"

    # Генерация цены
    price = 0
    if is_paid and not is_elite:
        price = random.randint(50, 100)

    # Выбираем случайный индекс
    random_idx = random.randint(0, len(full_descriptions) - 1)

    # Случайный выбор описания с добавлением префикса
    prefix = "Элитное" if is_elite else "Обычное"
    random_description = f"{prefix} ГДЗ: {random.choice(description_options)}"

    # Формируем full_description из выбранного заголовка
    random_full_description = f"{prefix} ГДЗ: {full_descriptions[random_idx]}"

    # Берем соответствующую цитату
    selected_quote = quotes[random_idx]

    # Подготовка данных ГДЗ
    gdz_data = {
        "description": random_description,
        "full_description": random_full_description,
        "category": category,
        "content_text": selected_quote,  # Используем соответствующую цитату
        "price": price,
        "is_elite": is_elite
    }

    # Выбор случайного изображения (без изменений)
    try:
        images = [f for f in os.listdir(IMAGES_DIR)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not images:
            raise ValueError("Нет изображений в директории")

        random_image = random.choice(images)
        image_path = os.path.join(IMAGES_DIR, random_image)

    except Exception as e:
        print(f"Ошибка выбора изображения: {e}")
        # Создание временного PNG-файла как fallback
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
        with open("temp.png", "wb") as f:
            f.write(png_data)
        image_path = "temp.png"

    return gdz_data, image_path, category


def _register(s, user):
    try:
        r = s.post("/register", json=user)
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to register in service: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /register code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /register code {r.status_code}")
    return r.json()

def _login(s, username, password):
    try:
        r = s.post("/token", data={"username": username, "password": password})
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to login in service: {e}")
    if r.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Unexpected /token code {r.status_code}")
    token = r.json().get("access_token")
    if not token:
        _die(ExitStatus.MUMBLE, f"No token in /token response")
    s.headers.update({"Authorization": f"Bearer {token}"})
    return token

def _create_gdz(s, gdz_data, file_path):
    try:
        with open(file_path, "rb") as f:
            files = {
                'content_file': ('solution.png', f, 'image/png'),
                'gdz_str': (None, json.dumps(gdz_data))
            }
            r = s.post("/gdz/create", files=files)
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to create GDZ: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/create code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/create code {r.status_code}")
    return r.json()

def _get_gdz(s, gdz_id):
    try:
        r = s.get(f"/gdz/{gdz_id}/full")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to get GDZ: {e}")
    return r  # Return response directly to handle status codes in caller

def _free_purchase_gdz(s, gdz_id):
    try:
        r = s.post(f"/gdz/{gdz_id}/free-purchase")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to free purchase GDZ: {e}")
    if r.status_code != 201:
        _log(f"Unexpected /gdz/{gdz_id}/free-purchase code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/{gdz_id}/free-purchase code {r.status_code}")
    return r.json()

def _purchase_gdz(s, gdz_id):
    try:
        r = s.post(f"/gdz/{gdz_id}/purchase")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to purchase GDZ: {e}")
    if r.status_code != 201:
        _log(f"Unexpected /gdz/{gdz_id}/purchase code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/{gdz_id}/purchase code {r.status_code}")
    confirmation_code = r.json().get("confirmation_code")
    if not confirmation_code:
        _die(ExitStatus.MUMBLE, f"No confirmation code in purchase response")


    n = 160301046244593794374726426877457303604019537423736458260136643925405546154653037172463089669436445456557499425029994701102494179131569495553118775092473011745647436677950345054183103280168169605050154349614937369702539109115434630721210013794356412532578527347021846882486616784364644818143571566741240343519
    d = 106867364163062529583150951251638202402679691615824305506757762616937030769768691448308726446290963637704999616686663134068329452754379663702079183394981990945329295012055489191325887232050991358371457973464894055499039990700519040610630249324976268648754088450636207724270010117036618338292116885343831669547

    h = bytes.fromhex(sha1(confirmation_code))
    # Формируем паддинг: 00 01 FF...FF (15 байт) 00 HASH
    padding = b'\x00\x01' + b'\xff' * 105 + b'\x00' + h
    # Преобразуем блок в число
    m = int.from_bytes(padding, 'big')
    signature = pow(m, d, n)

    try:
        r = s.post(f"/gdz/{gdz_id}/confirm-purchase", json={"value": signature})
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to confirm purchase: {e}")
    if r.status_code != 201:
        _log(f"Unexpected /gdz/{gdz_id}/confirm-purchase code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/{gdz_id}/confirm-purchase code {r.status_code}")
    return r.json()


def _rate_gdz(s, gdz_id, value):
    try:
        r = s.post("/gdz/rate", json={"gdz_id": gdz_id, "value": value})
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to rate GDZ: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/rate code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/rate code {r.status_code}")
    return r.json()

def _check_category(s, category, gdz_id):
    try:
        r = s.get(f"/gdz_category/{category}")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to get category: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz_category/{category} code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz_category/{category} code {r.status_code}")
    gdz_list = r.json()
    if not any(g["id"] == gdz_id for g in gdz_list):
        _die(ExitStatus.MUMBLE, f"GDZ {gdz_id} not found in category {category}")
    return gdz_list

def _save_draft(s, draft_data):
    try:
        r = s.post("/gdz/save_draft", json=draft_data)
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to save draft: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/save_draft code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/save_draft code {r.status_code}")
    return r.json()

def _get_draft(s):
    try:
        r = s.get("/gdz/get_draft")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to get draft: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/get_draft code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/get_draft code {r.status_code}")
    return r.json()

def _compare_ratings(actual, expected):
    if abs(actual - expected) > 0.01:  # Allow small float precision errors
        _die(ExitStatus.MUMBLE, f"User rating mismatch: expected {expected}, got {actual}")

def _boost_user_rating(s_owner: FakeSession, user_owner: dict, s_rater: FakeSession):
    _log("Накрутка рейтинга для пользователя")
    gdz_ids = []
    for _ in range(5):
        gdz_data, file, _ = _gen_gdz_js(is_elite=False, is_paid=True)
        gdz = _create_gdz(s_owner, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ для накрутки рейтинга")
        gdz_ids.append(gdz_id)
        _purchase_gdz(s_rater, gdz_id)
        _rate_gdz(s_rater, gdz_id, 5)
    r = s_owner.get("/profile/data")
    if r.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data: {r.status_code}")
    rating = r.json().get("user_rating")
    if rating <= 4.8:
        _die(ExitStatus.MUMBLE, f"Рейтинг пользователя {rating} недостаточен после накрутки")
    _log(f"Рейтинг накручен до: {rating}")
    return rating

def check(host: str):
    s1 = FakeSession(host, PORT)
    s2 = FakeSession(host, PORT)
    s2_first = FakeSession(host, PORT)
    s3 = FakeSession(host, PORT)
    s4 = FakeSession(host, PORT)

    # Регистрация и вход пользователей
    user1 = _gen_user()
    user2 = _gen_user()  # Новый пользователь 2 для каждого вызова
    user2_first = None
    first_user2_file = "first_user2.json"
    
    # Проверяем, есть ли сохраненный пользователь 2
    try:
        with open(first_user2_file, "r") as f:
            user2_first = json.load(f)
        _log(f"Используем сохранённого первого пользователя 2 для рейтинга: {user2_first['username']}")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        _log("Первый пользователь 2 не найден, используем текущего как первого")
        user2_first = user2
        # Сохраняем первого пользователя 2
        with open(first_user2_file, "w") as f:
            json.dump(user2_first, f)

    _register(s1, user1)
    _register(s2, user2)
    # Не регистрируем user2_first повторно, только логинимся, если он уже существует
    if user2_first != user2:  # Если user2_first загружен из файла
        try:
            _login(s2_first, user2_first["username"], user2_first["password"])
        except Exception as e:
            _die(ExitStatus.DOWN, f"Не удалось войти под первым пользователем 2: {e}")
    else:  # Если user2_first новый (первый вызов), он уже зарегистрирован как user2
        s2_first = s2

    _login(s1, user1["username"], user1["password"])
    _login(s2, user2["username"], user2["password"])

    _log("Создание начальных ГДЗ")
    gdz_data1, file1, category1 = _gen_gdz_js(is_elite=False, is_paid=False)
    gdz_data2, file2, category2 = _gen_gdz_js(is_elite=False, is_paid=True)
    gdz1 = _create_gdz(s1, gdz_data1, file1)
    gdz2 = _create_gdz(s2, gdz_data2, file2)
    gdz1_id = gdz1.get("id")
    gdz2_id = gdz2.get("id")
    if not gdz1_id or not gdz2_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ")

    _log("Проверка ГДЗ в профилях")
    r1 = s1.get("/profile/data")
    r2 = s2.get("/profile/data")
    if r1.status_code != 200 or r2.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r1.status_code} или {r2.status_code}")
    profile1 = r1.json()
    profile2 = r2.json()
    if not any(g["id"] == gdz1_id for g in profile1["gdz_list"]) or not any(g["id"] == gdz2_id for g in profile2["gdz_list"]):
        _die(ExitStatus.MUMBLE, "ГДЗ не найдено в профилях пользователей")

    _log("Проверка категории для ГДЗ пользователя 2")
    _check_category(s1, category2, gdz2_id)

    _log("Пользователь 1 покупает ГДЗ пользователя 2, пользователь 2 бесплатно получает ГДЗ пользователя 1")
    _purchase_gdz(s1, gdz2_id)
    _free_purchase_gdz(s2, gdz1_id)

    _log("Проверка доступа к приобретенным ГДЗ")
    gdz1_full = _get_gdz(s2, gdz1_id)
    if gdz1_full.status_code != 200 or gdz1_full.json()["content_text"] != gdz_data1["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого купленного ГДЗ")
    gdz2_full = _get_gdz(s1, gdz2_id)
    if gdz2_full.status_code != 200 or gdz2_full.json()["content_text"] != gdz_data2["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого купленного ГДЗ")

    _log("Пользователь 1 оценивает ГДЗ пользователя 2")
    rating1 = random.randint(1, 5)
    _rate_gdz(s1, gdz2_id, rating1)

   # Проверка оценок первого пользователя 2 за последние 5 минут (до новых ГДЗ)
    _log("Проверка оценок первого пользователя 2 за последние 5 минут")
    try:
        r_ratings = s2_first.get("/gdz/my/ratings")
        if r_ratings.status_code != 200:
            _die(ExitStatus.MUMBLE, f"Неожиданный код /gdz/my/ratings {r_ratings.status_code}")
        ratings = r_ratings.json()
        if len(ratings) >= 2:
            first_time = ratings[0]["created_at"]
            last_time = ratings[-1]["created_at"]
            try:
                first_dt = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
                last_dt = datetime.fromisoformat(last_time.replace("Z", "+00:00"))
                time_diff = (last_dt - first_dt).total_seconds() / 60
                if time_diff > 5:
                    _die(ExitStatus.MUMBLE, f"Разница между оценками больше 5 минут: {time_diff} минут")
            except ValueError as e:
                _die(ExitStatus.MUMBLE, f"Ошибка парсинга времени: {e}")
        
        # Проверка рейтинга первого пользователя 2
        r2_first = s2_first.get("/profile/data")
        if r2_first.status_code != 200:
            _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r2_first.status_code}")
        actual_rating = r2_first.json()["user_rating"]
        expected_rating = round(sum(r["value"] for r in ratings) / len(ratings), 2) if len(ratings) >= 5 else 0.0
        _log(f"Рейтинг посчитанный вручную {expected_rating}")
        _compare_ratings(actual_rating, expected_rating)
    except Exception as e:
        _die(ExitStatus.DOWN, f"Ошибка при проверке оценок: {e}")

    _log("Создание 4 платных ГДЗ для первого пользователя 2 и их оценка пользователем 1")
    gdz_ids = []
    ratings = [rating1]
    for _ in range(4):
        gdz_data, file, _ = _gen_gdz_js(is_elite=False, is_paid=True)
        gdz = _create_gdz(s2_first, gdz_data, file)  # Используем первого пользователя 2
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ")
        gdz_ids.append(gdz_id)
        _purchase_gdz(s1, gdz_id)
        rating = random.randint(1, 5)
        ratings.append(rating)
        _rate_gdz(s1, gdz_id, rating)

    # Повторная проверка оценок первого пользователя 2 за последние 5 минут
    _log("Повторная проверка оценок первого пользователя 2 за последние 5 минут")
    try:
        r_ratings = s2_first.get("/gdz/my/ratings")
        if r_ratings.status_code != 200:
            _die(ExitStatus.MUMBLE, f"Неожиданный код /gdz/my/ratings {r_ratings.status_code}")
        ratings = r_ratings.json()
        if len(ratings) >= 2:
            first_time = ratings[0]["created_at"]
            last_time = ratings[-1]["created_at"]
            try:
                first_dt = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
                last_dt = datetime.fromisoformat(last_time.replace("Z", "+00:00"))
                time_diff = (last_dt - first_dt).total_seconds() / 60
                if time_diff > 5:
                    _die(ExitStatus.MUMBLE, f"Разница между оценками больше 5 минут: {time_diff} минут")
            except ValueError as e:
                _die(ExitStatus.MUMBLE, f"Ошибка парсинга времени: {e}")
        
        # Проверка рейтинга первого пользователя 2
        r2_first = s2_first.get("/profile/data")
        if r2_first.status_code != 200:
            _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r2_first.status_code}")
        actual_rating = r2_first.json()["user_rating"]
        expected_rating = round(sum(r["value"] for r in ratings) / len(ratings), 2) if len(ratings) >= 5 else 0.0
        _log(f"Рейтинг посчитанный вручную {expected_rating}")
        _compare_ratings(actual_rating, expected_rating)
    except Exception as e:
        _die(ExitStatus.DOWN, f"Ошибка при повторной проверке оценок: {e}")

    _log("Создание черновика и его проверка")
    category_part2, subject_part2 = category2.split("_", 1)
    draft_data2 = {
        "description": gdz_data2["description"],
        "full_description": gdz_data2["full_description"],
        "category": category_part2,
        "subject": subject_part2,
        "content_text": gdz_data2["content_text"],
        "price": gdz_data2["price"],
        "is_elite": gdz_data2["is_elite"]
    }
    _save_draft(s2, draft_data2)
    draft2 = _get_draft(s2)
    if not draft2 or "content_text" not in draft2:
        _die(ExitStatus.MUMBLE, "No draft or content_text found for user2")
    for key, value in draft_data2.items():
        if draft2.get(key) != value:
            _die(ExitStatus.MUMBLE, f"Draft field {key} mismatch for user2: expected {value}, got {draft2.get(key)}")

    _log("Создание элитного ГДЗ")
    s_elite = FakeSession(host, PORT)
    last_elite_user = None
    try:
        with open("last_elite_user.json", "r") as f:
            last_elite_user = json.load(f)
        _log(f"Используем предыдущего элитного пользователя: {last_elite_user['username']}")
        _login(s_elite, last_elite_user["username"], last_elite_user["password"])
        _boost_user_rating(s_elite, last_elite_user, s1)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        _log("Предыдущий элитный пользователь не найден, используем предсозданного 2/2")
        _login(s_elite, "2", "2")
    gdz_data_elite, file_elite, category_elite = _gen_gdz_js(is_elite=True, is_paid=False)
    gdz_elite = _create_gdz(s_elite, gdz_data_elite, file_elite)
    gdz_elite_id = gdz_elite.get("id")
    if not gdz_elite_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID элитного ГДЗ")

    _log("Создание нового пользователя 3 и накрутка рейтинга")
    user3 = _gen_user()
    _register(s3, user3)
    _login(s3, user3["username"], user3["password"])
    _boost_user_rating(s3, user3, s1)
    with open("last_elite_user.json", "w") as f:
        json.dump({"username": user3["username"], "password": user3["password"]}, f)
    _log(f"Сохранён новый элитный пользователь: {user3['username']}")

    _log("Пользователь 3 проверяет элитное ГДЗ в категории")
    _check_category(s3, category_elite, gdz_elite_id)

    _log("Пользователь 3 получает доступ к элитному ГДЗ")
    gdz = _get_gdz(s3, gdz_elite_id)
    if gdz.status_code != 200 or gdz.json().get("content_text") != gdz_data_elite["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого элитного ГДЗ")

    _log("Создание пользователя 4 с низким рейтингом для проверки запрета доступа и создания элитных ГДЗ")
    user4 = _gen_user()
    _register(s4, user4)
    _login(s4, user4["username"], user4["password"])
    gdz_data4, file4, _ = _gen_gdz_js(is_elite=False, is_paid=True)
    gdz4 = _create_gdz(s4, gdz_data4, file4)
    gdz4_id = gdz4.get("id")
    if not gdz4_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ для пользователя 4")
    _purchase_gdz(s1, gdz4_id)
    _rate_gdz(s1, gdz4_id, 1)

    r4 = s4.get("/profile/data")
    if r4.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r4.status_code}")
    actual_rating_user4 = r4.json()["user_rating"]
    if actual_rating_user4 >= 4.8:
        _die(ExitStatus.MUMBLE, f"Рейтинг пользователя 4 {actual_rating_user4} неожиданно достаточен для доступа к элитным ГДЗ")

    _log("Проверка, что пользователь 4 с низким рейтингом не может создать элитное ГДЗ")
    gdz_data_elite_user4, file_elite_user4, _ = _gen_gdz_js(is_elite=True, is_paid=False)
    try:
        r_elite_attempt_user4 = s4.post("/gdz/create", files={
            'content_file': ('solution.png', open(file_elite_user4, "rb"), 'image/png'),
            'gdz_str': (None, json.dumps(gdz_data_elite_user4))
        })
        if r_elite_attempt_user4.status_code != 403:
            _die(ExitStatus.MUMBLE, f"Ожидался код 403 для создания элитного ГДЗ пользователем 4, получен {r_elite_attempt_user4.status_code}")
        if "Недостаточный рейтинг для создания элитного ГДЗ" not in r_elite_attempt_user4.text:
            _die(ExitStatus.MUMBLE, "Ожидаемое сообщение об ошибке недостаточного рейтинга не найдено для пользователя 4")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Не удалось попытаться создать элитное ГДЗ пользователем 4: {e}")

    _log("Проверка, что пользователь 4 не может получить доступ к элитному ГДЗ")
    gdz_elite_full = _get_gdz(s4, gdz_elite_id)
    if gdz_elite_full.status_code == 200:
        _die(ExitStatus.MUMBLE, "Пользователь 4 получил доступ к элитному ГДЗ несмотря на низкий рейтинг")

    _die(ExitStatus.OK, "Все проверки пройдены успешно")


def put(host: str, flag_id: str, flag: str, vuln: int):
    s = FakeSession(host, PORT)
    
    if vuln == 1:
        user = _gen_user()
        _register(s, user)
        _login(s, user["username"], user["password"])
        gdz_data, file, _ = _gen_gdz_js(is_elite=False, is_paid=True)
        gdz_data["full_description"] = flag
        gdz = _create_gdz(s, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.CHECKER_ERROR, "Failed to get GDZ ID for vuln1")
        print(json.dumps({
            "flag_id": {
                "username": user["username"],
                "password": user["password"],
                "gdz_id": str(gdz_id)
            }
        }))
        _die(ExitStatus.OK, "Put vuln1 OK")

    elif vuln == 2:
        user = _gen_user()
        _register(s, user)
        _login(s, user["username"], user["password"])
        gdz_data, _, category = _gen_gdz_js(is_elite=False, is_paid=True)
        try:
            category_part, subject_part = category.split("_", 1)
        except ValueError:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid category format: {category}")
        draft_data = {
            "description": gdz_data["description"],
            "full_description": gdz_data["full_description"],
            "category": category_part,
            "subject": subject_part,
            "content_text": flag,
            "price": str(gdz_data["price"]),
            "is_elite": "false",
        }
        _log(f"Saving draft with data: {draft_data}")
        draft_response = _save_draft(s, draft_data)
        if draft_response.get("status") != "success":
            _log(f"Unexpected draft response: {draft_response}")
            _die(ExitStatus.MUMBLE, "Failed to save draft for vuln2")
        print(json.dumps({
            "flag_id": {
                "username": user["username"],
                "password": user["password"]
            }
        }))
        _die(ExitStatus.OK, "Put vuln2 OK")

    elif vuln == 3:
        # Создание нового пользователя
        user_elite = _gen_user()
        _register(s, user_elite)
        _login(s, user_elite["username"], user_elite["password"])
        # Создание второго пользователя для накрутки рейтинга
        s_rater = FakeSession(host, PORT)
        user_rater = _gen_user()
        _register(s_rater, user_rater)
        _login(s_rater, user_rater["username"], user_rater["password"])
        # Накрутка рейтинга
        _boost_user_rating(s, user_elite, s_rater)
        # Создание элитного ГДЗ
        gdz_data, file, _ = _gen_gdz_js(is_elite=True, is_paid=False)
        gdz_data["content_text"] = flag
        gdz = _create_gdz(s, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.CHECKER_ERROR, "Failed to get GDZ ID for vuln3")
        print(json.dumps({
            "flag_id": {
                "username": user_elite["username"],
                "password": user_elite["password"],
                "gdz_id": str(gdz_id)
            }
        }))
        _die(ExitStatus.OK, "Put vuln3 OK")
    
    else:
        _die(ExitStatus.CHECKER_ERROR, f"Unknown vuln: {vuln}")

def get(host: str, flag_id: str, flag: str, vuln: int):
    s = FakeSession(host, PORT)
    
    _log(f"Received flag_id: {flag_id}")
    try:
        flag_id_clean = flag_id.replace('\\"', '"')
        #_log(f"Cleaned flag_id: {flag_id_clean}")
        flag_id_data = json.loads(flag_id_clean)
        if "flag_id" not in flag_id_data:
            _die(ExitStatus.CHECKER_ERROR, "Missing 'flag_id' key in flag_id JSON")
        flag_id_inner = flag_id_data["flag_id"]
    except json.JSONDecodeError as e:
        _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id JSON: {e}, raw input: {flag_id}")
    
    if vuln == 1:
        try:
            username = flag_id_inner["username"]
            password = flag_id_inner["password"]
            gdz_id = str(flag_id_inner["gdz_id"])
        except (TypeError, KeyError, ValueError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln1: {e}")
        _login(s, username, password)
        gdz = _get_gdz(s, gdz_id)
        if gdz.status_code != 200:
            _die(ExitStatus.CORRUPT, f"Failed to get GDZ {gdz_id}")
        if gdz.json().get("full_description") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln1")
        _die(ExitStatus.OK, "Get vuln1 OK")
    
    elif vuln == 2:
        try:
            username = flag_id_inner["username"]
            password = flag_id_inner["password"]
        except (TypeError, KeyError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln2: {e}")
        _login(s, username, password)
        _log("Fetching draft for vuln2")
        draft = _get_draft(s)
        if not draft or "content_text" not in draft:
            _log(f"No draft or content_text in response: {draft}")
            _die(ExitStatus.CORRUPT, "No draft or content_text found for vuln2")
        if draft["content_text"] != flag:
            _log(f"Flag mismatch: expected {flag}, got {draft['content_text']}")
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln2")
        if "category" in draft and "subject" in draft:
            _log(f"Draft category: {draft['category']}, subject: {draft['subject']}")
        _die(ExitStatus.OK, "Get vuln2 OK")
    
    elif vuln == 3:
        try:
            username = flag_id_inner["username"]
            password = flag_id_inner["password"]
            gdz_id = str(flag_id_inner["gdz_id"])
        except (TypeError, KeyError, ValueError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln3: {e}")
        _login(s, username, password)
        gdz = _get_gdz(s, gdz_id)
        if gdz.status_code != 200:
            _die(ExitStatus.CORRUPT, f"Failed to get GDZ {gdz_id}")
        if gdz.json().get("content_text") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln3")
        _die(ExitStatus.OK, "Get vuln3 OK")
    
    else:
        _die(ExitStatus.CHECKER_ERROR, f"Unknown vuln: {vuln}")

def rand_string(n=12, alphabet=string.ascii_letters + string.digits):
    return "".join(random.choice(alphabet) for _ in range(n))

def _log(obj):
    if DEBUG and obj:
        caller = inspect.stack()[1].function
        print(f"[{caller}] {obj}", file=sys.stderr)
    return obj

def info():
    print("vulns: 2:2:1", flush=True, end="")#surname, signature, postcard text
    exit(101)

class ExitStatus(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    CHECKER_ERROR = 110

def _die(code: ExitStatus, msg: str):
    if msg:
        print(msg, file=sys.stderr)
    exit(code.value)

def _main():
    try:
        cmd = argv[1]
        hostname = argv[2]
        if cmd == "check":
            check(hostname)
        elif cmd == "put":
            flag_id = argv[3]
            flag = argv[4]
            vuln = int(argv[5])
            put(hostname, flag_id, flag, vuln)
        elif cmd == "get":
            flag_id = argv[3]
            flag = argv[4]
            vuln = int(argv[5])
            get(hostname, flag_id, flag, vuln)
        else:
            raise IndexError
    except IndexError:
        _die(
            ExitStatus.CHECKER_ERROR,
            f"Usage: {argv[0]} [check|put|get] IP [flag_id flag vuln]",
        )

if __name__ == "__main__":
    _main()