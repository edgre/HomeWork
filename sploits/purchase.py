import requests
import uuid
import json
import math
import re

# Базовый URL сервера
BASE_URL = "http://localhost:8000"


def register_user(username: str, password: str, realname: str = None):
    """Регистрирует нового пользователя."""
    url = f"{BASE_URL}/register"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": username,
        "password": password,
    }
    if realname:
        data["realname"] = realname

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Регистрация успешна:", response.json())
        return response.json()  # Возвращает токен доступа
    except requests.exceptions.HTTPError as e:
        print("Ошибка при регистрации:", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print("Ошибка запроса при регистрации:", str(e))
        return None


def login_user(username: str, password: str):
    """Выполняет вход для пользователя."""
    url = f"{BASE_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        print("Вход успешен:", response.json())
        return response.json()  # Возвращает токен доступа
    except requests.exceptions.HTTPError as e:
        print("Ошибка при входе:", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print("Ошибка запроса при входе:", str(e))
        return None


def get_categories():
    """Получает список категорий."""
    url = f"{BASE_URL}/category"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        categories = response.json()
        return categories
    except requests.exceptions.HTTPError as e:
        print("Ошибка при получении категорий:", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print("Ошибка запроса при получении категорий:", str(e))
        return None


def get_subjects_by_category(category: str):
    """Получает список предметов для заданной категории."""
    url = f"{BASE_URL}/subjects/{category}"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        subjects = response.json()
        return subjects
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при получении предметов для категории '{category}':", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса для предметов категории '{category}':", str(e))
        return None


def get_all_paid_gdz(token: str):
    """Получает список платных ГДЗ по всем комбинациям category_subject."""
    categories = get_categories()
    if not categories:
        print("Не удалось получить категории для запроса ГДЗ")
        return None

    all_gdz = []
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    for category in categories:
        subjects = get_subjects_by_category(category)
        if not subjects:
            continue

        for subject in subjects:
            combined_category = f"{category}_{subject}"
            url = f"{BASE_URL}/gdz_category/{combined_category}"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                gdz_list = [x for x in response.json() if x["price"] > 0]
                all_gdz.extend(gdz_list)
            except requests.exceptions.HTTPError as e:
                print(f"Ошибка получения ГДЗ для '{combined_category}':", e.response.status_code, e.response.text)
                continue
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса для ГДЗ '{combined_category}':", str(e))
            continue

    return all_gdz


def purchase_gdz(token: str, gdz_id: int):
    """Запрашивает код подтверждения покупки ГДЗ."""
    url = f"{BASE_URL}/gdz/{gdz_id}/purchase"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"Код подтверждения для ГДЗ {gdz_id}:", response.json())
        return response.json().get("confirmation_code")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при запросе покупки ГДЗ {gdz_id}:", e.response.status_code, e.response.text)
        return None


def confirm_purchase(token: str, gdz_id: int, confirmation: float):
    """Подтверждает покупку ГДЗ, отправляя корень пятой степени кода."""
    url = f"{BASE_URL}/gdz/{gdz_id}/confirm-purchase"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "value": confirmation
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Покупка ГДЗ {gdz_id} подтверждена:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при подтверждении покупки ГДЗ {gdz_id}:", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса для подтверждения покупки ГДЗ {gdz_id}:", str(e))
        return None


def get_gdz_full(token: str, gdz_id: int):
    """Получает полные данные ГДЗ."""
    url = f"{BASE_URL}/gdz/{gdz_id}/full"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при получении ГДЗ {gdz_id}:", e.response.status_code, e.response.text)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса для ГДЗ {gdz_id}:", str(e))
        return None


def main():
    # Генерируем уникальный username
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    password = "securepassword123"
    realname = "Test User"

    # Регистрация пользователя
    print(f"Регистрация пользователя: {unique_username}")
    register_response = register_user(unique_username, password, realname)
    if not register_response:
        print("Не удалось зарегистрировать пользователя")
        return

    # Вход пользователя
    print(f"\nВход пользователя: {unique_username}")
    login_response = login_user(unique_username, password)
    if not login_response:
        print("Не удалось войти")
        return

    # Получение токена
    access_token = login_response.get("access_token")
    if not access_token:
        print("Токен доступа не получен")
        return
    print(f"Получен токен доступа: {access_token}")

    # Получение всех платных ГДЗ
    print("\nПолучение всех платных ГДЗ")
    all_gdz = get_all_paid_gdz(access_token)
    if all_gdz is None:
        print("Не удалось получить ГДЗ")
        return
    elif not all_gdz:
        print("Платные ГДЗ не найдены")
        return

    print(f"Найдено платных ГДЗ: {len(all_gdz)}")

    # Покупка и получение full_description для каждого ГДЗ
    purchased_gdz = []
    # Регулярное выражение для проверки content_text
    pattern = re.compile(r'TEAM[0-9]{3}_[A-Z0-9]{32}')

    for gdz in all_gdz:
        gdz_id = gdz["id"]
        print(f"\nОбработка ГДЗ: ID={gdz_id}, Описание={gdz['description']}")

        # Запрос кода покупки
        confirmation_code = purchase_gdz(access_token, gdz_id)
        if not confirmation_code:
            print(f"Пропуск ГДЗ {gdz_id}: не удалось получить код подтверждения")
            continue

        # Вычисление корня пятой степени
        try:
            code_float = float(confirmation_code)
            fifth_root = round(math.pow(code_float, 1 / 5))
            print(f"Корень пятой степени из кода {confirmation_code}: {fifth_root}")
        except ValueError:
            print(f"Пропуск ГДЗ {gdz_id}: код {confirmation_code} не является числом")
            continue

        # Подтверждение покупки
        confirm_response = confirm_purchase(access_token, gdz_id, fifth_root)
        if not confirm_response:
            print(f"Пропуск ГДЗ {gdz_id}: не удалось подтвердить покупку")
            continue

        # Получение полного текста ГДЗ
        gdz_full = get_gdz_full(access_token, gdz_id)
        if gdz_full:
            full_description = gdz_full.get('full_description', 'Полное описание отсутствует')
            content_text = gdz_full.get('content_text', '')
            print(f"Полное описание ГДЗ {gdz_id}: {full_description}")

            # Проверка content_text на соответствие регулярному выражению
            if pattern.match(content_text):
                purchased_gdz.append({
                    "id": gdz_id,
                    "content_text": content_text,
                })
                print(f"ГДЗ {gdz_id} добавлено в результат: content_text соответствует шаблону")
            else:
                print(f"ГДЗ {gdz_id} пропущено: content_text не соответствует шаблону")
        else:
            print(f"Пропуск ГДЗ {gdz_id}: не удалось получить полные данные")

    # Итоговый вывод
    print("\nИтоговый список купленных ГДЗ:")
    if purchased_gdz:
        for gdz in purchased_gdz:
            print(f"ID: {gdz['id']}, Ответ: {gdz['content_text']}")
    else:
        print("Ни одно ГДЗ не было успешно куплено или не соответствует шаблону")


if __name__ == "__main__":
    main()