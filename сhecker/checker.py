#!/usr/bin/env python3

import html
import inspect
import json
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
import io

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
    usernames = [
        "Umnik", "Botanik", "Zubrila", "Geniy", "Uchenik", "Krutoy", "Vseznayka", "Neznayka", "Mudrets", "Guru", "Erudit"
    ]
    realnames = [
        "Ivan", "Anna", "Mikhail", "Olga", "Dmitriy", "Elena", "Sergey", "Natalya", "Andrey", "Marina",
        "Pavel", "Yuliya", "Alexey", "Svetlana", "Nikolay", "Tatyana", "Vladimir", "Ekaterina", "Igor", "Anastasia"
    ]
    username = f"{random.choice(usernames)}_{random.randint(1000, 9999)}"
    realname = random.choice(realnames)
    password = rand_string(12)
    return {"username": username, "realname": realname, "password": password}

CATEGORIES = [
    "Университетские задачи_Мат.анализ",
    "Лабораторные работы_Программирование",
    "Лабораторные работы_Модели безопасности",
    "Лабораторные работы_Сети",
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
    "Научные работы_Диплом"
]

def _gen_gdz(is_elite=False, is_paid=False):
    category = random.choice(CATEGORIES)
    price = 0
    if is_paid and not is_elite:  # Elite GDZ are always free
        price = random.randint(50, 100)
    gdz_data = {
        "description": f"{'Элитное' if is_elite else 'Обычное'} ГДЗ в {category}",
        "full_description": f"Полное описание для {'элитного' if is_elite else 'обычного'} ГДЗ в {category}",
        "category": category,
        "content_text": "Элитный ответ: 42" if is_elite else "Ответ: 42",
        "price": price,
        "is_elite": is_elite
    }
    # Generate a minimal PNG file
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
    with open("temp.png", "wb") as f:
        f.write(png_data)
    return gdz_data, "temp.png", category

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

    # Calculate signature: confirmation_code ^ d mod n
    d = 386870053273161916907984328001307348057048690563534755725698763638375412504055903963147549
    n = 967175133182904792269960820003268370142621728469171845263028425710252738044931468967566271
    signature = pow(int(confirmation_code), d, n)

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

