"""
Главное окно после входа.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MainWindow(QWidget):
    """Главное окно приложения после авторизации."""

    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout
        self.setWindowTitle("Mini AI — Главная")
        self.setMinimumSize(480, 320)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QHBoxLayout()
        title = QLabel("Mini AI")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        header.addWidget(title)
        header.addStretch()
        btn_logout = QPushButton("Выйти")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.on_logout)
        header.addWidget(btn_logout)
        layout.addLayout(header)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        welcome = QLabel(f"Добро пожаловать, {self.user['username']}!")
        welcome.setWordWrap(True)
        layout.addWidget(welcome)

        info = QLabel(
            "Подключение к БД активно. Авторизация выполнена.\n"
            "Здесь можно добавить функции AI и другие разделы."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #555;")
        layout.addWidget(info)

        layout.addStretch()
