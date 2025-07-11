#!/usr/bin/env python3

from UserClass import User

import inspect
import os
import random
import string
import sys
import time
import random
import pickle
from enum import Enum
from sys import argv
import requests
import json
from cryptohash import sha1
from datetime import datetime
from dynamic_generation import dynamic_generate
from static_generation import static_generate

random = random.SystemRandom()

""" <config> """
PORT = 8000
HOST = "localhost"
EXPLOIT_NAME = argv[0]

DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)
""" </config> """

start_time = time.time()


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
            print(
                "[TRACE] {method} {url} {r.status_code}".format(
                    method=method, url=url, r=r.status_code
                )
            )
        return r


def _gen_user():
    try:
        user = User.generate()
        return {
            "realname": user.realname,
            "username": user.username,
            "password": user.password,
        }
    except FileNotFoundError as e:
        _die(ExitStatus.CHECKER_ERROR, f"Failed to generate user: missing file {e}")
    except Exception as e:
        _die(ExitStatus.MUMBLE, f"Failed to generate user: {e}")


CATEGORIES = [
    "Университетские задачи_Мат.анализ",
    "Лабораторные работы_Модели безопасности",
    "Лабораторные работы_Компьютерные сети",
    "Лабораторные работы_ТЧМК",
    "Лабораторные работы_АИСД",
    "Школьные задачи_Алгебра",
    "Школьные задачи_Геометрия",
    "Школьные задачи_Физика",
    "Школьные задачи_Информатика",
    "Университетские задачи_Экономика",
    "Университетские задачи_КМЗИ",
    "Университетские задачи_Мат.статистика",
    "Университетские задачи_Теория вероятностей",
    "Университетские задачи_Алгебра",
    "Мемология_Уроки Французского",
    "Мемология_Джаваскриптолюбие",
    "Мемология_Инглиш мафака",
    "Мемология_Царица наук"
]


def _gen_gdz(is_elite=False, is_paid=False):
    category = random.choice(CATEGORIES)
    price = 0
    if is_paid and not is_elite:
        price = random.randint(50, 100)

    use_static = random.choice([True, False])

    if (
            (use_static or category == "Мемология_Инглиш мафака")
            and category != "Мемология_Уроки Французского"
            and category != "Мемология_Царица наук"
            and category != "Мемология_Джаваскриптолюбие"
    ):
        gdz = static_generate(category)
        file_path = gdz["content"]
        gdz_data = {
            "description": gdz["description"],
            "full_description": gdz["full_description"],
            "category": category,
            "content_text": gdz["content_text"],
            "price": price,
            "is_elite": is_elite,
        }
        return gdz_data, file_path, category
    else:
        gdz = dynamic_generate(category)
        gdz_data = {
            "description": gdz["description"],
            "full_description": gdz["full_description"],
            "category": category,
            "content_text": gdz["content_text"],
            "price": price,
            "is_elite": is_elite,
        }
        return gdz_data, gdz["content"], category


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
        _die(ExitStatus.CORRUPT, f"No token in /token response")
    s.headers.update({"Authorization": f"Bearer {token}"})
    return token


def _create_gdz(s, gdz_data, file_path):
    try:
        files = {"gdz_str": (None, json.dumps(gdz_data))}

        if file_path is not None:
            try:
                with open(file_path, "rb") as f:
                    file_content = f.read()
                files["content_file"] = ("solution.png", file_content, "image/png")
            except FileNotFoundError as e:
                _die(ExitStatus.CHECKER_ERROR, f"File not found: {file_path}")

        r = s.post("/gdz/create", files=files)
    except Exception as e:
        _die(ExitStatus.MUMBLE, f"Failed to create GDZ: {e}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/create code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/create code {r.status_code}")
    return r.json()


def _get_gdz(s, gdz_id):
    try:
        r = s.get(f"/gdz/{gdz_id}/full")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to get GDZ: {e}")
    if r.status_code == 403:
        _die(ExitStatus.MUMBLE, f"Unexpected status code {r.status_code}")
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"GDZ not found {r.status_code}")
    return r


def _free_purchase_gdz(s, gdz_id):
    try:
        r = s.post(f"/gdz/{gdz_id}/free-purchase")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to free purchase GDZ: {e}")
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"GDZ not found {r.status_code}")
    if r.status_code == 400:
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/{gdz_id}/purchase code {r.status_code}")
    return r.json()


