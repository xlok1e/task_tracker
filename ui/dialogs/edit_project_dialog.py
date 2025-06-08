from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from ui.dialogs.delete_confirmation_dialog import DeleteConfirmationDialog

class EditProjectDialog(QDialog):
    def __init__(self, parent=None, project_name: str = None, project_id: int = None):
        super().__init__(parent)
        self.setWindowTitle('Редактировать проект')
        self.project_name = project_name
        self.project_id = project_id
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

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.open_confirmation_dialog)
        button_layout.addWidget(self.delete_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("edit_button")
        self.save_button.clicked.connect(self.validate_and_accept)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def open_confirmation_dialog(self):
        dialog = DeleteConfirmationDialog(self, "Вы уверены, что хотите удалить проект?", "Проект и все задачи в нем будут удалены безвозвратно")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.parent().task_manager.delete_project(self.project_id)
            
            # Находим индекс текущего проекта
            current_index = -1
            for i, project in enumerate(self.parent().task_manager.data):
                if project["id"] == self.project_id:
                    current_index = i
                    break
            
            # Если есть другие проекты, переключаемся на предыдущий или следующий
            if len(self.parent().task_manager.data) > 0:
                if current_index > 0:
                    self.parent()._switch_project(self.parent().task_manager.data[current_index - 1])
                else:
                    self.parent()._switch_project(self.parent().task_manager.data[0])
            else:
                # Если проектов не осталось, показываем экран без проектов
                self.parent().ui.main_content.setCurrentIndex(1)
            
            self.accept()

    def validate_and_accept(self):
        if not self.name_field.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название проекта не может быть пустым")
            return
        
        if len(self.name_field.text().strip()) > 65:
            QMessageBox.warning(self, "Ошибка", "Название проекта не может превышать 65 символов")
            return
        
        self.project_name = self.name_field.text().strip()
        self.accept()