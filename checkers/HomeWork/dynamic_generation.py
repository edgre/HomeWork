import random
import math
from math import pi,sqrt,  gcd, log2
from sympy import symbols, diff, integrate, mod_inverse
import os
import sys
import re

# Базы данных для генерации учебников
PROBABILITY_BOOKS = [
    ("Теория вероятностей и математическая статистика", "Гмурман В.Е."),
    ("Вероятность и статистика", "Ширяев А.Н."),
    ("Теория вероятностей", "Боровков А.А.")
]

STATISTICS_BOOKS = [
    ("Математическая статистика", "Кремер Н.Ш."),
    ("Статистика для всех", "Спирин П.А."),
    ("Теория вероятностей и статистика", "Тюрин Ю.Н.")
]

ECONOMICS_BOOKS = [
    ("Экономическая теория", "Нуреев Р.М."),
    ("Микроэкономика", "Пиндайк Р."),
    ("Экономика", "Самуэльсон П.")
]

ALGEBRA_BOOKS = [
    ("Алгебра и начала анализа", "Колмогоров А.Н."),
    ("Высшая алгебра", "Курош А.Г."),
    ("Линейная алгебра", "Ильин В.А.")
]

CALCULUS_BOOKS = [
    ("Математический анализ", "Фихтенгольц Г.М."),
    ("Курс дифференциального и интегрального исчисления", "Зорич В.А."),
    ("Основы математического анализа", "Ильин В.А.")
]

SCHOOL_ALGEBRA_BOOKS = [
    ("Алгебра", "Иванов А.П."),
    ("Алгебра", "Петрова В.М."),
    ("Алгебра", "Сидоров Г.К.")
]

SCHOOL_GEOMETRY_BOOKS = [
    ("Геометрия", "Атанасян Л.С."),
    ("Геометрия", "Погорелов А.В."),
    ("Геометрия", "Бутузов В.Ф.")
]

SCHOOL_INFORMATICS_BOOKS = [
    ("Информатика", "Гейн А.Г."),
    ("Информатика", "Семакин И.Г."),
    ("Информатика", "Угринович Н.Д.")
]

SCHOOL_PHYSICS_BOOKS = [
    ("Физика", "Ломоносов М.В."),
    ("Физика", "Эйнштейн А.И."),
    ("Физика", "Ландау Л.Д.")
]

CRYPTO_BOOKS = [
    ("Криптографические методы защиты информации", "Шнайер Б."),
    ("Криптография", "Менезис А."),
    ("Основы криптографии", "Ростовцев А.Г.")
]

PROGRAMMING_BOOKS = [
    ("Алгоритмы и структуры данных", "Кормен Т."),
    ("Программирование на Python", "Лутц М."),
    ("Введение в программирование", "Седжвик Р.")
]

SECURITY_MODELS_BOOKS = [
    ("Модели безопасности компьютерных систем", "Галатенко В.А."),
    ("Основы информационной безопасности", "Погонышева Д.А."),
    ("Теория и практика построения защищенных систем", "Шаньгин В.Ф."),
    ("Computer Security: Art and Science", "Matt Bishop"),
    ("Security Engineering", "Ross Anderson")
]

NETWORK_SECURITY_BOOKS = [
    ("Компьютерные сети. Принципы, технологии, протоколы", "Олифер В.Г."),
    ("Современные компьютерные сети", "Палмер М."),
    ("Компьютерные сети и информационная безопасность", "Пярин В.А."),
    ("Computer Networking: A Top-Down Approach", "Kurose, Ross"),
    ("Network Security Essentials", "William Stallings")
]


def generate_book(book_list):
    title, author = random.choice(book_list)
    year = random.randint(2000, 2023)
    publisher = random.choice(["Просвещение", "Физматлит", "Высшая школа", "Лань", "Дрофа", "БИНОМ"])
    return f"{title} {author} {publisher}, {year}"


def generate_school_algebra_task():
    GRADES = {
        7: ["линейные уравнения", "разложение на множители", "проценты"],
        8: ["квадратные уравнения", "алгебраические дроби", "графики функций"],
        9: ["системы уравнений", "геометрическая прогрессия", "неравенства"]
    }

    grade = random.choice(list(GRADES.keys()))
    topic = random.choice(GRADES[grade])
    book = generate_book(SCHOOL_ALGEBRA_BOOKS)

    if grade == 7:
        if topic == "линейные уравнения":
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            c = random.randint(1, 30)
            exercise = f"Решите уравнение: {a}x + {b} = {c}"
            answer = f"x = ({c} - {b}) / {a} = {(c - b) / a:.1f}"

        elif topic == "разложение на множители":
            a = random.randint(2, 5)
            b = random.randint(2, 5)
            exercise = f"Разложите на множители: {a * a}x²y - {a * b}xy²"
            answer = f"{a}xy({a}x - {b}y)"

        elif topic == "проценты":
            price = random.randint(100, 2000)
            discount = random.randint(5, 30)
            exercise = f"Цена товара {price} руб. снизилась на {discount}%. Какова новая цена?"
            answer = f"{price} * 0.{100 - discount} = {price * (100 - discount) / 100:.1f} руб."

    elif grade == 8:
        if topic == "квадратные уравнения":
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-15, 15)
            exercise = f"Решите уравнение: {a}x² + {b}x + {c} = 0"
            D = b ** 2 - 4 * a * c
            if D > 0:
                x1 = (-b + sqrt(D)) / (2 * a)
                x2 = (-b - sqrt(D)) / (2 * a)
                answer = f"D = {D}, x₁ = {x1:.1f}, x₂ = {x2:.1f}"
            else:
                answer = f"D = {D} (нет действительных корней)"

        elif topic == "алгебраические дроби":
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            exercise = f"Упростите дробь: (x² - {a * a})/(x² + {2 * a}x + {a * a})"
            answer = f"(x - {a})(x + {a})/(x + {a})² = (x - {a})/(x + {a})"

        elif topic == "графики функций":
            k = random.randint(-3, 3)
            b = random.randint(-5, 5)
            exercise = f"Постройте график функции y = {k}x + {b}. Найдите точку пересечения с осью OY."
            answer = f"При x = 0: y = {b}. Точка: (0, {b})"

    elif grade == 9:
        if topic == "системы уравнений":
            a1, b1 = random.randint(1, 5), random.randint(1, 5)
            a2, b2 = random.randint(1, 5), random.randint(1, 5)
            c1, c2 = random.randint(5, 15), random.randint(5, 15)
            det = a1 * b2 - a2 * b1
            while det == 0:  # Повторяем выбор, пока det != 0
                a1, b1 = random.randint(1, 5), random.randint(1, 5)
                a2, b2 = random.randint(1, 5), random.randint(1, 5)
                det = a1 * b2 - a2 * b1
            det_x = c1 * b2 - c2 * b1
            det_y = a1 * c2 - a2 * c1
            exercise = f"Решите систему:\n{{\n  {a1}x + {b1}y = {c1}\n  {a2}x + {b2}y = {c2}\n}}"
            answer = f"Δ = {det}, Δx = {det_x}, Δy = {det_y}\nx = {det_x / det:.1f}, y = {det_y / det:.1f}"

        elif topic == "геометрическая прогрессия":
            b1 = random.randint(1, 5)
            q = random.randint(2, 4)
            n = random.randint(3, 6)
            exercise = f"Найдите сумму первых {n} членов прогрессии, где b₁ = {b1}, q = {q}"
            answer = f"S_{n} = {b1}*({q}^{n}-1)/({q}-1) = {b1 * (q ** n - 1) / (q - 1)}"

        elif topic == "неравенства":
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            exercise = f"Решите неравенство: {a}x² + {b}x + {c} > 0"
            D = b ** 2 - 4 * a * c
            if D > 0:
                x1 = (-b + sqrt(D)) / (2 * a)
                x2 = (-b - sqrt(D)) / (2 * a)
                answer = f"D = {D}. Парабола ветвями {'вверх' if a > 0 else 'вниз'}. Решение: x ∈ ({min(x1, x2):.1f}; {max(x1, x2):.1f})"
            else:
                answer = f"D = {D}. Решение: {'все x' if a > 0 else 'нет решений'}"

    return book, exercise, answer, None


