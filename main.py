import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel
)

def main():
    app = QApplication(sys.argv)
    widget = QWidget()

    text_label = QLabel("Hello World", widget)
    text_label.move(115, 90)

    widget.setWindowTitle("First Application")
    widget.resize(300, 200)
    widget.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
