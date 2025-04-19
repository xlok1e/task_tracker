from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить новую задачу')
        self.resize(500, 120)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Введите название задачи")
        self.layout.addWidget(self.input_field)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel, self
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_task_text(self):
        return self.input_field.text()