def generate_school_geometry_task():
    GRADES = {
        7: ["треугольники", "углы", "начальные геометрические сведения"],
        8: ["четырёхугольники", "окружность", "подобные треугольники"],
        9: ["векторы", "метод координат", "соотношения в треугольнике"]
    }

    grade = random.choice(list(GRADES.keys()))
    topic = random.choice(GRADES[grade])
    book = generate_book(SCHOOL_GEOMETRY_BOOKS)

    if grade == 7:
        if topic == "треугольники":
            a, b, c = sorted([random.randint(3, 10) for _ in range(3)])
            while a + b <= c:
                a, b, c = sorted([random.randint(3, 10) for _ in range(3)])
            exercise = f"Стороны треугольника равны {a}, {b} и {c}. Найдите периметр."
            answer = f"P = a + b + c = {a} + {b} + {c} = {a + b + c}"

        elif topic == "углы":
            angle1 = random.randint(20, 70)
            angle2 = random.randint(20, 70)
            exercise = f"Два угла треугольника равны {angle1}° и {angle2}°. Найдите третий угол."
            answer = f"180° - {angle1}° - {angle2}° = {180 - angle1 - angle2}°"

        elif topic == "начальные геометрические сведения":
            segments = [random.randint(1, 10) for _ in range(2)]
            exercise = f"Длина первого отрезка {segments[0]} см, второго - {segments[1]} см. На сколько один длиннее другого?"
            answer = f"|{segments[0]} - {segments[1]}| = {abs(segments[0] - segments[1])} см"

    elif grade == 8:
        if topic == "четырёхугольники":
            side = random.randint(5, 15)
            exercise = f"Найдите площадь квадрата со стороной {side} см."
            answer = f"S = a² = {side}² = {side ** 2} см²"

        elif topic == "окружность":
            r = random.randint(1, 10)
            exercise = f"Радиус окружности равен {r} см. Найдите длину окружности (π≈3.14)."
            answer = f"C = 2πr = 2*3.14*{r} ≈ {2 * 3.14 * r:.1f} см"

        elif topic == "подобные треугольники":
            k = random.choice([2, 3, 4])
            p1 = random.randint(10, 20)
            exercise = f"Коэффициент подобия треугольников равен {k}. Периметр меньшего треугольника {p1}. Найдите периметр большего."
            answer = f"P₂ = k*P₁ = {k}*{p1} = {k * p1}"

    elif grade == 9:
        if topic == "векторы":
            x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
            x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
            exercise = f"Найдите сумму векторов a({x1};{y1}) и b({x2};{y2})."
            answer = f"a + b = ({x1 + x2}; {y1 + y2})"

        elif topic == "метод координат":
            x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
            x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
            exercise = f"Найдите расстояние между точками A({x1};{y1}) и B({x2};{y2})."
            dx, dy = x2 - x1, y2 - y1
            answer = f"AB = √({dx}² + {dy}²) = √({dx ** 2 + dy ** 2}) ≈ {sqrt(dx ** 2 + dy ** 2):.2f}"

        elif topic == "соотношения в треугольнике":
            a, b = random.randint(5, 15), random.randint(5, 15)
            angle = random.randint(30, 60)
            exercise = f"В треугольнике две стороны {a} и {b}, угол между ними {angle}°. Найдите площадь."
            rad = math.radians(angle)
            answer = f"S = ½ab·sinα = ½*{a}*{b}*sin{angle}° ≈ {0.5 * a * b * math.sin(rad):.2f}"

    return book, exercise, answer, None


