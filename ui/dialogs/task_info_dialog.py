from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox, QHBoxLayout, QPushButton, QScrollArea, QWidget, QMainWindow
from PySide6.QtCore import Qt
from ui.dialogs.add_or_edit_task_dialog import AddOrEditTaskDialog
from ui.dialogs.delete_confirmation_dialog import DeleteConfirmationDialog

class TaskInfoDialog(QDialog):
    def __init__(self, parent=None, task_name: str = None, description: str = None, priority: int = None, date: str = None, task_id: int = None, column_id: int = None):
        super().__init__(parent)
        self.setWindowTitle('Информация о задаче')
        self.setMinimumSize(500, 400)
        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.date = date
        self.task_id = task_id
        self.column_id = column_id
        self.init_ui()

    def get_priority_text(self, priority_number):
        match priority_number:
            case 1:
                return "Низкий"
            case 2:
                return "Средний"
            case 3:
                return "Высокий"
            case 0:
                return "Не задан"
            case _:
                return "Не задан"

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_widget.setObjectName("content_widget")
        layout = QVBoxLayout(content_widget)
        field_layout = QVBoxLayout()
        field_layout.setSpacing(20)

        # Название
        name_group = QVBoxLayout()
        name_group.setSpacing(4)
        self.name_title = QLabel("Название задачи:")
        self.name_label = QLabel(self.task_name)
        self.name_label.setWordWrap(True)
        self.name_title.setObjectName("task_info_title")
        self.name_label.setObjectName("task_info_label")
        name_group.addWidget(self.name_title)
        name_group.addWidget(self.name_label)
        field_layout.addLayout(name_group)

        # Описание
        desc_group = QVBoxLayout()
        desc_group.setSpacing(4)
        self.description_title = QLabel("Описание задачи:")
        self.description_label = QLabel(self.description or "Описание не задано")
        self.description_label.setWordWrap(True)
        self.description_title.setObjectName("task_info_title")
        self.description_label.setObjectName("task_info_label")
        desc_group.addWidget(self.description_title)
        desc_group.addWidget(self.description_label)
        field_layout.addLayout(desc_group)

        # Приоритет
        priority_group = QVBoxLayout()
        priority_group.setSpacing(4)
        self.priority_title = QLabel("Приоритет:")
        self.priority_label = QLabel(self.get_priority_text(self.priority))
        self.priority_label.setWordWrap(True)
        self.priority_title.setObjectName("task_info_title")
        self.priority_label.setObjectName("task_info_label")
        priority_group.addWidget(self.priority_title)
        priority_group.addWidget(self.priority_label)
        field_layout.addLayout(priority_group)

        # Дата
        date_group = QVBoxLayout()
        date_group.setSpacing(4)
        self.date_title = QLabel("Дата:")
        self.date_label = QLabel(self.date or "Дата не задана")
        self.date_label.setWordWrap(True)
        self.date_title.setObjectName("task_info_title")
        self.date_label.setObjectName("task_info_label")
        date_group.addWidget(self.date_title)
        date_group.addWidget(self.date_label)
        field_layout.addLayout(date_group)

        layout.addLayout(field_layout)
        layout.addStretch()

        # Устанавливаем виджет-контейнер в область прокрутки
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Кнопки управления
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)        
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        
        self.edit_button.setObjectName("edit_button")
        self.delete_button.setObjectName("delete_button")
        
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(button_layout)

        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)

    def edit_task(self):
        from ui.task_card import TaskCard
        
        dialog = AddOrEditTaskDialog(
            self,
            task_name=self.task_name,
            description=self.description,
            priority=self.priority,
            date=self.date,
            task_id=self.task_id,
            column_id=self.column_id
        )
        
        if dialog.exec():
            # Получаем главное окно
            main_window = self.parent()
            while main_window and not isinstance(main_window, QMainWindow):
                main_window = main_window.parent()
            
            if main_window:
                # Обновляем задачу через TaskManager
                updated_task = main_window.task_manager.update_task(
                    main_window.project["id"],
                    self.column_id,
                    self.task_id,
                    dialog.get_task_text(),
                    dialog.get_description(),
                    dialog.get_priority(),
                    dialog.get_date()
                )
                
                if updated_task:
                    # Обновляем отображение задачи
                    layout = main_window._get_layout_by_column_id(self.column_id)
                    if layout:
                        # Находим и обновляем существующую карточку
                        for i in range(layout.count()):
                            widget = layout.itemAt(i).widget()
                            if isinstance(widget, TaskCard) and widget.task_id == self.task_id:
                                # Обновляем данные карточки
                                widget._original_title = updated_task["task_name"]
                                widget._original_description = updated_task["description"]
                                widget.priority_value = updated_task["priority"]
                                widget.date_value = updated_task["date"]
                                
                                # Обновляем отображение
                                widget.title_label.setText(widget._trim_text(updated_task["task_name"], 30))
                                widget.description_label.setText(widget._trim_text(updated_task["description"] or 'Описание не задано', 60))
                                widget.priority_label.setText(widget.getPriority(updated_task["priority"]))
                                widget.priority_label.setStyleSheet(f"""
                                    background-color: {widget.getPriorityColor(updated_task["priority"])};
                                    max-height: 24px;
                                    min-height: 24px;
                                    border-radius: 4px;
                                    padding: 0 2px;
                                    margin-left: auto;
                                """)
                                widget.date_label.setText(widget.get_date_format(updated_task["date"]))
                                break
                    
                    self.close()

    def delete_task(self):
        dialog = DeleteConfirmationDialog(self, "Вы уверены, что хотите удалить эту задачу?", "После подтверждения, задача будет удалена безвозвратно.")
        
        if dialog.exec():
            # Получаем главное окно и вызываем метод удаления
            main_window = self.parent()
            while main_window and not isinstance(main_window, QMainWindow):
                main_window = main_window.parent()
            
            if main_window:
                main_window.remove_task(self.task_id, self.column_id)
            self.close()