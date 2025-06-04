from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox, QHBoxLayout, QPushButton, QScrollArea, QWidget
from PySide6.QtCore import Qt

class TaskInfoDialog(QDialog):
    def __init__(self, parent=None, task_name: str = None, description: str = None, priority: int = None, date: str = None):
        super().__init__(parent)
        self.setWindowTitle('Информация о задаче')
        self.setMinimumSize(500, 400)
        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.date = date
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Создаем область прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Создаем виджет-контейнер для содержимого
        content_widget = QWidget()
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
        self.description_label = QLabel(self.description)
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
        self.priority_label = QLabel(self.priority)
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
        self.date_label = QLabel(self.date)
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

        self.setStyleSheet("""
            #task_info_title {
                color: #9CA3AF;
                font-size: 14px;
                font-weight: 500;
            }
            #task_info_label {
                color: white;
                font-size: 16px;
                background-color: transparent;
                padding: 0;
            }
            #edit_button, #delete_button {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                min-width: 100px;
            }
            #edit_button {
                background-color: #3B82F6;
                color: white;
            }
            #delete_button {
                background-color: #EF4444;
                color: white;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #374151;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4B5563;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)