def check(host: str):
    s1 = FakeSession(host, PORT)
    s2 = FakeSession(host, PORT)

    # Регистрация и вход двух пользователей
    user1 = _gen_user()
    user2 = _gen_user()
    _register(s1, user1)
    _register(s2, user2)
    _login(s1, user1["username"], user1["password"])
    _login(s2, user2["username"], user2["password"])

    _log("Создание начальных ГДЗ для обоих пользователей")
    # Пользователь 1 создает бесплатное неэлитное ГДЗ, пользователь 2 создает платное неэлитное ГДЗ
    gdz_data1, file1, category1 = _gen_gdz(is_elite=False, is_paid=False)
    gdz_data2, file2, category2 = _gen_gdz(is_elite=False, is_paid=True)
    gdz1 = _create_gdz(s1, gdz_data1, file1)
    gdz2 = _create_gdz(s2, gdz_data2, file2)
    gdz1_id = gdz1.get("id")
    gdz2_id = gdz2.get("id")
    if not gdz1_id or not gdz2_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ")

    _log("Проверка ГДЗ в профилях пользователей")
    # Проверка ГДЗ в профилях через /profile/data
    r1 = s1.get("/profile/data")
    r2 = s2.get("/profile/data")
    if r1.status_code != 200 or r2.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r1.status_code} или {r2.status_code}")
    profile1 = r1.json()
    profile2 = r2.json()
    if not any(g["id"] == gdz1_id for g in profile1["gdz_list"]) or not any(g["id"] == gdz2_id for g in profile2["gdz_list"]):
        _die(ExitStatus.MUMBLE, "ГДЗ не найдено в профилях пользователей")

    _log("Проверка категории для ГДЗ пользователя 2")
    # Пользователь 1 проверяет ГДЗ пользователя 2 в категории
    _check_category(s1, category2, gdz2_id)

    _log("Пользователь 1 покупает ГДЗ пользователя 2, пользователь 2 бесплатно получает ГДЗ пользователя 1")
    # Пользователь 1 покупает ГДЗ пользователя 2 (платное)
    _purchase_gdz(s1, gdz2_id)
    # Пользователь 2 бесплатно получает ГДЗ пользователя 1 (бесплатное)
    _free_purchase_gdz(s2, gdz1_id)

    _log("Проверка доступа к приобретенным ГДЗ")
    # Проверка доступа к купленным ГДЗ
    gdz1_full = _get_gdz(s2, gdz1_id)
    if gdz1_full.status_code != 200 or gdz1_full.json()["content_text"] != gdz_data1["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого купленного ГДЗ")
    gdz2_full = _get_gdz(s1, gdz2_id)
    if gdz2_full.status_code != 200 or gdz2_full.json()["content_text"] != gdz_data2["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого купленного ГДЗ")

    _log("Пользователь 1 оценивает ГДЗ пользователя 2")
    # Пользователь 1 оценивает ГДЗ пользователя 2 (случайная оценка)
    rating1 = random.randint(1, 5)
    _rate_gdz(s1, gdz2_id, rating1)

    _log("Сохранение и получение черновика для пользователя 2")
    # Пользователь 2 сохраняет и получает черновик
    draft_data = {
        "description": gdz_data2["description"],
        "full_description": gdz_data2["full_description"],
        "category": gdz_data2["category"],
        "content_text": gdz_data2["content_text"],
        "price": str(gdz_data2["price"]),
        "is_elite": "true" if gdz_data2["is_elite"] else "false",
        "gdz_id": str(gdz2_id)
    }
    #draft_response = _save_draft(s2, draft_data)
    #draft = _get_draft(s2)
    #if draft["description"] != draft_data["description"] or draft["category"] != draft_data["category"]:
    #    _die(ExitStatus.MUMBLE, "Несоответствие данных черновика")

    _log("Создание еще 4 платных ГДЗ для пользователя 2 и их оценка")
    # Пользователь 2 создает еще 4 платных ГДЗ
    gdz_ids = []
    ratings = [rating1]  # Включаем первую оценку
    for _ in range(4):
        gdz_data, file, _ = _gen_gdz(is_elite=False, is_paid=True)
        gdz = _create_gdz(s2, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ")
        gdz_ids.append(gdz_id)
        _purchase_gdz(s1, gdz_id)
        rating = random.randint(1, 5)
        ratings.append(rating)
        _rate_gdz(s1, gdz_id, rating)

    _log("Проверка рейтинга пользователя 2")
    # Проверка рейтинга пользователя 2
    r2 = s2.get("/profile/data")
    if r2.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r2.status_code}")
    actual_rating = r2.json()["user_rating"]
    expected_rating = round(sum(ratings[-5:]) / 5, 2)  # Последние 5 оценок
    _compare_ratings(actual_rating, expected_rating)

    _log("Проверка функциональности элитного ГДЗ")
    # Вход под элитным пользователем (username: 1, password: 1)
    s_elite = FakeSession(host, PORT)
    _login(s_elite, "2", "2")
    # Создание элитного ГДЗ
    gdz_data_elite, file_elite, category_elite = _gen_gdz(is_elite=True, is_paid=False)
    gdz_elite = _create_gdz(s_elite, gdz_data_elite, file_elite)
    gdz_elite_id = gdz_elite.get("id")
    if not gdz_elite_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID элитного ГДЗ")

    _log("Создание пользователя 3 и 5 ГДЗ для проверки доступа к элитным ГДЗ")
    # Создание пользователя 3
    s3 = FakeSession(host, PORT)
    user3 = _gen_user()
    _register(s3, user3)
    _login(s3, user3["username"], user3["password"])

    # Пользователь 3 создает 5 ГДЗ
    gdz_ids_user3 = []
    ratings_user3 = [5, 5, 5, 5, 5]  # Гарантируем рейтинг > 4.8
    for i in range(5):
        gdz_data, file, _ = _gen_gdz(is_elite=False, is_paid=True)
        gdz = _create_gdz(s3, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ для пользователя 3")
        gdz_ids_user3.append(gdz_id)
        # Пользователь 1 покупает и оценивает
        _purchase_gdz(s1, gdz_id)
        _rate_gdz(s1, gdz_id, ratings_user3[i])

    _log("Проверка рейтинга пользователя 3 для доступа к элитным ГДЗ")
    # Проверка рейтинга пользователя 3
    r3 = s3.get("/profile/data")
    if r3.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r3.status_code}")
    actual_rating_user3 = r3.json()["user_rating"]
    expected_rating_user3 = round(sum(ratings_user3) / 5, 2)
    _compare_ratings(actual_rating_user3, expected_rating_user3)
    if actual_rating_user3 <= 4.8:
        _die(ExitStatus.MUMBLE, f"Рейтинг пользователя 3 {actual_rating_user3} недостаточен для доступа к элитным ГДЗ")

    _log("Пользователь 3 проверяет элитное ГДЗ в категории")
    # Пользователь 3 проверяет элитное ГДЗ в категории
    _check_category(s3, category_elite, gdz_elite_id)

    _log("Пользователь 3 получает доступ к элитному ГДЗ")
    # Пользователь 3 получает доступ к элитному ГДЗ
    gdz_elite_full = _get_gdz(s3, gdz_elite_id)
    if gdz_elite_full.status_code != 200 or gdz_elite_full.json()["content_text"] != gdz_data_elite["content_text"]:
        _die(ExitStatus.MUMBLE, "Несоответствие содержимого элитного ГДЗ")

    _log("Создание пользователя 4 с низким рейтингом для проверки запрета доступа и создания элитных ГДЗ")
    # Создание пользователя 4 с низким рейтингом
    s4 = FakeSession(host, PORT)
    user4 = _gen_user()
    _register(s4, user4)
    _login(s4, user4["username"], user4["password"])
    # Создание одного ГДЗ для пользователя 4 и получение низкой оценки
    gdz_data4, file4, _ = _gen_gdz(is_elite=False, is_paid=True)
    gdz4 = _create_gdz(s4, gdz_data4, file4)
    gdz4_id = gdz4.get("id")
    if not gdz4_id:
        _die(ExitStatus.MUMBLE, "Не удалось получить ID ГДЗ для пользователя 4")
    _purchase_gdz(s1, gdz4_id)
    _rate_gdz(s1, gdz4_id, 1)  # Низкая оценка для обеспечения рейтинга < 4.8

    # Проверка рейтинга пользователя 4
    r4 = s4.get("/profile/data")
    if r4.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Неожиданный код /profile/data {r4.status_code}")
    actual_rating_user4 = r4.json()["user_rating"]
    if actual_rating_user4 >= 4.8:
        _die(ExitStatus.MUMBLE, f"Рейтинг пользователя 4 {actual_rating_user4} неожиданно достаточен для доступа к элитным ГДЗ")

    # НОВЫЙ ТЕСТ: Пользователь 4 пытается создать элитное ГДЗ
    _log("Проверка, что пользователь 4 с низким рейтингом не может создать элитное ГДЗ")
    gdz_data_elite_user4, file_elite_user4, _ = _gen_gdz(is_elite=True, is_paid=False)
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

    # Пользователь 4 пытается получить доступ к элитному ГДЗ и должен потерпеть неудачу
    _log("Проверка, что пользователь 4 не может получить доступ к элитному ГДЗ")
    gdz_elite_full = _get_gdz(s4, gdz_elite_id)
    if gdz_elite_full.status_code == 200:
        _die(ExitStatus.MUMBLE, "Пользователь 4 получил доступ к элитному ГДЗ несмотря на низкий рейтинг")

    _die(ExitStatus.OK, "Все проверки пройдены успешно")

