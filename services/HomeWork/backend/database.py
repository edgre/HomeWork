from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db" / "database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

INITIAL_SUBJECTS = [
    {"subject_name": "Мат.анализ", "category": "Университетские задачи", "paths": "Университетские задачи_Мат.анализ"},
    {"subject_name": "Модели безопасности", "category": "Лабораторные работы", "paths": "Лабораторные работы_Модели безопасности"},
    {"subject_name": "Компьютерные сети", "category": "Лабораторные работы", "paths": "Лабораторные работы_Компьютерные сети"},
    {"subject_name": "ТЧМК", "category": "Лабораторные работы", "paths": "Лабораторные работы_ТЧМК"},
    {"subject_name": "АИСД", "category": "Лабораторные работы", "paths": "Лабораторные работы_Языки программирования"},
    {"subject_name": "Алгебра", "category": "Школьные задачи", "paths": "Школьные задачи_Алгебра"},
    {"subject_name": "Геометрия", "category": "Школьные задачи", "paths": "Школьные задачи_Геометрия"},
    {"subject_name": "Физика", "category": "Школьные задачи", "paths": "Школьные задачи_Физика"},
    {"subject_name": "Экономика", "category": "Университетские задачи", "paths": "Университетские задачи_Экономика"},
    {"subject_name": "КМЗИ", "category": "Университетские задачи", "paths": "Университетские задачи_КМЗИ"},
    {"subject_name": "Мат.статистика", "category": "Университетские задачи", "paths": "Университетские задачи_Мат.статистика"},
    {"subject_name": "Теория вероятностей", "category": "Университетские задачи", "paths": "Университетские задачи_Теория вероятностей"},
    {"subject_name": "Алгебра", "category": "Университетские задачи", "paths": "Университетские задачи_Алгебра"},
    {"subject_name": "Программирование", "category": "Университетские задачи", "paths": "Университетские задачи_Программирование"},
    {"subject_name": "Информатика", "category": "Школьные задачи", "paths": "Школьные задачи_Информатика"},
    {"subject_name": "Уроки Французского", "category": "Мемология", "paths": "Мемология_Уроки Французского"},
    {"subject_name": "Инглиш мафака", "category": "Мемология", "paths": "Мемология_Инглиш мафака"},
    {"subject_name": "Джаваскриптолюбие", "category": "Мемология", "paths": "Мемология_Джаваскриптолюбие"},
    {"subject_name": "Царица наук", "category": "Мемология", "paths": "Мемология_Царица наук"},
]

def add_initial_subjects(db: sessionmaker):
    try:
        from models import Subjects
        for subject_data in INITIAL_SUBJECTS:
                subject = Subjects(
                    subject_name=subject_data["subject_name"],
                    category=subject_data["category"],
                    paths=subject_data["paths"]
                )
                db.add(subject)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении начальных записей: {str(e)}")
        raise

def init_db():
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            from models import User, Subjects, GDZ, Purchase, GDZRating, Codes, Base
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            try:
                add_initial_subjects(db)
            finally:
                db.close()
        except Exception as e:
            print(f"Ошибка при создании базы данных или добавлении записей: {str(e)}")
            raise

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
init_db()