def generate_school_informatics_task():
    GRADES = {
        7: ["информация и её кодирование", "алгоритмы и исполнители", "компьютерные сети"],
        8: ["программирование на Python", "логика и алгоритмы", "компьютерная графика"],
        9: ["базы данных", "компьютерные системы", "теория алгоритмов"]
    }

    grade = random.choice(list(GRADES.keys()))
    topic = random.choice(GRADES[grade])
    book = generate_book(SCHOOL_INFORMATICS_BOOKS)

    if grade == 7:
        if topic == "информация и её кодирование":
            bits = random.randint(8, 24)
            exercise = f"Сколько байт занимает сообщение длиной {bits} бит?"
            answer = f"{bits} бит = {bits // 8} байт и {bits % 8} бит"

        elif topic == "алгоритмы и исполнители":
            steps = random.randint(3, 8)
            exercise = f"Составьте алгоритм из {steps} шагов для исполнителя 'Робот', чтобы обойти препятствие."
            answer = "1. Вперёд 2\n 2. Поворот направо\n 3. Вперёд 1\n... (пример для {steps} шагов)"

        elif topic == "компьютерные сети":
            speed = random.choice([10, 100, 1000])
            exercise = f"Какая пропускная способность у сети со скоростью {speed} Мбит/с в байтах?"
            answer = f"{speed} Мбит/с = {speed * 10 ** 6 / 8} байт/с = {speed / 8} Мбайт/с"

    elif grade == 8:
        if topic == "программирование на Python":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            exercise = f"Напишите программу на Python для вычисления суммы чисел {a} и {b}"
            answer = f"print({a} + {b})  # Результат: {a + b}"

        elif topic == "логика и алгоритмы":
            x = random.choice([True, False])
            y = random.choice([True, False])
            exercise = f"Вычислите значение выражения: not ({x} and {y}) or {x}"
            answer = f"not ({x} and {y}) or {x} = {not (x and y) or x}"

        elif topic == "компьютерная графика":
            width = random.randint(100, 500)
            height = random.randint(100, 500)
            depth = random.choice([8, 16, 24, 32])
            exercise = f"Рассчитайте объем видеопамяти для изображения размером {width}x{height} пикселей с глубиной цвета {depth} бит"
            answer = f"{width} * {height} * {depth} бит = {width * height * depth / 8 / 1024:.1f} Кбайт"

    elif grade == 9:
        if topic == "базы данных":
            fields = random.randint(3, 8)
            records = random.randint(10, 1000)
            exercise = f"В базе данных {fields} полей и {records} записей. Сколько байт нужно для хранения, если каждое поле занимает 4 байта?"
            answer = f"{fields} * {records} * 4 = {fields * records * 4} байт"

        elif topic == "компьютерные системы":
            freq = random.choice([2.4, 3.0, 3.5, 4.0])
            cores = random.choice([2, 4, 6, 8])
            exercise = f"Процессор с частотой {freq} ГГц и {cores} ядрами. Какая теоретическая производительность в операциях/сек?"
            answer = f"{freq} ГГц * {cores} ядер = {freq * cores * 10 ** 9:.1e} операций/сек"

        elif topic == "теория алгоритмов":
            n = random.randint(5, 20)
            exercise = f"Оцените сложность алгоритма сортировки пузырьком для массива из {n} элементов"
            answer = f"O(n²) = O({n ** 2}) операций в худшем случае"

    return book, exercise, answer, None


def generate_school_physics_task():
    GRADES = {
        7: ["кинематика", "плотность вещества", "давление"],
        8: ["тепловые явления", "электричество", "оптика"],
        9: ["законы Ньютона", "электромагнетизм", "ядерная физика"]
    }

    grade = random.choice(list(GRADES.keys()))
    topic = random.choice(GRADES[grade])
    book = generate_book(SCHOOL_PHYSICS_BOOKS)

    if grade == 7:
        if topic == "кинематика":
            v = random.randint(1, 10)
            t = random.randint(1, 10)
            exercise = f"Тело движется со скоростью {v} м/с в течение {t} с. Найдите путь."
            answer = f"S = v * t = {v} * {t} = {v * t} м"

        elif topic == "плотность вещества":
            m = random.randint(10, 100)
            V = random.randint(1, 10)
            exercise = f"Масса тела {m} кг, объем {V} м³. Найдите плотность."
            answer = f"ρ = m/V = {m}/{V} = {m / V} кг/м³"

        elif topic == "давление":
            F = random.randint(10, 100)
            S = random.randint(1, 5)
            exercise = f"Сила {F} Н действует на площадь {S} м². Каково давление?"
            answer = f"p = F/S = {F}/{S} = {F / S} Па"

    elif grade == 8:
        if topic == "тепловые явления":
            m = random.randint(1, 5)
            Δt = random.randint(10, 50)
            c = 4200
            exercise = f"Какое количество теплоты нужно для нагрева {m} кг воды на {Δt}°C?"
            answer = f"Q = c * m * Δt = 4200 * {m} * {Δt} = {4200 * m * Δt} Дж"

        elif topic == "электричество":
            U = random.randint(1, 12)
            R = random.randint(1, 10)
            exercise = f"Напряжение в цепи {U} В, сопротивление {R} Ом. Найдите силу тока."
            answer = f"I = U/R = {U}/{R} = {U / R} А"

        elif topic == "оптика":
            f = random.randint(5, 20)
            exercise = f"Фокусное расстояние линзы {f} см. Найдите оптическую силу."
            answer = f"D = 1/f = 1/{f / 100} = {1 / (f / 100):.1f} дптр"

    elif grade == 9:
        if topic == "законы Ньютона":
            m = random.randint(1, 10)
            a = random.randint(1, 5)
            exercise = f"Тело массой {m} кг движется с ускорением {a} м/с². Найдите силу."
            answer = f"F = m * a = {m} * {a} = {m * a} Н (2-й закон Ньютона)"

        elif topic == "электромагнетизм":
            B = random.uniform(0.1, 1.0)
            I = random.randint(1, 5)
            L = random.randint(1, 10)
            exercise = f"Проводник длиной {L} м с током {I} А находится в магнитном поле {B:.1f} Тл. Найдите силу Ампера."
            answer = f"F = B * I * L = {B:.1f} * {I} * {L} = {B * I * L:.1f} Н"

        elif topic == "ядерная физика":
            E = random.randint(1, 10) * 1.6e-13
            exercise = f"Энергия связи ядра {E:.1e} Дж. Найдите дефект массы."
            answer = f"Δm = E/c² = {E:.1e} / (3e8)² ≈ {E / 9e16:.1e} кг"

    return book, exercise, answer, None


