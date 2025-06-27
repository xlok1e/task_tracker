from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QComboBox, QTextEdit, QDateEdit, QMessageBox
from PySide6.QtCore import QDate

class AddOrEditTaskDialog(QDialog):
    def __init__(self, parent=None, task_name: str = None, description: str = None, priority: int = None, date: str = None, task_id: int = None, column_id: int = None):
        super().__init__(parent)
        self.setWindowTitle('Добавить новую задачу' if task_id is None else 'Редактировать задачу')
        self.setFixedSize(500, 300)
        # TODO убрать возможность ставить весь экран
        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.date = date
        self.task_id = task_id
        self.column_id = column_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.name_field = QLineEdit(self)
        self.name_field.setPlaceholderText("Введите название задачи")
        self.name_field.setMaxLength(150)
        if self.task_name:
            self.name_field.setText(self.task_name)
        layout.addWidget(self.name_field)

        self.date_field = QDateEdit(self)
        self.date_field.setCalendarPopup(True)
        if self.date:
            self.date_field.setDate(QDate.fromString(self.date, "yyyy-MM-dd"))
        else:
            self.date_field.setDate(QDate.currentDate())
        self.date_field.setDisplayFormat("dd.MM.yyyy")
        self.date_field.setCalendarPopup(True)
        layout.addWidget(self.date_field)

        self.priority_select = QComboBox(self)
        self.priority_select.addItems(["Не задан", "Низкий", "Средний", "Высокий"])
        self.priority_select.setPlaceholderText("Выберите приоритет задачи")
        if self.priority is not None:
            priority_map = {0: "Не задан", 1: "Низкий", 2: "Средний", 3: "Высокий"}
            self.priority_select.setCurrentText(priority_map.get(self.priority, "Не задан"))
        layout.addWidget(self.priority_select)

        # Описание задачи
        self.description_field = QTextEdit(self)
        self.description_field.setFixedHeight(100)
        self.description_field.setStyleSheet("QTextEdit { vertical-align: top; }")
        self.description_field.setPlaceholderText("Введите описание задачи")
        if self.description:
            self.description_field.setText(self.description)
        self.description_field.setAcceptRichText(False)
        layout.addWidget(self.description_field)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel, self
        )

        save_btn = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_btn.setText("Сохранить")

        cancel_btn = self.button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_btn.setText("Отмена")

        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def validate_and_accept(self):
        task_name = self.name_field.text().strip()
        description = self.description_field.toPlainText().strip()
        selected_date = self.date_field.date()
        current_date = QDate.currentDate()

        if not task_name:
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым")
            return

        if len(description) > 5000:
            QMessageBox.warning(self, "Ошибка", "Описание задачи не может превышать 5000 символов. Сейчас у вас " + str(len(description)) + " символов.")
            return

        # Проверяем, что дата не более 100 лет назад
        min_date = current_date.addYears(-100)
        if selected_date < min_date:
            QMessageBox.warning(self, "Ошибка", "Дата не может быть более 100 лет назад")
            return

        # Проверяем, что дата не более 100 лет вперед
        max_date = current_date.addYears(100)
        if selected_date > max_date:
            QMessageBox.warning(self, "Ошибка", "Дата не может быть более 100 лет вперед")
            return

        self.accept()

    def get_task_text(self):
        return self.name_field.text().strip()

    def get_description(self):
        return self.description_field.toPlainText().strip()

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
