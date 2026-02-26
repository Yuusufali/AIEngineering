"""
Веб-приложение Mini AI: БД, авторизация, Flask.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

from database import init_db, get_user_by_id
from auth import login as do_login, register as do_register

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
init_db()


def get_current_user():
    """Возвращает данные текущего пользователя из сессии или None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    row = get_user_by_id(user_id)
    if row is None:
        session.pop("user_id", None)
        return None
    return {"id": row["id"], "username": row["username"], "created_at": row["created_at"]}


@app.route("/")
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user():
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ok, msg, user = do_login(username, password)
        if ok:
            session["user_id"] = user["id"]
            flash("Вход выполнен.", "success")
            return redirect(url_for("index"))
        flash(msg, "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if get_current_user():
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        if password != password2:
            flash("Пароли не совпадают.", "error")
        else:
            ok, msg = do_register(username, password)
            flash(msg, "success" if ok else "error")
            if ok:
                return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    flash("Вы вышли из аккаунта.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