def generate_probability_task():
    topics = ["классическая вероятность", "условная вероятность", "случайные величины"]
    topic = random.choice(topics)
    book = generate_book(PROBABILITY_BOOKS)

    if topic == "классическая вероятность":
        n = random.randint(5, 10)
        k = random.randint(2, n - 1)
        exercise = f"В урне {n} шаров, {k} из них красные. Какова вероятность вытянуть красный шар?"
        answer = f"P = {k}/{n} = {k / n:.2f}"

    elif topic == "условная вероятность":
        pa = random.uniform(0.1, 0.5)
        pb_a = random.uniform(0.3, 0.7)
        exercise = f"P(A) = {pa:.2f}, P(B|A) = {pb_a:.2f}. Найдите P(A∩B)."
        answer = f"P(A∩B) = P(A)*P(B|A) = {pa:.2f}*{pb_a:.2f} = {pa * pb_a:.4f}"

    else:
        x = [1, 2, 3, 4]
        p = [0.1, 0.2, 0.3, 0.4]
        exercise = "Дана случайная величина X:\nX: " + " ".join(map(str, x)) + \
                   "\nP: " + " ".join(f"{val:.1f}" for val in p) + \
                   "\nНайдите математическое ожидание."
        answer = f"M(X) = {sum(xi * pi for xi, pi in zip(x, p)):.2f}"

    return book, exercise, answer, None


def generate_statistics_task():
    topics = ["описательная статистика", "доверительные интервалы", "проверка гипотез"]
    topic = random.choice(topics)
    book = generate_book(STATISTICS_BOOKS)

    if topic == "описательная статистика":
        data = [random.randint(10, 50) for _ in range(5)]
        exercise = f"Вычислите среднее и дисперсию для выборки: {data}"
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        answer = f"Среднее: {mean:.2f}, Дисперсия: {variance:.2f}"

    elif topic == "доверительные интервалы":
        mean = random.uniform(50, 100)
        n = random.randint(20, 100)
        std = random.uniform(5, 15)
        exercise = f"Постройте 95% доверительный интервал для среднего (n={n}, μ={mean:.1f}, σ={std:.1f})"
        margin = 1.96 * std / (n ** 0.5)
        answer = f"{mean:.1f} ± {margin:.2f} → ({mean - margin:.2f}, {mean + margin:.2f})"

    else:
        m1, m2 = random.uniform(70, 80), random.uniform(75, 85)
        s1, s2 = random.uniform(5, 10), random.uniform(5, 10)
        n1, n2 = random.randint(30, 50), random.randint(30, 50)
        exercise = f"Проверьте гипотезу о равенстве средних (α=0.05):\nГруппа 1: m={m1:.1f}, s={s1:.1f}, n={n1}\nГруппа 2: m={m2:.1f}, s={s2:.1f}, n={n2}"
        answer = "Расчет t-критерия Стьюдента (требуется дополнительное вычисление)"

    return book, exercise, answer, None


def generate_economics_task():
    topics = ["спрос и предложение", "эластичность", "издержки"]
    topic = random.choice(topics)
    book = generate_book(ECONOMICS_BOOKS)

    if topic == "спрос и предложение":
        qd = f"{random.randint(50, 100)} - {random.randint(2, 5)}P"
        qs = f"{random.randint(10, 40)} + {random.randint(2, 5)}P"
        exercise = f"Найдите равновесную цену и объем:\nQd = {qd}\nQs = {qs}"
        answer = "Приравнять Qd=Qs и решить уравнение"

    elif topic == "эластичность":
        p1, p2 = random.randint(10, 20), random.randint(21, 30)
        q1, q2 = random.randint(100, 200), random.randint(50, 99)
        exercise = f"Рассчитайте эластичность спроса по цене при изменении цены с {p1} до {p2} и объема с {q1} до {q2}"
        elasticity = ((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2))
        answer = f"E = {elasticity:.2f} ({'эластичный' if abs(elasticity) > 1 else 'неэластичный'})"

    else:
        fc = random.randint(1000, 5000)
        vc = random.randint(50, 150)
        q = random.randint(10, 100)
        exercise = f"Рассчитайте общие издержки при FC={fc}, VC={vc} на единицу, Q={q}"
        answer = f"TC = FC + VC*Q = {fc} + {vc}*{q} = {fc + vc * q}"

    return book, exercise, answer, None


def generate_algebra_task():
    topics = ["линейные уравнения", "квадратные уравнения", "матрицы"]
    topic = random.choice(topics)
    book = generate_book(ALGEBRA_BOOKS)

    if topic == "линейные уравнения":
        a = random.randint(1, 5)
        b = random.randint(10, 20)
        exercise = f"Решите уравнение: {a}x + {b} = 0"
        answer = f"x = {-b}/{a} = {-b / a}"

    elif topic == "квадратные уравнения":
        a, b, c = random.randint(1, 3), random.randint(-5, 5), random.randint(-3, 3)
        exercise = f"Решите квадратное уравнение: {a}x² + {b}x + {c} = 0"
        D = b ** 2 - 4 * a * c
        if D > 0:
            x1 = (-b + D ** 0.5) / (2 * a)
            x2 = (-b - D ** 0.5) / (2 * a)
            answer = f"D={D}, x1={x1:.2f}, x2={x2:.2f}"
        else:
            answer = f"D={D} (нет действительных корней)"

    else:
        m = [[random.randint(1, 5) for _ in range(2)] for _ in range(2)]
        exercise = "Найдите определитель матрицы:\n" + "\n".join(" ".join(map(str, row)) for row in m)
        det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        answer = f"det = {det}"

    return book, exercise, answer, None


def generate_calculus_task():
    topics = ["производные", "интегралы", "пределы"]
    topic = random.choice(topics)
    x = symbols('x')
    book = generate_book(CALCULUS_BOOKS)

    if topic == "производные":
        func = random.choice(["x**2", "sin(x)", "cos(x)", "tan(x)"])
        exercise = f"Найдите производную функции: f(x) = {func}"
        df = diff(func, x)
        answer = f"f'(x) = {df}"

    elif topic == "интегралы":
        func = random.choice(["x", "x**2", "2*x+1"])
        exercise = f"Вычислите интеграл: ∫({func})dx"
        integral = integrate(func, x)
        answer = f"∫({func})dx = {integral} + C"

    else:
        func = random.choice(["sin(x)/x", "(1-cos(x))/x", "(x**2-4)/(x-2)"])
        point = random.choice([0, 2])
        exercise = f"Найдите предел: lim(x→{point}) {func}"
        answer = "Использовать правило Лопиталя или алгебраические преобразования"

    return book, exercise, answer, None


