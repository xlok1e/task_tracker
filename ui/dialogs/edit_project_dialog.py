from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class EditProjectDialog(QDialog):
    def __init__(self, parent=None, project_name: str = None):
        super().__init__(parent)
        self.setWindowTitle('Редактировать проект')
        self.setFixedSize(500, 300)
        self.project_name = project_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.name_field = QLineEdit(self)
        self.name_field.setPlaceholderText("Введите название проекта")
        self.name_field.setMaxLength(150)
        if self.project_name:
            self.name_field.setText(self.project_name)
        layout.addWidget(self.name_field)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("save_button")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def validate_and_accept(self):
        if not self.name_field.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название проекта не может быть пустым")
            return
        self.accept()