def _purchase_gdz(s, gdz_id):
    try:
        r = s.post(f"/gdz/{gdz_id}/purchase")
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to purchase GDZ: {e}")
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"GDZ not found {r.status_code}")
    if r.status_code == 400:
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/{gdz_id}/purchase code {r.status_code}")

    confirmation_code = r.json().get("confirmation_code")
    if not confirmation_code:
        _die(ExitStatus.CORRUPT, f"No confirmation code in purchase response")

    n = 160301046244593794374726426877457303604019537423736458260136643925405546154653037172463089669436445456557499425029994701102494179131569495553118775092473011745647436677950345054183103280168169605050154349614937369702539109115434630721210013794356412532578527347021846882486616784364644818143571566741240343519
    d = 106867364163062529583150951251638202402679691615824305506757762616937030769768691448308726446290963637704999616686663134068329452754379663702079183394981990945329295012055489191325887232050991358371457973464894055499039990700519040610630249324976268648754088450636207724270010117036618338292116885343831669547

    h = bytes.fromhex(sha1(confirmation_code))
    padding = b"\x00\x01" + b"\xff" * 105 + b"\x00" + h
    # Преобразуем блок в число
    m = int.from_bytes(padding, "big")
    signature = pow(m, d, n)

    try:
        r = s.post(f"/gdz/{gdz_id}/confirm-purchase", json={"value": signature})
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to confirm purchase: {e}")
    if r.status_code != 201:
        _log(
            f"Unexpected /gdz/{gdz_id}/confirm-purchase code {r.status_code} with body {r.text}"
        )
        _die(
            ExitStatus.MUMBLE,
            f"Unexpected /gdz/{gdz_id}/confirm-purchase code {r.status_code}",
        )
    return r.json()


def _rate_gdz(s, gdz_id, value):
    try:
        r = s.post("/gdz/rate", json={"gdz_id": gdz_id, "value": value})
    except Exception as e:
        _die(ExitStatus.DOWN, f"Failed to rate GDZ: {e}")
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"GDZ not found {r.status_code}")
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
        _log(
            f"Unexpected /gdz_category/{category} code {r.status_code} with body {r.text}"
        )
        _die(
            ExitStatus.MUMBLE,
            f"Unexpected /gdz_category/{category} code {r.status_code}",
        )
    gdz_list = r.json()
    if not any(g["id"] == gdz_id for g in gdz_list):
        _die(ExitStatus.CORRUPT, f"GDZ {gdz_id} not found in category {category}")
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
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"User not found {r.status_code}")
    if r.status_code != 200:
        _log(f"Unexpected /gdz/get_draft code {r.status_code} with body {r.text}")
        _die(ExitStatus.MUMBLE, f"Unexpected /gdz/get_draft code {r.status_code}")
    return r.json()


def _compare_ratings(actual, expected):
    if abs(actual - expected) > 0.01:
        _die(
            ExitStatus.MUMBLE,
            f"User rating mismatch: expected {expected}, got {actual}",
        )


def _boost_user_rating(s_owner: FakeSession, user_owner: dict, s_rater: FakeSession):
    gdz_ids = []
    for _ in range(5):
        gdz_data, file, _ = _gen_gdz(is_elite=False, is_paid=True)
        gdz = _create_gdz(s_owner, gdz_data, file)
        gdz_id = gdz.get("id")
        if not gdz_id:
            _die(ExitStatus.CORRUPT, "Can't get user ID for boosting rating")
        gdz_ids.append(gdz_id)
        _purchase_gdz(s_rater, gdz_id)
        _rate_gdz(s_rater, gdz_id, 5)
        time.sleep(0.1)
    r = s_owner.get("/profile/data")
    if r.status_code == 404:
        _die(ExitStatus.CORRUPT, f"User not found {r.status_code}")
    if r.status_code != 200:
        _die(ExitStatus.MUMBLE, f"Unexpected code /profile/data: {r.status_code}")
    rating = r.json().get("user_rating")
    if rating <= 4.8:
        _die(
            ExitStatus.MUMBLE,
            f"User rating = {rating} not enough after boosting",
        )
    _log(f"Boosted up to {rating} it's okey")
    return rating


