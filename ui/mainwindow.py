from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QTextEdit, QApplication, QMessageBox

from ui.dialogs.add_project_dialog import AddProjectDialog
from ui.dialogs.edit_project_dialog import EditProjectDialog
from utils.project_manager import ProjectManager
from .ui_mainwindow import Ui_Form
from .task_card import TaskCard
from .dialogs.add_or_edit_task_dialog import AddOrEditTaskDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Task Manager")

        self.setWindowFlags(Qt.WindowType.Window)
        self.setMinimumSize(1600, 900)
        self.showMaximized()

        self._setup_resizable_layout()

        self.task_manager = ProjectManager("models/main.json")
        self.project = None

        if self.task_manager.data and len(self.task_manager.data) > 0:
            self.project = self.task_manager.data[0]
            self._update_header()
            self.ui.main_content.setCurrentIndex(0)
        else:
            self.ui.main_content.setCurrentIndex(1)

        self._setup_ui()
        self._setup_events()
        self._setup_drag_drop()
        self._populate_projects_list()

        if self.project:
            self._populate_tasks()

    def _setup_resizable_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        menu_widget = QWidget()
        menu_widget.setObjectName("menu")
        menu_widget.setMinimumWidth(250)
        menu_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(24)
        
        top_buttons = QWidget()
        top_buttons_layout = QVBoxLayout(top_buttons)
        top_buttons_layout.setContentsMargins(12, 12, 12, 12)
        top_buttons_layout.setSpacing(8)
        top_buttons_layout.addWidget(self.ui.menu_add_list_btn)
        menu_layout.addWidget(top_buttons)
        
        projects_widget = QWidget()
        projects_layout = QVBoxLayout(projects_widget)
        projects_layout.setContentsMargins(12, 12, 12, 12)
        projects_layout.setSpacing(12)
        
        projects_layout.addWidget(self.ui.my_lists_text)
        
        self.ui.all_lists_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.all_lists_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.all_lists_area.setStyleSheet("QScrollArea { border: none; }")
        self.ui.all_lists_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.ui.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(8)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        projects_layout.addWidget(self.ui.all_lists_area)
        menu_layout.addWidget(projects_widget, 1)
        
        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.ui.main_content)

        project_layout = QVBoxLayout()
        project_layout.setContentsMargins(20, 20, 20, 20)
        project_layout.setSpacing(20)
        self.ui.project_page.setLayout(project_layout)

        project_layout.addWidget(self.ui.layoutWidget2)

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
                card = self.add_task_to_layout(layout, task['task_name'], task['description'], task['priority'], task['date'])
                card.task_id = task['id']
                card.column_id = col_id
        self._update_column_counts()

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

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(self.ui.verticalLayoutWidget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.ui.no_lists_page.setLayout(layout)

        self.ui.no_lists_layout.setSpacing(20)
        
        self.ui.no_lists_layout.insertSpacing(2, 10)

        button_container = QWidget(self.ui.verticalLayoutWidget)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.ui.main_screen_add_project_btn)
        button_layout.addStretch()

        self.ui.no_lists_layout.removeWidget(self.ui.main_screen_add_project_btn)
        self.ui.no_lists_layout.addWidget(button_container)

    def _setup_events(self):
        self.ui.add_task_to_backlog.clicked.connect(self.add_new_task_to_backlog)
        self.ui.add_task_to_inprogress.clicked.connect(self.add_new_task_to_todo)
        self.ui.add_task_to_done.clicked.connect(self.add_new_task_to_done)

        self.ui.edit_list_btn.clicked.connect(self.open_edit_project_dialog)
        self.ui.main_screen_add_project_btn.clicked.connect(self.open_add_project_dialog)
        self.ui.menu_add_list_btn.clicked.connect(self.open_add_project_dialog)

    def _setup_drag_drop(self):
        self.ui.column_backlog.setAcceptDrops(True)
        self.ui.column_todo.setAcceptDrops(True)
        self.ui.column_done.setAcceptDrops(True)

        self.ui.column_backlog.installEventFilter(self)
        self.ui.column_todo.installEventFilter(self)
        self.ui.column_done.installEventFilter(self)

    def add_task_to_layout(self, layout, text: str, description: str, priority: int, date: str):
        task = TaskCard(text, description, priority, date)
        layout.addWidget(task)
        self._update_column_counts()
        return task
    
    def _remove_task_from_layout(self, layout, task_id):
        for widget in layout.children():
            if isinstance(widget, TaskCard) and widget.task_id == task_id:
                widget.setParent(None)
                widget.deleteLater()
                return True
        self._update_column_counts()
        return False

    def remove_task(self, task_id, column_id):
        removed = self.task_manager.remove_task(self.project["id"], column_id, task_id)
        if removed:
            column = None
            if column_id == 1:
                column = self.ui.column_backlog
            elif column_id == 2:
                column = self.ui.column_todo
            elif column_id == 3:
                column = self.ui.column_done

            if column:
                layout = column.layout()
                if layout:
                    while layout.count():
                        item = layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()
                    
                    for task in self.task_manager.get_column(self.project["id"], column_id)["tasks"]:
                        card = self.add_task_to_layout(layout, task["task_name"], task["description"], task["priority"], task["date"])
                        card.task_id = task["id"]
                        card.column_id = column_id
                    
                    layout.update()
                    column.update()
                    self.update()

    def add_new_task_to_backlog(self):
        self._add_new_task(self.backlog_layout, column_id=1)

    def add_new_task_to_todo(self):
        self._add_new_task(self.todo_layout, column_id=2)

    def add_new_task_to_done(self):
        self._add_new_task(self.done_layout, column_id=3)

    def _add_new_task(self, layout, column_id: int):
        dialog = AddOrEditTaskDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        text = dialog.get_task_text().strip()
        description = dialog.get_description()
        priority = dialog.get_priority()
        date = dialog.get_date()
        print(f"Добавляем задачу с приоритетом: {priority}")

        if not text:
            return

        new_task = self.task_manager.add_task(
            self.project["id"],
            column_id,
            text,
            description,
            priority,
            date
        )

        card = self.add_task_to_layout(layout, new_task["task_name"], new_task["description"], new_task["priority"], new_task["date"])
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
            if moved:
                self._update_column_counts()

            target_layout = self._get_layout_by_column_id(target_column)
            new_card = self.add_task_to_layout(
                target_layout,
                source_card.title_label.text(),
                source_card.description_label.toPlainText() if hasattr(source_card.description_label, 'toPlainText') else source_card.description_label.text(),
                self._get_priority_number(source_card.priority_label.text()),
                source_card.date_label.text()
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

    def open_edit_project_dialog(self):
        dialog = EditProjectDialog(self, self.project["project_name"], self.project["id"])

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = dialog.name_field.text().strip()
            if new_name:
                self.project["project_name"] = new_name
                self.task_manager.update_project(self.project["id"], new_name)
                self._update_header()

    def open_add_project_dialog(self):
        dialog = AddProjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = dialog.project_name
            if new_name:
                self.task_manager.add_project(new_name)
                self._populate_projects_list()
                self._switch_project(self.task_manager.data[-1])

    def _populate_projects_list(self):
        if not self.ui.scrollAreaWidgetContents.layout():
            layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
            layout.setSpacing(8)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        else:
            layout = self.ui.scrollAreaWidgetContents.layout()
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        for project in self.task_manager.data:
            btn = QPushButton(project["project_name"][:20] + "..." if len(project["project_name"]) > 20 else project["project_name"])
            btn.setObjectName(f"project_btn_{project['id']}")
            btn.setProperty("project_id", project["id"])
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, p=project: self._switch_project(p))
            
            is_selected = project["id"] == self.project["id"]
            btn.setProperty("is_selected", is_selected)
            btn.setStyleSheet(self._get_project_button_style(is_selected))
            layout.addWidget(btn)

    def _get_project_button_style(self, is_selected):
        base_style = """
            QPushButton {
                text-align: left;
                padding-left: 8px;
                border: none;
                border-radius: 8px;
                height: 40px;
            }
        """
        
        if is_selected:
            return base_style + """
                QPushButton {
                    background-color: #4f46e5;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    height: 40px;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
            """
        else:
            return base_style + """
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #4b5563;
                    height: 40px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #374151;
                    color: white;
                }
            """
        
    def _update_column_counts(self):
        counts = {col['id']: len(col.get('tasks', [])) for col in self.project['project_columns']}

        self.ui.backlog_text.setText(f"BACKLOG ({counts.get(1, 0)})")
        self.ui.inprogress_text.setText(f"TODO ({counts.get(2, 0)})")
        self.ui.done_text_3.setText(f"DONE ({counts.get(3, 0)})")    

    def _switch_project(self, project):
        self.project = project
        self._update_header()
        self._clear_all_columns()
        self._populate_tasks()
        self._populate_projects_list()
        self.ui.main_content.setCurrentIndex(0)

    def _clear_all_columns(self):
        for layout in [self.backlog_layout, self.todo_layout, self.done_layout]:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()