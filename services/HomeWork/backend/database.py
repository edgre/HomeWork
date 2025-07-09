import os
from pathlib import Path
import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DATABASE_URL = "sqlite:///./db/database.db"
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db" / "database.db"

# SQL для создания таблиц
INIT_SQL = """
CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "purchases" (
        "id"    INTEGER,
        "buyer_id"      INTEGER,
        "gdz_id"        INTEGER,
        PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "subjects" (
        "subject_name"  TEXT,
        "category"      TEXT NOT NULL,
        "id"    INTEGER,
        "paths" TEXT,
        PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "gdz_ratings" (
        "id"    INTEGER,
        "gdz_id"        INTEGER,
        "user_id"       INTEGER,
        "value" INTEGER, 
        created_at DATETIME,
        PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
        "id"    INTEGER,
        "username"      TEXT NOT NULL UNIQUE,
        "password_hash" TEXT NOT NULL,
        "realname"      TEXT NOT NULL,
        "user_rating"   NUMERIC,
        "has_draft"     INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "codes" (
        "id"    INTEGER,
        "user_id"       INTEGER,
        "gdz_id"        INTEGER,
        "code"  TEXT,
        PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "gdz" (
        "id"    INTEGER,
        "owner_id"      INTEGER NOT NULL,
        "content"       TEXT,
        "content_text"  TEXT,
        "description"   TEXT NOT NULL,
        "category"      TEXT NOT NULL,
        "is_elite"      INTEGER NOT NULL,
        "price" INTEGER NOT NULL,
        "full_description"      TEXT,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("owner_id") REFERENCES "users"("id")
);
"""

def init_db():
    """Инициализирует БД, если она не существует"""
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        engine = sql.create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(sql.text(INIT_SQL))
        print(f"Создана новая БД: {DB_PATH}")

init_db()

engine = sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()