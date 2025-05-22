import requests
import json
from requests_toolbelt import MultipartEncoder

# 1. Получение токена
response1 = requests.post(
    "http://localhost:8000/token",
    data={"username": "1", "password": "1"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
token = response1.json()["access_token"]

print(token)

# # 2. Подготовка данных
# gdz_payload= {
#     "description": "Решение задач по математике",
#     "full_description": "Упражнение 1",
#     "price": 100,
#     "category": "Школа_Физика",
#     "content_text": "цветочек"
# }
#
#
# response = requests.post(
#     "http://localhost:8000/gdz/create",
#     files={
#         "content_file": open("solution.png", "rb"),
#     },
#     data={
#         "gdz_str": json.dumps(gdz_payload, ensure_ascii=False)
#     },
#     headers={
#         "Authorization": f"Bearer {token}",
#     }
# )
#
# print(f"Status Code: {response.status_code}")
# print(response.json())

response3 = requests.get(
    "http://localhost:8000/images/036265f4-3f8f-4471-897a-fdbbcdd4a2b4.png",
)
print(response3)