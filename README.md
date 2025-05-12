# Про Frontend

## Перед запуском

1. Установить Node.js
   1. Проверить: `node -v`
2. Установить пакетный менеджер npm
   1. Проверить: `npm -v`
3. Создание проекта `npm create vite@latest app`
   1. Выбираем фреймворк React
   2. Выбираем вариант JavaScript
   3. Переходим в папку проекта `cd app`
   4. Установка зависимостей `npm install`
4. Добавляем React Router `npm install react-router-dom`

## Запустить dev-сервер

> `npm run dev` (в папке frontend/app)

# Про Backend

1. Установить необходимые зависимости
   1. Выполнить: `pip install -r requirements.txt`

## Запустить Uvicorn-сервер

> Из директории backend выполнить
>
> 1. `pip install uvicorn fastapi`
> 2. `pip install python-multipart`
> 3. Запуск: `uvicorn main:app --reload`
