from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog

from utils.task_manager import TaskManager
from .ui_mainwindow import Ui_Form
from .task_card import TaskCard
from .dialogs import AddTaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.task_manager = TaskManager("models/main.json")

        if self.task_manager.data:
            self.project = self.task_manager.data[0]
            self._update_header()
        else:
            # todo Тут надо выводить экран без проектов
            print('No projects')

        print("Loading JSON from:", self.task_manager.json_file.resolve())
        print("Loaded data:", self.task_manager.data)

        self._setup_ui()
        self._setup_events()
        self._setup_drag_drop()

        self._populate_tasks()

    def _update_header(self):
        name = self.project.get("project_name", "Без имени")
        self.ui.list_name_text.setText(name)

    def _populate_tasks(self):
        for col in self.project['project_columns']:
            col_id = col['id']

            layout = self._get_layout_by_column_id(col_id)
            if layout is None:
                continue

            for task in col['tasks']:
                card = self.add_task_to_layout(layout, task['task_name'])
                card.task_id = task['id']
                card.column_id = col_id

    def _get_layout_by_column_id(self, col_id):
        if col_id == 1:
            return self.ui.layout_backlog
        elif col_id == 2:
            return self.ui.layout_todo
        elif col_id == 3:
            return self.ui.layout_done
        else:
            return None


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
        self._add_new_task(self.backlog_layout, column_id=1)

    def add_new_task_to_todo(self):
        self._add_new_task(self.todo_layout, column_id=2)

    def add_new_task_to_done(self):
        self._add_new_task(self.done_layout, column_id=3)

    def _add_new_task(self, layout, column_id: int):
        dialog = AddTaskDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return
        text = dialog.get_task_text().strip()
        if not text:
            return

        new_task = self.task_manager.add_task(
            self.project["id"],
            column_id,
            text
        )

        card = self.add_task_to_layout(layout, new_task["task_name"])
        card.task_id = new_task["id"]
        card.column_id = column_id

    def _get_column_id_by_watched(self, watched):
        if watched == self.ui.column_backlog:
            return 1
        if watched == self.ui.column_todo:
            return 2
        if watched == self.ui.column_done:
            return 3
        return None


    def eventFilter(self, watched, event):
        if event.type() == QEvent.DragEnter:
            if event.mimeData().hasText():
                event.acceptProposedAction()
                return True

        elif event.type() == QEvent.Drop:
            if event.mimeData().hasText():
                task_text = event.mimeData().text()

        if event.type() == QEvent.Drop and event.mimeData().hasText():
            source_card = event.source()
            target_column = self._get_column_id_by_watched(watched)
            source_column = getattr(source_card, "column_id", None)
            if not isinstance(source_card, TaskCard) or target_column is None or source_column is None:
                return super().eventFilter(watched, event)

            moved = self.task_manager.move_task(
                self.project["id"],
                source_column,
                target_column,
                source_card.task_id
            )
            if not moved:
                return super().eventFilter(watched, event)

            target_layout = self._get_layout_by_column_id(target_column)
            new_card = self.add_task_to_layout(target_layout, source_card.text())
            new_card.task_id = source_card.task_id
            new_card.column_id = target_column

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