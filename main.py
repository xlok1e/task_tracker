import sys
from PySide6.QtWidgets import QApplication

from ui.mainwindow import MainWindow
from utils.utils import load_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("resources/styles.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