def check(host: str):
    s1 = FakeSession(host, PORT)
    s2 = FakeSession(host, PORT)
    s3 = FakeSession(host, PORT)
    s4 = FakeSession(host, PORT)

    user1 = None
    user2 = None

    while user1 == None or user2 == None:
        user1 = _gen_user()
        user2 = _gen_user()
        _log("check: trying to gen user1, user2")

    _log("Registration of user1, user2:")
    _register(s1, user1)
    _register(s2, user2)
    _log("Login user1, user2:")
    _login(s1, user1["username"], user1["password"])
    _login(s2, user2["username"], user2["password"])

    _log("Creating first GDZ")
    gdz_data1, file1, category1 = _gen_gdz(is_elite=False, is_paid=False)
    gdz_data2, file2, category2 = _gen_gdz(is_elite=False, is_paid=True)
    _log("Creating finished")
    gdz1 = _create_gdz(s1, gdz_data1, file1)
    gdz2 = _create_gdz(s2, gdz_data2, file2)
    gdz1_id = gdz1.get("id")
    gdz2_id = gdz2.get("id")
    if not gdz1_id or not gdz2_id:
        _die(ExitStatus.CORRUPT, "Can't get GDZ id")

    _log("Checking GDZ in user profile...")
    r1 = s1.get("/profile/data")
    r2 = s2.get("/profile/data")
    if r1.status_code == 404 or r2.status_code == 404:
        _die(ExitStatus.CORRUPT, f"User not found {r1.status_code} или {r2.status_code}")
    if r1.status_code != 200 or r2.status_code != 200:
        _die(
            ExitStatus.MUMBLE,
            f"Unexpected code /profile/data {r1.status_code} или {r2.status_code}",
        )
    profile1 = r1.json()
    profile2 = r2.json()
    if not any(g["id"] == gdz1_id for g in profile1["gdz_list"]) or not any(
            g["id"] == gdz2_id for g in profile2["gdz_list"]
    ):
        _die(ExitStatus.CORRUPT, "Can't find GDZ in users profile")

    _log("Checking categoty for GDZ of user2...")
    _check_category(s1, category2, gdz2_id)

    _log(
        "user1 trying to buy user2's GDZ. user2 trying to free open user1's GDZ..."
    )
    _purchase_gdz(s1, gdz2_id)

    _log(
        "Checking access to purchase GDZ..."
    )
    gdz1_full = _get_gdz(s2, gdz1_id)
    if gdz1_full.json()["content_text"] != gdz_data1["content_text"]:
        _die(ExitStatus.CORRUPT, "GDZ data mismatch")
    if gdz1_full.status_code != 200:
        _die(
            ExitStatus.MUMBLE,
            "Found differences between contents of purchased GDZ 1 from s2",
        )

    gdz2_full = _get_gdz(s1, gdz2_id)
    if gdz2_full.json()["content_text"] != gdz_data2["content_text"]:
        _die(ExitStatus.CORRUPT, "GDZ data mismatch")
    if gdz2_full.status_code != 200:
        _die(
            ExitStatus.MUMBLE,
            "Found differences between contents of purchased GDZ 2 from s1",
        )

    _log("Creating and checking draft...")
    category_part2, subject_part2 = category2.split("_", 1)
    draft_data2 = {
        "description": gdz_data2["description"],
        "full_description": gdz_data2["full_description"],
        "category": category_part2,
        "subject": subject_part2,
        "content_text": gdz_data2["content_text"],
        "price": gdz_data2["price"],
        "is_elite": gdz_data2["is_elite"],
    }
    _log(f"draft_data {draft_data2}")
    _save_draft(s2, draft_data2)
    draft2 = _get_draft(s2)
    if not draft2 or "content_text" not in draft2:
        _die(ExitStatus.CORRUPT, "No draft or content_text found for user2")
    for key, value in draft_data2.items():
        if draft2.get(key) != value:
            _die(
                ExitStatus.CORRUPT,
                f"Draft field {key} mismatch for user2: expected {value}, got {draft2.get(key)}",
            )

    _die(ExitStatus.OK, "ALL CHECKS PASSED SUCCESSFULLY")


def put(host: str, flag_id: str, flag: str, vuln: int):
    s = FakeSession(host, PORT)

    if vuln == 1:
        try:
            user = None
            while user is None:
                user = _gen_user()

            _register(s, user)
            _login(s, user["username"], user["password"])

            gdz_data, file, _ = _gen_gdz(is_elite=False, is_paid=True)
            gdz_data["full_description"] = flag
            gdz = _create_gdz(s, gdz_data, file)
            gdz_id = gdz.get("id")
            if not gdz_id:
                _die(ExitStatus.CORRUPT, "Failed to get GDZ ID for vuln3")
            jd = json.dumps(
                {
                    "username": user["username"],
                    "password": user["password"],
                    "gdz_id": str(gdz_id),
                }
            )
            print(jd, flush=True)
            _die(ExitStatus.OK, f"{jd}")
        except Exception as e:
            _log("Failed to put flag in vuln3")
            _die(ExitStatus.MUMBLE, f"Failed to put flag: {e}")

    elif vuln == 2:
        try:
            user = None
            while user is None:
                user = _gen_user()

            _register(s, user)
            _login(s, user["username"], user["password"])

            gdz_data, _, category = _gen_gdz(is_elite=False, is_paid=True)
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
            draft_response = _save_draft(s, draft_data)
            if draft_response.get("status") != "success":
                _die(ExitStatus.MUMBLE, "Failed to save draft for vuln2")
            jd = json.dumps({"username": user["username"], "password": user["password"]})
            print(jd, flush=True)
            _die(ExitStatus.OK, f"{jd}")
        except Exception as e:
            _log("Failed to put flag in vuln2")
            _die(ExitStatus.MUMBLE, f"Failed to put flag: {e}")

    elif vuln == 3:
        try:
            user_elite = _gen_user()
            _register(s, user_elite)
            _login(s, user_elite["username"], user_elite["password"])
            s_rater = FakeSession(host, PORT)
            user_rater = _gen_user()
            _register(s_rater, user_rater)
            _login(s_rater, user_rater["username"], user_rater["password"])
            _boost_user_rating(s, user_elite, s_rater)

            gdz_data, file, _ = _gen_gdz(is_elite=True, is_paid=False)
            gdz_data["description"] = flag
            gdz = _create_gdz(s, gdz_data, file)
            gdz_id = gdz.get("id")
            if not gdz_id:
                _die(ExitStatus.CORRUPT, "Failed to get GDZ ID for vuln1")
            jd = json.dumps(
                {
                    "username": user_elite["username"],
                    "password": user_elite["password"],
                    "gdz_id": str(gdz_id)
                }
            )
            print(jd, flush=True)
            _die(ExitStatus.OK, f"{jd}")
        except Exception as e:
            _log("Failed to put flag in vuln1")
            _die(ExitStatus.MUMBLE, f"Failed to put flag: {e}")

    else:
        _die(ExitStatus.CHECKER_ERROR, f"Unknown vuln: {vuln}")


