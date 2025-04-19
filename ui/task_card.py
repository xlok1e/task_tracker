from PySide6.QtCore import Qt
from PySide6.QtGui import QDrag
from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QLabel, QApplication

class TaskCard(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignTop)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("task_card")
        self.setAcceptDrops(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)

        drag.setPixmap(self.grab())
        drag.setHotSpot(event.position().toPoint())

        drop_action = drag.exec(Qt.MoveAction)

        if drop_action == Qt.MoveAction:
            self.hide()