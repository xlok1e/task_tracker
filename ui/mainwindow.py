from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QTextEdit

from utils.task_manager import TaskManager
from .ui_mainwindow import Ui_Form
from .task_card import TaskCard
from .dialogs import AddTaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.WindowType.Window)
        self.setMinimumSize(1600, 900)

        self._setup_resizable_layout()

        self.task_manager = TaskManager("models/main.json")

        if self.task_manager.data:
            self.project = self.task_manager.data[0]
            self._update_header()
        else:
            # todo Тут надо выводить экран без проектов
            print('No projects')

        self._setup_ui()
        self._setup_events()
        self._setup_drag_drop()

        self._populate_tasks()

    def _setup_resizable_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.ui.menu)
        main_layout.addWidget(self.ui.main_content)

        project_layout = QVBoxLayout()
        project_layout.setContentsMargins(20, 20, 20, 20)
        project_layout.setSpacing(20)
        self.ui.project_page.setLayout(project_layout)

        project_layout.addWidget(self.ui.widget)

        board_container = QWidget()
        board_container.setLayout(self.ui.layout_board)
        project_layout.addWidget(board_container)

        self.ui.backlog.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.todo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.done.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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
                    card = self.add_task_to_layout(layout, task['task_name'], task['description'], task['priority'])
                    setattr(card, 'task_id', task['id'])
                    setattr(card, 'column_id', col_id)

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
            button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.ui.column_backlog.setLayout(self.ui.layout_backlog)
        self.ui.column_todo.setLayout(self.ui.layout_todo)
        self.ui.column_done.setLayout(self.ui.layout_done)

        self.backlog_layout = self.ui.layout_backlog
        self.todo_layout = self.ui.layout_todo
        self.done_layout = self.ui.layout_done

        self.backlog_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.todo_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.done_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

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

    def add_task_to_layout(self, layout, text: str, description: str, priority: int):
        task = TaskCard(text, description, priority)
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

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        text = dialog.get_task_text().strip()
        description = dialog.get_description()
        priority = dialog.get_priority()

        print(f"Добавляем задачу с приоритетом: {priority}")

        if not text:
            return

        new_task = self.task_manager.add_task(
            self.project["id"],
            column_id,
            text,
            description,
            priority
        )

        print(f"Задача добавлена с приоритетом: {new_task['priority']}")
        card = self.add_task_to_layout(layout, new_task["task_name"], new_task["description"], new_task["priority"])
        setattr(card, 'task_id', new_task["id"])
        setattr(card, 'column_id', column_id)

    def _get_column_id_by_watched(self, watched):
        if watched == self.ui.column_backlog:
            return 1
        if watched == self.ui.column_todo:
            return 2
        if watched == self.ui.column_done:
            return 3
        return None


    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasText():
                event.acceptProposedAction()
                return True

        elif event.type() == QEvent.Type.Drop:
            if event.mimeData().hasText():
                pass

        if event.type() == QEvent.Type.Drop and event.mimeData().hasText():
            source_card = event.source()
            target_column = self._get_column_id_by_watched(watched)
            source_column = getattr(source_card, "column_id", None)
            if not isinstance(source_card, TaskCard) or target_column is None or source_column is None:
                return super().eventFilter(watched, event)

            moved = self.task_manager.move_task(
                self.project["id"],
                source_column,
                target_column,
                getattr(source_card, 'task_id')
            )
            if not moved:
                return super().eventFilter(watched, event)

            target_layout = self._get_layout_by_column_id(target_column)
            new_card = self.add_task_to_layout(
                target_layout,
                source_card.title_label.text(),
                source_card.description_label.toPlainText() if hasattr(source_card.description_label, 'toPlainText') else source_card.description_label.text(),
                self._get_priority_number(source_card.priority_label.text())
            )
            setattr(new_card, 'task_id', getattr(source_card, 'task_id'))
            setattr(new_card, 'column_id', target_column)

            self._remove_source_card(event)

            event.acceptProposedAction()
            return True

        return super().eventFilter(watched, event)

    def _get_priority_number(self, priority_text):
        priority_map = {
            "Низкий": 1,
            "Средний": 2,
            "Высокий": 3,
            "Не задан": 0
        }
        return priority_map.get(priority_text, 0)

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
                parent = source_widget.parent()
                if parent:
                    layout = parent.layout()
                    if layout:
                        layout.removeWidget(source_widget)
                        source_widget.deleteLater()