def get(host: str, flag_id: str, flag: str, vuln: int):
    s = FakeSession(host, PORT)

    _log(f"Received flag_id: {flag_id}")
    flag_id_data = json.loads(flag_id)
    _log(f"data in get: {flag_id_data}")
    if not flag_id_data:
        _die(ExitStatus.CHECKER_ERROR, "ERROR json.loads")

    if vuln == 1:
        try:
            username = flag_id_data["username"]
            password = flag_id_data["password"]
            gdz_id = str(flag_id_data["gdz_id"])

        except (TypeError, KeyError, ValueError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln1: {e}")
        _login(s, username, password)
        gdz = _get_gdz(s, gdz_id)
        if gdz.json().get("full_description") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln1")
        _die(ExitStatus.OK, "Get vuln1 OK")

    elif vuln == 2:
        try:
            username = flag_id_data["username"]
            password = flag_id_data["password"]
        except (TypeError, KeyError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln2: {e}")
        _login(s, username, password)
        draft = _get_draft(s)
        if not draft or "content_text" not in draft:
            _die(ExitStatus.CORRUPT, "No draft or content_text found for vuln2")
        if draft["content_text"] != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln2")
        _die(ExitStatus.OK, "Get vuln2 OK")

    elif vuln == 3:
        try:
            username = flag_id_data["username"]
            password = flag_id_data["password"]
            gdz_id = str(flag_id_data["gdz_id"])
        except (TypeError, KeyError, ValueError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln3: {e}")
        _login(s, username, password)

        try:
            username = flag_id_data["username"]
            password = flag_id_data["password"]
            gdz_id = str(flag_id_data["gdz_id"])
        except (TypeError, KeyError, ValueError) as e:
            _die(ExitStatus.CHECKER_ERROR, f"Invalid flag_id for vuln3: {e}")

        s_elite = FakeSession(host, PORT)
        user_elite = _gen_user()
        _register(s_elite, user_elite)
        _login(s_elite, user_elite["username"], user_elite["password"])
        s_rater = FakeSession(host, PORT)
        user_rater = _gen_user()
        _register(s_rater, user_rater)
        _login(s_rater, user_rater["username"], user_rater["password"])
        _boost_user_rating(s_elite, user_elite, s_rater)
        gdz_data, file, category = _gen_gdz(is_elite=True, is_paid=False)
        gdz1 = _create_gdz(s_elite, gdz_data, file)
        gdz_id_elite = gdz1.get("id")
        gdz1 = _get_gdz(s, gdz_id_elite)
        if gdz1.status_code != 200:
            _die(ExitStatus.CORRUPT, f"Failed to get GDZ {gdz_id}")

        _login(s, username, password)
        gdz = _get_gdz(s, gdz_id)
        if gdz.json().get("description") != flag:
            _die(ExitStatus.CORRUPT, "Flag mismatch for vuln3")
        _die(ExitStatus.OK, "Get vuln3 OK")



    else:
        _die(ExitStatus.CHECKER_ERROR, f"Unknown vuln: {vuln}")


def _log(obj):
    if DEBUG and obj:
        # elapsed_time = time.time() - start_time
        caller = inspect.stack()[1].function
        print(f"[{caller}] {obj}", file=sys.stderr)
    return obj


def info():
    print("vulns: 2:2:1", flush=True, end="")
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
        if cmd == "info":
            info()
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