def put(host: str, flag: str, vuln: str):
    s = FakeSession(host, PORT)
    
    if vuln == "1":
        # Create new user
        user = _gen_user()
        _register(s, user)
        _login(s, user["username"], user["password"])
        # Create paid GDZ with flag in full_description
        gdz_data, file, _ = _gen_gdz(is_elite=False, is_paid=True)
        gdz_data["full_description"] = flag
        gdz = _create_gdz(s, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.CHECKER_ERROR, "Failed to get GDZ ID for vuln1")
        print(json.dumps({"flag_id": str(gdz_id)}))
        _die(ExitStatus.OK, "Put vuln1 OK")
        print("a")
    elif vuln == "2":
        # Create new user
        user = _gen_user()
        _register(s, user)
        _login(s, user["username"], user["password"])
        # Create draft with flag in content_text
        gdz_data, _, _ = _gen_gdz(is_elite=False, is_paid=True)
        draft_data = {
            "description": gdz_data["description"],
            "full_description": gdz_data["full_description"],
            "category": gdz_data["category"],
            "content_text": flag,
            "price": str(gdz_data["price"]),
            "is_elite": "false",
        }
        draft_response = _save_draft(s, draft_data)
        draft_id = draft_response.get("owner_id")
        if not draft_id:
            _die(ExitStatus.CHECKER_ERROR, "Failed to get draft ID for vuln2")
        print(json.dumps({
            "flag_id": {
                "username": user["username"],
                "password": user["password"],
                "draft_id": str(draft_id)
            }
        }))
        _die(ExitStatus.OK, "Put vuln2 OK")
    
    elif vuln == "3":
        # Login as elite user 1/1
        _login(s, "2", "2")
        # Create elite GDZ with flag in content_text
        gdz_data, file, _ = _gen_gdz(is_elite=True, is_paid=False)
        gdz_data["content_text"] = flag
        gdz = _create_gdz(s, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.CHECKER_ERROR, "Failed to get GDZ ID for vuln3")
        print(json.dumps({"flag_id": str(gdz_id)}))
        _die(ExitStatus.OK, "Put vuln3 OK")
    
    else:
        _die(ExitStatus.CHECKER_ERROR, f"Unknown vuln: {vuln}")

