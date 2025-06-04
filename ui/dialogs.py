from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QComboBox, QTextEdit, QDateEdit
from PySide6.QtCore import QDate


class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить новую задачу')
        self.setFixedSize(500, 300)
        # todo убрать возможность ставить весь экран
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.name_field = QLineEdit(self)
        self.name_field.setPlaceholderText("Введите название задачи")
        layout.addWidget(self.name_field)

        self.date_field = QDateEdit(self)
        self.date_field.setCalendarPopup(True)
        self.date_field.setDate(QDate.currentDate())
        self.date_field.setDisplayFormat("dd.MM.yyyy")
        self.date_field.setCalendarPopup(True)
        layout.addWidget(self.date_field)

        self.priority_select = QComboBox(self)
        self.priority_select.addItems(["Не задан", "Низкий", "Средний", "Высокий"])
        self.priority_select.setPlaceholderText("Выберите приоритет задачи")
        layout.addWidget(self.priority_select)

        # Описание задачи
        self.description_field = QTextEdit(self)
        self.description_field.setFixedHeight(100)
        self.description_field.setStyleSheet("QTextEdit { vertical-align: top; }")
        self.description_field.setPlaceholderText("Введите описание задачи")
        self.description_field.setAcceptRichText(False)
        layout.addWidget(self.description_field)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_task_text(self):
        return self.name_field.text()

    def get_description(self):
        return self.description_field.toPlainText()

    def get_priority(self):
        priority_text = self.priority_select.currentText()
        priority_map = {
            "Не задан": 0,
            "Низкий": 1,
            "Средний": 2,
            "Высокий": 3
        }
        return priority_map.get(priority_text, 0)
    
    def get_date(self):
        return self.date_field.date().toString("yyyy-MM-dd")
