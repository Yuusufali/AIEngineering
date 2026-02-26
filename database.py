"""
Модуль работы с SQLite: подключение, таблица пользователей, запросы для авторизации.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")


def get_connection():
    """Возвращает подключение к БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # доступ к колонкам по имени
    return conn


def init_db():
    """Создаёт таблицу users, если её ещё нет."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def create_user(username: str, password_hash: str) -> int | None:
    """
    Добавляет пользователя. Возвращает id или None при ошибке (например, дубликат username).
    """
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username.strip(), password_hash),
            )
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username: str) -> sqlite3.Row | None:
    """Возвращает строку пользователя по username или None."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, username, password_hash, created_at FROM users WHERE username = ?",
            (username.strip(),),
        )
        return cur.fetchone()


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    """Возвращает строку пользователя по id или None."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,),
        )
        return cur.fetchone()
