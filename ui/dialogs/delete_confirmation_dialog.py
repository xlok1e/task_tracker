from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class DeleteConfirmationDialog(QDialog):
    def __init__(self, parent=None, dialog_title: str = None, dialog_text: str = None):
        super().__init__(parent)
        self.setWindowTitle(dialog_title)
        self.setMinimumSize(450, 100)
        self.setMaximumSize(450, 100)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.text = dialog_text
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.dialog_text = QLabel(self.text)
        self.dialog_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.dialog_text)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.accept)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)