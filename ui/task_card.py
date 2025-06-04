from PySide6.QtCore import Qt
from PySide6.QtGui import QDrag
from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QSizePolicy
from ui.dialogs.task_info_dialog import TaskInfoDialog

class TaskCard(QWidget):
    def __init__(self, title: str, description: str, priority: int, date: str):
            super().__init__()

            self.setObjectName("task_card")
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            self._original_description = description
            self._original_title = title
            self.priority_value = priority
            self.date_value = date
            self.setMinimumWidth(200)
            self.setMaximumHeight(100)
            self.is_dragging = False

            layout = QVBoxLayout()
            layout.setContentsMargins(25, 25, 25, 20)

            header_layout = QHBoxLayout()
            header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            header_layout.setContentsMargins(0, 0, 0, 0)

            short_title = self._trim_text(title, 30)
            self.title_label = QLabel(short_title)
            self.title_label.setObjectName("task_card_title")
            self.title_label.setWordWrap(False)

            self.priority_label = QLabel(f"{self.getPriority(priority)}")
            self.priority_label.setObjectName("task_card_priority")
            self.priority_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            self.priority_label.setStyleSheet(f"""
                background-color: {self.getPriorityColor(priority)};
                max-height: 24px;
                min-height: 24px;
                border-radius: 4px;
                padding: 0 2px;
                margin-left: auto;
            """)

            self.date_label = QLabel(self.get_date_format(date))
            self.date_label.setObjectName("task_card_date")
            self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            self.date_label.setStyleSheet("""
                color: #9CA3AF;
            """)

            header_layout.addWidget(self.title_label)
            header_layout.addStretch(1)
            header_layout.addWidget(self.priority_label)           

            short_description = self._trim_text(description, 65)
            self.description_label = QTextEdit(short_description or 'Описание не задано')
            self.description_label.setObjectName("task_card_description")
            self.description_label.setReadOnly(True)
            self.description_label.setFrameShape(QTextEdit.Shape.NoFrame)
            self.description_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self.description_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.description_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.description_label.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.description_label.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.description_label.document().setDocumentMargin(0)
            size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.description_label.setSizePolicy(size_policy)

            layout.addLayout(header_layout)
            layout.addWidget(self.description_label)
            layout.addWidget(self.date_label)
            layout.addStretch(1)

            self.setLayout(layout)

            self.setStyleSheet("""
                #task_card {
                    background-color: #374151;
                    color: white;
                    border-radius: 8px;
                }
                #task_card_description {
                    color: #9CA3AF;
                    font-weight: 500;
                    font-size: 14px;
                    background-color: transparent;
                    padding: 0;
                    margin-top: 4px;
                    border: none;
                }
                QTextEdit {
                    color: white;
                }
            """)

            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setAcceptDrops(False)
            # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            # self.customContextMenuRequested.connect(self.show_task_info)

    def text(self):
        return self._original_description

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        self.is_dragging = True
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.title_label.text())
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.position().toPoint())

        drop_action = drag.exec(Qt.DropAction.MoveAction)

        if drop_action == Qt.DropAction.MoveAction:
            self.hide()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_dragging:
            self.show_task_info()

    def _trim_text(self, text, max_length=100):
            if len(text) <= max_length:
                return text
            return text[:max_length] + "..."

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

    def getPriorityColor(self, priority_number):
        match priority_number:
            case 1:
                return "#10B981"
            case 2:
                return "#F59E0B"
            case 3:
                return "#EF4444"
            case 0:
                return "#9E9E9E"
            case _:
                return "#9E9E9E"

    def get_date_format(self, date):
        if not date:
            return "Дата не задана"
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            months = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            return f"До {date_obj.day} {months[date_obj.month]} {date_obj.year}"
        except:
            return date
        
    def show_task_info(self):
        dialog = TaskInfoDialog(self, self._original_title, self._original_description, self.priority_label.text(), self.date_label.text())
        dialog.exec()