def generate_crypto_task():
    topics = [
        "симметричные криптосистемы",
        "асимметричные криптосистемы",
        "хеш-функции",
        "электронная подпись",
        "криптографические протоколы"
    ]
    topic = random.choice(topics)
    book = generate_book(CRYPTO_BOOKS)

    if topic == "симметричные криптосистемы":
        shift = random.randint(1, 25)
        message = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
        exercise = f"Зашифруйте сообщение '{message}' с помощью шифра Цезаря со сдвигом {shift}."
        answer = "".join([chr((ord(c) - 65 + shift) % 26 + 65) for c in message])
        answer = f"Зашифрованное сообщение: {answer}"

    elif topic == "асимметричные криптосистемы":
        primes = [11, 13, 17, 19, 23, 29]
        p, q = random.sample(primes, 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        possible_e = [3, 5, 7, 11, 13, 17, 19]
        e = random.choice([x for x in possible_e if gcd(x, phi) == 1])
        m = random.randint(2, 10)
        exercise = f"""Даны p={p}, q={q}, e={e}. Зашифруйте сообщение m={m} по алгоритму RSA.
    Вычислите n, φ(n), d и зашифрованное сообщение c."""
        d = mod_inverse(e, phi)
        c = pow(m, e, n)
        answer = f"n = {n}, φ(n) = {phi}, d = {d}, c = {m}^{e} mod {n} = {c}"

    elif topic == "хеш-функции":
        values = [random.randint(100, 999) for _ in range(3)]
        mod = random.choice([10, 16, 100])
        exercise = f"""Найдите коллизию для хеш-функции h(x) = x mod {mod}.
    Пример: найти два разных числа с одинаковым хешем."""
        answer = f"Пример коллизии: {values[0]} mod {mod} = {values[0] % mod}, " + \
                 f"{values[1]} mod {mod} = {values[1] % mod} (при совпадении остатков)"

    elif topic == "электронная подпись":
        p = 23
        g = 5
        while True:
            x = random.randint(2, p - 2)
            if gcd(x, p - 1) == 1:
                break
        y = pow(g, x, p)
        while True:
            k = random.randint(2, p - 2)
            if gcd(k, p - 1) == 1:
                break
        m = random.randint(1, 10)
        exercise = f"""Сгенерируйте ЭЦП для сообщения m={m} по схеме ГОСТ Р 34.10-94.
    Даны p={p}, g={g}, закрытый ключ x={x}, k={k}."""
        r = pow(g, k, p)
        k_inv = mod_inverse(k, p - 1)
        s = (k_inv * (m - x * r)) % (p - 1)
        answer = f"Открытый ключ y = {y}, подпись (r, s) = ({r}, {s})"

    elif topic == "криптографические протоколы":
        p = 23
        g = 5
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        exercise = f"""Алиса и Боб используют протокол Диффи-Хеллмана.
    Даны p={p}, g={g}. Алиса выбрала a={a}, Боб выбрал b={b}.
    Вычислите общий секретный ключ."""
        A = pow(g, a, p)
        B = pow(g, b, p)
        K_A = pow(B, a, p)
        K_B = pow(A, b, p)
        answer = f"A = {g}^{a} mod {p} = {A}, B = {g}^{b} mod {p} = {B}\n" + \
                 f"K_A = B^a mod p = {K_A}, K_B = A^b mod p = {K_B}\n" + \
                 f"Общий ключ: {K_A}"

    return book, exercise, answer, None


def generate_networks_lab_task():
    topics = [
        "Настройка локальной сети",
        "Анализ сетевого трафика",
        "Конфигурация маршрутизатора",
        "Исследование протоколов TCP/IP",
        "Разработка клиент-серверного приложения"
    ]
    topic = random.choice(topics)
    book = generate_book(NETWORK_SECURITY_BOOKS)

    if topic == "Настройка локальной сети":
        ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        mask = "255.255.255.0"
        exercise = f"""Настройте локальную сеть между двумя компьютерами:
    1. Задайте IP-адрес: {ip}
    2. Маска подсети: {mask}
    3. Проверьте соединение командой ping"""
        answer = f"""1. Настройки сети:
       - IP: {ip}
       - Маска: {mask}
    2. Проверка:
       > ping {ip.replace(str(ip.split('.')[-1]), str(int(ip.split('.')[-1]) + 1))}
       Должны получить ответ от другого компьютера"""

    elif topic == "Анализ сетевого трафика":
        protocol = random.choice(["HTTP", "DNS", "ICMP"])
        exercise = f"""Захватите и проанализируйте сетевой трафик для протокола {protocol}:
    1. Запустите Wireshark
    2. Настройте фильтр для {protocol}
    3. Определите основные поля пакета"""
        answer = f"""Анализ протокола {protocol}:
    1. Основные поля:
       - {random.choice(['Source/Destination IP', 'Ports', 'Flags', 'Sequence number'])}
       - {random.choice(['Payload length', 'Checksum', 'Timestamp', 'TTL'])}
    2. Пример пакета: {random.randint(100, 500)} байт"""

    elif topic == "Конфигурация маршрутизатора":
        model = random.choice(["Cisco 2900", "TP-Link Archer", "MikroTik RB750"])
        exercise = f"""Настройте маршрутизатор {model}:
    1. Подключитесь через консоль
    2. Настройте NAT
    3. Проверьте работу интернета"""
        answer = f"""Настройка {model}:
    1. Команды:
       - {random.choice(['enable', 'configure terminal', 'interface fastethernet0/0'])}
       - {random.choice(['ip nat inside', 'ip nat outside', 'access-list 1 permit any'])}
    2. Проверка: ping 8.8.8.8"""

    elif topic == "Исследование протоколов TCP/IP":
        layer = random.randint(1, 4)
        exercise = f"""Исследуйте протоколы {layer}-го уровня модели TCP/IP:
    1. Приведите примеры протоколов
    2. Опишите формат заголовка
    3. Объясните процесс инкапсуляции"""
        answer = f"""Уровень {layer}:
    1. Протоколы: {random.choice([['HTTP', 'FTP', 'SMTP'], ['TCP', 'UDP'], ['IP', 'ICMP'], ['Ethernet', 'Wi-Fi']][layer - 1])}
    2. Заголовок: содержит поля {random.choice(['адреса', 'флаги', 'контрольные суммы', 'номера портов'])}
    3. Инкапсуляция: данные передаются с верхнего уровня на нижний"""

    else:
        lang = random.choice(["Python", "Java", "C++"])
        exercise = f"""Разработайте клиент-серверное приложение на {lang}:
    1. Реализуйте сервер, слушающий порт {random.randint(1024, 9999)}
    2. Создайте клиент для отправки/получения сообщений
    3. Проверьте работу в локальной сети"""
        answer = f"""Пример на {lang}:
    1. Сервер:
       - {random.choice(['socket()', 'bind()', 'listen()', 'accept()'])}
    2. Клиент:
       - {random.choice(['connect()', 'send()', 'recv()', 'close()'])}
    3. Тестирование: отправка сообщения 'Hello' и получение ответа"""

    book = f"{book}. Лабораторная работа: {topic}"

    return book, exercise, answer, None


def generate_algorithms_lab_task():
    topics = [
        "Реализация сортировки",
        "Поиск в структурах данных",
        "Работа с деревьями",
        "Алгоритмы на графах",
        "Динамическое программирование"
    ]
    topic = random.choice(topics)
    book = generate_book(PROGRAMMING_BOOKS)

    if topic == "Реализация сортировки":
        algo = random.choice(["пузырьковая", "быстрая", "слиянием"])
        arr = [random.randint(1, 100) for _ in range(5)]
        exercise = f"""Реализуйте {algo} сортировку для массива:
    {arr}
    1. Напишите код на Python
    2. Объясните временную сложность
    3. Проверьте на разных наборах данных"""
        answer = f"""Алгоритм {algo} сортировки:
    1. Код:
       def {algo}_sort(arr):
           # Реализация алгоритма
           return sorted_arr
    2. Сложность: {random.choice(['O(n^2)', 'O(n log n)', 'O(n)'])}
    3. Результат: {sorted(arr)}"""

    elif topic == "Поиск в структурах данных":
        struct = random.choice(["хэш-таблица", "бинарное дерево", "связный список"])
        val = random.randint(10, 99)
        exercise = f"""Реализуйте поиск элемента {val} в {struct}:
    1. Создайте структуру данных
    2. Реализуйте алгоритм поиска
    3. Проанализируйте эффективность"""
        code_snippet = f"def search_{struct.replace(' ', '_')}(data, target):\n    # Реализация поиска\n    return found"
        answer = f"""Поиск в {struct}:
    1. {random.choice(['Хэш-функция: key % size', 'Рекурсивный обход', 'Линейный поиск'])}
    2. Код:
       {code_snippet}
    3. Сложность: {random.choice(['O(1)', 'O(log n)', 'O(n)'])}"""

    elif topic == "Работа с деревьями":
        tree_type = random.choice(["бинарное", "AVL", "красно-черное"])
        exercise = f"""Работа с {tree_type} деревом:
    1. Реализуйте вставку элемента
    2. Напишите функцию обхода (in-order)
    3. Удалите узел и балансируйте дерево"""
        code_snippet = f"""def traverse(node):
        if node:
            traverse(node.left)
            print(node.value)
            traverse(node.right)"""
        answer = f"""Дерево {tree_type}:
    1. Вставка:
       - {random.choice(['Сравнение значений', 'Рекурсивный спуск', 'Повороты для балансировки'])}
    2. Обход:
       {code_snippet}
    3. Балансировка: {random.choice(['Одина roja поворот', 'Двойной поворот', 'Перекрашивание узлов'])}"""

    elif topic == "Алгоритмы на графах":
        algo = random.choice(["Дейкстры", "Крускала", "Флойда-Уоршелла"])
        exercise = f"""Реализуйте алгоритм {algo}:
    1. Представьте граф в коде
    2. Напишите алгоритм
    3. Найдите {random.choice(['кратчайший путь', 'минимальное остовное дерево', 'транзитивное замыкание'])}"""
        code_snippet = f"def {algo.lower().replace('-', '_')}(graph):\n    # Реализация алгоритма\n    return result"
        answer = f"""Алгоритм {algo}:
    1. Граф:
       - {random.choice(['Матрица смежности', 'Список смежности', 'Ребра с весами'])}
    2. Код:
       {code_snippet}
    3. Результат: {random.choice(['Путь длиной X', 'Дерево с весом Y', 'Матрица достижимости'])}"""

    else:
        problem = random.choice(["рюкзак", "наибольшая подпоследовательность", "размен монет"])
        exercise = f"""Решите задачу {problem} методом динамического программирования:
    1. Определите подзадачи
    2. Запишите рекуррентное соотношение
    3. Реализуйте итеративное решение"""
        code_snippet = f"""def {problem.replace(' ', '_')}(items):
        # Реализация динамического программирования
        return result"""
        answer = f"""Динамическое программирование ({problem}):
    1. Подзадачи: {random.choice(['частичные суммы', 'префиксы последовательности', 'ограниченная вместимость'])}
    2. Соотношение:
       - {random.choice(['dp[i] = max(dp[i], dp[i-w] + v)', 'dp[i][j] = dp[i-1][j-1] + 1', 'dp[i] = min(dp[i], dp[i-c] + 1)'])}
    3. Решение:
       {code_snippet}
       Сложность: {random.choice(['O(nW)', 'O(n^2)', 'O(nk)'])}"""

    book = f"{book}. Лабораторная работа: {topic}"

    return book, exercise, answer, None


def generate_number_theory_lab_task():
    topics = [
        "Алгоритм Евклида и расширенный алгоритм Евклида",
        "Малая теорема Ферма и тест Ферма",
        "Функция Эйлера и теорема Эйлера",
        "Китайская теорема об остатках",
        "Тест Миллера-Рабина на простоту",
        "Дискретное логарифмирование",
        "Возведение в степень по модулю"
    ]
    topic = random.choice(topics)
    book = generate_book(CRYPTO_BOOKS)

    if topic == "Алгоритм Евклида и расширенный алгоритм Евклида":
        a, b = random.randint(100, 1000), random.randint(100, 1000)
        exercise = f"""1. С помощью алгоритма Евклида вычислите НОД({a}, {b})
    2. Используя расширенный алгоритм Евклида, найдите коэффициенты Безу (x, y) такие, что {a}*x + {b}*y = НОД({a}, {b})"""
        answer = f"""1. НОД({a}, {b}) = {math.gcd(a, b)}
    2. Коэффициенты Безу: x = [вычисленное значение], y = [вычисленное значение]"""

    elif topic == "Малая теорема Ферма и тест Ферма":
        p = random.choice([17, 19, 23, 29, 31])
        a = random.randint(2, p - 2)
        exercise = f"""1. Проверьте выполнение малой теоремы Ферма для a = {a}, p = {p}
    2. С помощью теста Ферма проверьте числа {p} и {p + 1} на простоту"""
        answer = f"""1. {a}^({p}-1) mod {p} = [вычисленное значение]
    2. Число {p} - [простое/составное], число {p + 1} - [простое/составное]"""

    elif topic == "Функция Эйлера и теорема Эйлера":
        n = random.choice([10, 12, 15, 20])
        a = random.randint(2, n - 1)
        while math.gcd(a, n) != 1:
            a = random.randint(2, n - 1)
        exercise = f"""1. Вычислите значение функции Эйлера φ({n})
    2. Проверьте выполнение теоремы Эйлера для a = {a}, n = {n}
    3. Найдите обратный элемент к {a} mod {n}"""
        answer = f"""1. φ({n}) = [вычисленное значение]
    2. {a}^φ({n}) mod {n} = [вычисленное значение]
    3. Обратный элемент к {a} mod {n} = [вычисленное значение]"""

    elif topic == "Китайская теорема об остатках":
        congruences = [(random.randint(2, 10), random.choice([3, 5, 7])) for _ in range(2)]
        exercise = f"""Решите систему сравнений:
    x ≡ {congruences[0][0]} mod {congruences[0][1]}
    x ≡ {congruences[1][0]} mod {congruences[1][1]}
    Найдите наименьшее положительное решение"""
        answer = f"""Решение: x ≡ [вычисленное значение] mod {congruences[0][1] * congruences[1][1]}"""

    elif topic == "Тест Миллера-Рабина на простоту":
        n = random.choice([17, 21, 29, 33, 37])
        exercise = f"""1. С помощью теста Миллера-Рабина проверьте число {n} на простоту
    2. Объясните полученный результат"""
        answer = f"""1. Число {n} - [вероятно простое/составное]
    2. Вероятность ошибки теста не превышает 25% для одного раунда"""

    elif topic == "Дискретное логарифмирование":
        p = random.choice([7, 11, 13, 17])
        g = random.choice([2, 3, 5])
        a = random.randint(2, p - 2)
        exercise = f"""Решите задачу дискретного логарифмирования:
    Найдите x такое, что {g}^x ≡ {pow(g, a, p)} mod {p}"""
        answer = f"""Решение: x = [вычисленное значение] (проверка: {g}^x mod {p} = {pow(g, a, p)})"""

    else:
        a = random.randint(10, 100)
        b = random.randint(10, 100)
        n = random.randint(10, 100)
        exercise = f"""Вычислите значение выражения {a}^{b} mod {n} с использованием алгоритма быстрого возведения в степень"""
        answer = f"""Результат: {a}^{b} mod {n} = [вычисленное значение]"""

    book = f"{book}. Лабораторная работа: {topic}"

    return book, exercise, answer, None


def generate_security_models_lab_task():
    topics = [
        "Модель Белла-Лападулы",
        "Модель Биба",
        "Модель Кларка-Вильсона",
        "Мандатное управление доступом",
        "Ролевое управление доступом (RBAC)",
        "Анализ рисков и угроз",
        "Построение матрицы доступа"
    ]
    topic = random.choice(topics)
    book = generate_book(SECURITY_MODELS_BOOKS)

    if topic == "Модель Белла-Лападулы":
        levels = ["совершенно секретно", "секретно", "конфиденциально", "несекретно"]
        subject_level = random.choice(levels)
        object_level = random.choice(levels)
        subject = "Офицер Иванов"
        obj = "Документ МО-2024"
        exercise = f"""1. Субъект '{subject}' (уровень: {subject_level}) пытается:
       - Прочитать '{obj}' (уровень: {object_level})
       - Записать в '{obj}'
    2. Определите, разрешены ли операции"""
        can_read = levels.index(subject_level) >= levels.index(object_level)
        can_write = levels.index(subject_level) <= levels.index(object_level)
        answer = f"""1. Результат:
       - Чтение: {'Разрешено' if can_read else 'Запрещено'} (No Read Up)
       - Запись: {'Разрешено' if can_write else 'Запрещено'} (No Write Down)"""

    elif topic == "Модель Биба":
        levels = ["критический", "важный", "обычный", "низкий"]
        process_level = random.choice(levels)
        data_level = random.choice(levels)
        exercise = f"""1. Процесс 'Платежная система' (уровень: {process_level}) пытается:
       - Изменить данные 'Баланс клиента' (уровень: {data_level})
       - Прочитать журнал операций (уровень: {data_level})
    2. Проверьте допустимость операций"""
        can_write = levels.index(process_level) <= levels.index(data_level)
        can_read = levels.index(process_level) >= levels.index(data_level)
        answer = f"""1. Результат:
       - Запись: {'Разрешена' if can_write else 'Запрещена'} (No Write Up)
       - Чтение: {'Разрешено' if can_read else 'Запрещено'} (No Read Down)"""

    elif topic == "Модель Кларка-Вильсона":
        exercise = """1. Для банковской системы определите:
       - CDI: Баланс счета, История транзакций
       - Правило трансформации: Перевод средств (сумма > 0, баланс ≥ суммы)
       - IVP: Ежедневная сверка балансов"""
        answer = """1. Пример реализации:
       - CDI: Баланс счета (целостность), История транзакций (полнота)
       - Правило: IF сумма > 0 AND баланс_отправителя >= сумма 
                  THEN уменьшить(отправитель, сумма), увеличить(получатель, сумма)
       - IVP: Сумма всех транзакций за день = Разница балансов"""

    elif topic == "Мандатное управление доступом":
        labels = ["TS: NATO", "S: NATO", "C: NATO", "U: PUBLIC"]
        selected = random.sample(labels, 2)
        exercise = f"""1. Может ли субъект с меткой '{selected[0]}':
       - Прочитать объект с меткой '{selected[1]}'
       - Записать в объект с меткой '{selected[1]}'"""
        read_ok = labels.index(selected[0]) >= labels.index(selected[1])
        write_ok = labels.index(selected[0]) <= labels.index(selected[1])
        answer = f"""1. Результат:
       - Чтение: {'Да' if read_ok else 'Нет'} (доминирует по чтению)
       - Запись: {'Да' if write_ok else 'Нет'} (доминирует по записи)"""

    elif topic == "Ролевое управление доступом (RBAC)":
        roles = {
            "Кассир": ["снять наличные", "внести платеж"],
            "Бухгалтер": ["провести транзакцию", "сформировать отчет"],
            "Аудитор": ["просмотр отчетов"]
        }
        role = random.choice(list(roles.keys()))
        exercise = f"""1. Для роли '{role}':
       - Проверьте, может ли она: {random.choice(roles[role])}
       - Может ли она: {'изменить курс валют' if role != 'Администратор' else 'удалить пользователя'}"""
        answer = f"""1. Результат:
       - Разрешено: {roles[role][0]}
       - Запрещено: {'изменить курс валют' if role != 'Администратор' else 'удалить пользователя'}"""

    elif topic == "Анализ рисков и угроз":
        threats = {
            "Утечка данных": "Высокий",
            "Отказ в обслуживании": "Средний",
            "Подмена сотрудника": "Низкий"
        }
        exercise = """1. Для системы 'Онлайн-банк':
       - Основные угрозы: Утечка данных, Отказ в обслуживании
       - Контрмеры: Шифрование, DDoS-защита"""
        answer = """1. Оценка рисков:
       - Утечка данных (риск: Высокий) → Шифрование TLS 1.3
       - DDoS (риск: Средний) → Cloudflare Protection"""

    else:
        matrix = {
            "Админ": {"Файл1": "чтение, запись", "Сокет2": "все"},
            "Пользователь": {"Файл1": "чтение"}
        }
        exercise = """1. Матрица доступа:
       - Админ → Файл1: чтение, запись
       - Пользователь → Файл1: чтение
    2. Может ли Пользователь записать в Файл1?"""
        answer = """1. Проверка:
       - Админ имеет полный доступ
       - Пользователь не может записывать в Файл1"""

    book = f"{book}. Лабораторная работа: {topic}"

    return book, exercise, answer, None


def get_base_path():
    """Возвращает абсолютный путь к директории чекера"""
    if getattr(sys, 'frozen', False):
        # Для исполняемых файлов (pyinstaller)
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _gen_gdz_random_image_random_answer_frog():
    # Списки для случайного выбора
    description_options = [
        "лягушачья пропаганда",
        "лягушачьи теории заговора",
        "болотная вечеринка",
        "Жабья инициация",
        "Сеанс Жабьей Правды",
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

    BASE_DIR = get_base_path()
    # Директории для изображений и цитат
    IMAGES_DIR = os.path.join(BASE_DIR, "Data_for_generations", "french_language", "images")
    QUOTES_FILE = os.path.join(BASE_DIR, "Data_for_generations", "french_language", "frogs.txt")

    # Загрузка случайной цитаты
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            quotes = [line.strip() for line in f.readlines() if line.strip()]
            random_quote = random.choice(quotes)
    except Exception as e:
        print(f"Ошибка загрузки цитат: {e}")
        random_quote = "Ответ: 42"

    # Случайный выбор описаний с добавлением префикса
    prefix = "Обычное"
    random_description = f"{prefix} ГДЗ: {random.choice(description_options)}"
    random_full_description = f"{prefix} ГДЗ: {random.choice(full_description_options)}"

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
    return random_description, random_full_description, random_quote, image_path


def _gen_gdz_js(is_elite=False, is_paid=False):
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

    BASE_DIR = get_base_path()
    # Директории для изображений
    IMAGES_DIR = os.path.join(BASE_DIR, "Data_for_generations", "js")
    print(IMAGES_DIR)

    # Выбираем случайный индекс
    random_idx = random.randint(0, len(full_descriptions) - 1)

    prefix = "Обычное"
    random_description = f"{prefix} ГДЗ: {random.choice(description_options)}"

    random_full_description = f"{prefix} ГДЗ: {full_descriptions[random_idx]}"

    selected_quote = quotes[random_idx]

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

    return random_description, random_full_description, selected_quote, image_path


def _gen_memology():
    # Списки для случайного выбора
    description_options = f"Мемология. Задача {random.randint(1, 1000)}"
    full_description_options = "Мемология - царица наук"
    content_text = "ха-ха"

    BASE_DIR = get_base_path()
    # Директории для изображений и цитат
    IMAGES_DIR = os.path.join(BASE_DIR, "Data_for_generations", "just memes images")

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
    return description_options, full_description_options, content_text, image_path


CATEGORY_GENERATORS = {
    "Школьные задачи_Алгебра": generate_school_algebra_task,
    "Школьные задачи_Геометрия": generate_school_geometry_task,
    "Школьные задачи_Физика": generate_school_physics_task,
    "Школьные задачи_Информатика": generate_school_informatics_task,
    "Университетские задачи_Экономика": generate_economics_task,
    "Университетские задачи_КМЗИ": generate_crypto_task,
    "Университетские задачи_Мат.статистика": generate_statistics_task,
    "Университетские задачи_Теория вероятностей": generate_probability_task,
    "Университетские задачи_Алгебра": generate_algebra_task,
    "Университетские задачи_Мат.анализ": generate_calculus_task,
    "Лабораторные работы_Компьютерные сети": generate_networks_lab_task,
    "Лабораторные работы_АИСД": generate_algorithms_lab_task,
    "Лабораторные работы_ТЧМК": generate_number_theory_lab_task,
    "Лабораторные работы_Модели безопасности": generate_security_models_lab_task,
    "Мемология_Уроки Французского": _gen_gdz_random_image_random_answer_frog,
    "Мемология_Джаваскриптолюбие": _gen_gdz_js,
    "Мемология_Царица наук": _gen_memology

}


def clean_string(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r'\\n[0-9]+', '\n', text)  # Удаляем \n1, \n2 и т.д.
    text = text.replace('\\\n', '\n')  # Исправляем экранированные \n
    text = re.sub(r'\s+', ' ', text).strip()  # Удаляем лишние пробелы
    return text


def dynamic_generate(category):
    if category not in CATEGORY_GENERATORS:
        raise ValueError(f"Неверная категория: {category}. Доступные категории: {list(CATEGORY_GENERATORS.keys())}")

    generator = CATEGORY_GENERATORS[category]
    book, exercise, answer, path = generator()
    book = clean_string(book)
    exercise = clean_string(exercise)
    answer = clean_string(exercise)
    task = {
        "description": book,
        "full_description": exercise,
        "content_text": answer,
        "content": path
    }
    return task
