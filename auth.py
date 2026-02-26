"""
Авторизация: хеширование пароля, регистрация и вход.
"""
import hashlib
import secrets

from database import init_db, create_user, get_user_by_username

# соль храним в коде для простоты; в продакшене — в конфиге/переменных окружения
PEPPER = "ai_engineering_mini_app"


def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """Хеширует пароль с солью. Возвращает (hash_hex, salt)."""
    if salt is None:
        salt = secrets.token_hex(16)
    raw = f"{PEPPER}{salt}{password}"
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return h, salt


def register(username: str, password: str) -> tuple[bool, str]:
    """
    Регистрация нового пользователя.
    Возвращает (успех, сообщение).
    """
    username = username.strip()
    if not username:
        return False, "Введите логин."
    if not password:
        return False, "Введите пароль."
    if len(password) < 4:
        return False, "Пароль должен быть не короче 4 символов."

    init_db()
    password_hash, salt = _hash_password(password)
    # храним как "salt:hash" для проверки при входе
    stored = f"{salt}:{password_hash}"
    user_id = create_user(username, stored)
    if user_id is None:
        return False, "Пользователь с таким логином уже существует."
    return True, "Регистрация успешна. Войдите в аккаунт."


def login(username: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Вход по логину и паролю.
    Возвращает (успех, сообщение, данные_пользователя или None).
    """
    username = username.strip()
    if not username or not password:
        return False, "Введите логин и пароль.", None

    init_db()
    row = get_user_by_username(username)
    if row is None:
        return False, "Неверный логин или пароль.", None

    stored = row["password_hash"]
    if ":" not in stored:
        return False, "Ошибка формата данных пользователя.", None
    salt, expected_hash = stored.split(":", 1)
    password_hash, _ = _hash_password(password, salt)
    if password_hash != expected_hash:
        return False, "Неверный логин или пароль.", None

    user = {"id": row["id"], "username": row["username"], "created_at": row["created_at"]}
    return True, "Вход выполнен.", user