def get(host: str, flag: str, flag_id: str, vuln: str):
    s = FakeSession(host, PORT)
    
    if vuln == "1":
        # Create new user
        user = _gen_user()
        _register(s, user)
        _login(s, user["username"], user["password"])
        # Purchase GDZ with flag_id
        gdz_id = flag_id
        _purchase_gdz(s, gdz_id)
        # Check flag in full_description
        gdz = _get_gdz(s, gdz_id)
        if gdz.status_code != 200:
            _die(ExitStatus.CORRUPT, f"Failed to get GDZ {gdz_id}")
        if gdz.json().get("full_description") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln1")
        _die(ExitStatus.OK, "Get vuln1 OK")
    
    elif vuln == "2":
        # Parse flag_id
        try:
            flag_id_data = json.loads(flag_id)
            username = flag_id_data["username"]
            password = flag_id_data["password"]
            draft_id = flag_id_data["draft_id"]
        except Exception as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln2: {e}")
        # Login as user
        _login(s, username, password)
        # Get draft
        draft = _get_draft(s)
        if draft.get("id") != draft_id or draft.get("content_text") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln2")
        _die(ExitStatus.OK, "Get vuln2 OK")
    
    elif vuln == "3":
        # Login as elite user 2/2
        _login(s, "1", "1")
        # Get GDZ with flag_id
        gdz_id = flag_id
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
            flag = argv[3]
            vuln = argv[4]
            put(hostname, flag, vuln)
        elif cmd == "get":
            flag = argv[3]
            flag_id = argv[4]
            vuln = argv[5]
            get(hostname, flag, flag_id, vuln)
        else:
            raise IndexError
    except IndexError:
        _die(
            ExitStatus.CHECKER_ERROR,
            f"Usage: {argv[0]} [check|put|get] IP [flag flag_id vuln]",
        )

if __name__ == "__main__":
    _main()