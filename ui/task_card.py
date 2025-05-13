from PySide6.QtCore import Qt
from PySide6.QtGui import QDrag
from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication

class TaskCard(QWidget):
    def __init__(self, title: str, description: str, priority: int):
            super().__init__()

            print(f"Создаю карточку с приоритетом: {priority}, тип: {type(priority)}")
            self.setObjectName("task_card")
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            self._original_description = description
            self.priority_value = priority

            self.setMinimumWidth(200)
            self.setMaximumHeight(100)

            layout = QVBoxLayout()
            layout.setContentsMargins(20, 20, 15, 15)
            layout.setSpacing(8)

            self.title_label = QLabel(title)
            self.title_label.setObjectName("task_card_title")
            self.title_label.setWordWrap(True)
            self.title_label.setMaximumHeight(40)

            self.priority_label = QLabel(f"Приоритет: {self.getPriority(priority)}")
            self.priority_label.setObjectName("task_card_priority")

            self.description_label = QLabel(description)
            self.description_label.setVisible(False)

            layout.addWidget(self.title_label)
            layout.addWidget(self.priority_label)

            layout.addStretch(1)

            self.setLayout(layout)

            self.setStyleSheet("""
                #task_card {
                    background-color: #374151;
                    color: white;
                    border-radius: 8px;
                }
                QTextEdit {
                    color: white;
                }
            """)

            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setAcceptDrops(False)

    def text(self):
        return self.description_label.text()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.title_label.text())
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.position().toPoint())

        drop_action = drag.exec(Qt.DropAction.MoveAction)

        if drop_action == Qt.DropAction.MoveAction:
            self.hide()

    def getPriority(self, priority_number):
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
