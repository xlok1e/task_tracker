from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog

from .ui_mainwindow import Ui_Form
from .task_card import TaskCard
from .dialogs import AddTaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_events()
        self._setup_drag_drop()

    def _setup_ui(self):
        for button in self.findChildren(QPushButton):
            button.setCursor(Qt.PointingHandCursor)

        self.ui.column_backlog.setLayout(self.ui.layout_backlog)
        self.ui.column_todo.setLayout(self.ui.layout_todo)
        self.ui.column_done.setLayout(self.ui.layout_done)

        self.backlog_layout = self.ui.layout_backlog
        self.todo_layout = self.ui.layout_todo
        self.done_layout = self.ui.layout_done

        self.backlog_layout.setAlignment(Qt.AlignTop)
        self.todo_layout.setAlignment(Qt.AlignTop)
        self.done_layout.setAlignment(Qt.AlignTop)

    def _setup_events(self):
        self.ui.add_task_to_backlog.clicked.connect(self.add_new_task_to_backlog)
        self.ui.add_task_to_inprogress.clicked.connect(self.add_new_task_to_todo)
        self.ui.add_task_to_done.clicked.connect(self.add_new_task_to_done)

    def _setup_drag_drop(self):
        self.ui.column_backlog.setAcceptDrops(True)
        self.ui.column_todo.setAcceptDrops(True)
        self.ui.column_done.setAcceptDrops(True)

        self.ui.column_backlog.installEventFilter(self)
        self.ui.column_todo.installEventFilter(self)
        self.ui.column_done.installEventFilter(self)

    def add_task_to_layout(self, layout, text: str):
        task = TaskCard(text)
        layout.addWidget(task)
        return task

    def add_new_task_to_backlog(self):
        self._add_new_task(self.backlog_layout)

    def add_new_task_to_todo(self):
        self._add_new_task(self.todo_layout)

    def add_new_task_to_done(self):
        self._add_new_task(self.done_layout)

    def _add_new_task(self, layout):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.Accepted:
            task_text = dialog.get_task_text().strip()
            if task_text:
                self.add_task_to_layout(layout, task_text)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.DragEnter:
            if event.mimeData().hasText():
                event.acceptProposedAction()
                return True

        elif event.type() == QEvent.Drop:
            if event.mimeData().hasText():
                task_text = event.mimeData().text()

                target_layout = self._get_target_layout(watched)

                if target_layout:
                    self.add_task_to_layout(target_layout, task_text)
                    self._remove_source_card(event)

                    event.acceptProposedAction()
                    return True

        return super().eventFilter(watched, event)

    def _get_target_layout(self, watched):
        if watched == self.ui.column_backlog:
            return self.backlog_layout
        elif watched == self.ui.column_todo:
            return self.todo_layout
        elif watched == self.ui.column_done:
            return self.done_layout
        return None

    def _remove_source_card(self, event):
        source_widget = event.source()
        if source_widget and isinstance(source_widget, TaskCard):
            parent_layout = source_widget.parent().layout()
            if parent_layout:
                parent_layout.removeWidget(source_widget)
                source_widget.deleteLater()