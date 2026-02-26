"""
Окно входа и регистрации.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QFormLayout,
    QMessageBox,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from auth import login as do_login, register as do_register


class AuthWindow(QWidget):
    """Окно с формами «Вход» и «Регистрация»."""

    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("Mini AI — Вход")
        self.setMinimumSize(360, 320)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Mini AI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self._make_login_form())
        self.stacked.addWidget(self._make_register_form())
        layout.addWidget(self.stacked)

        switch_label = QLabel("Нет аккаунта?")
        switch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(switch_label)
        self.btn_switch = QPushButton("Зарегистрироваться")
        self.btn_switch.setFlat(True)
        self.btn_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_switch.clicked.connect(self._switch_to_register)
        layout.addWidget(self.btn_switch, alignment=Qt.AlignmentFlag.AlignCenter)

    def _make_login_form(self):
        form = QWidget()
        fl = QFormLayout(form)
        fl.setSpacing(12)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Логин")
        self.login_username.setMinimumHeight(36)
        fl.addRow("Логин:", self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Пароль")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setMinimumHeight(36)
        fl.addRow("Пароль:", self.login_password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.setMinimumHeight(40)
        self.btn_login.setDefault(True)
        self.btn_login.clicked.connect(self._on_login)
        fl.addRow(self.btn_login)

        return form

    def _make_register_form(self):
        form = QWidget()
        fl = QFormLayout(form)
        fl.setSpacing(12)

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Логин")
        self.reg_username.setMinimumHeight(36)
        fl.addRow("Логин:", self.reg_username)

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Пароль (мин. 4 символа)")
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password.setMinimumHeight(36)
        fl.addRow("Пароль:", self.reg_password)

        self.reg_password2 = QLineEdit()
        self.reg_password2.setPlaceholderText("Повторите пароль")
        self.reg_password2.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password2.setMinimumHeight(36)
        fl.addRow("Повтор:", self.reg_password2)

        self.btn_register = QPushButton("Зарегистрироваться")
        self.btn_register.setMinimumHeight(40)
        self.btn_register.clicked.connect(self._on_register)
        fl.addRow(self.btn_register)

        return form

    def _switch_to_register(self):
        self.stacked.setCurrentIndex(1)
        self.btn_switch.setText("Уже есть аккаунт? Войти")
        self.btn_switch.clicked.disconnect()
        self.btn_switch.clicked.connect(self._switch_to_login)
        self.setWindowTitle("Mini AI — Регистрация")

    def _switch_to_login(self):
        self.stacked.setCurrentIndex(0)
        self.btn_switch.setText("Зарегистрироваться")
        self.btn_switch.clicked.disconnect()
        self.btn_switch.clicked.connect(self._switch_to_register)
        self.setWindowTitle("Mini AI — Вход")

    def _on_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        ok, msg, user = do_login(username, password)
        if ok:
            self.on_login_success(user)
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка входа", msg)

    def _on_register(self):
        username = self.reg_username.text()
        password = self.reg_password.text()
        password2 = self.reg_password2.text()
        if password != password2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return
        ok, msg = do_register(username, password)
        QMessageBox.information(self, "Регистрация", msg)
        if ok:
            self._switch_to_login()
