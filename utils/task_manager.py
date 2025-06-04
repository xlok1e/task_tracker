import json
from pathlib import Path

class TaskManager:
    def __init__(self, json_path: str):
        self.json_file = Path(json_path)

        # Храним все данные из проекта
        self.data = []

        self._load()

    def _load(self):
        if self.json_file.exists():
            with self.json_file.open('r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = []
            self._save()

    def _save(self):
            with self.json_file.open('w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_project(self, project_id: int) -> dict | None:
        for project in self.data:
            if project['id'] == project_id:
                return project
        return None

    def get_column(self, project_id: int, column_id: int) -> dict | None:
        project = self.get_project(project_id)
        if project is None:
            return None

        for column in project["project_columns"]:
            if column["id"] == column_id:
                return column
        return None

    def add_task(self, project_id: int, column_id: int, task_name: str, description: str, priority: int, date: str):
        col = self.get_column(project_id, column_id)

        if col is None:
            raise ValueError(f"Колонка {column_id} в проекте {project_id} не найдена")

        max_id = 0
        for proj in self.data:
            for c in proj["project_columns"]:
                for t in c["tasks"]:
                    if t["id"] > max_id:
                        max_id = t["id"]
        new_id = max_id + 1

        task = {"id": new_id, "task_name": task_name, "description": description, "priority": priority, "date": date}
        col['tasks'].append(task)
        self._save()
        return task

    def move_task(self, project_id: int, source_column_id: int, target_column_id: int, task_id: int) -> bool:
        source = self.get_column(project_id, source_column_id)
        target = self.get_column(project_id, target_column_id)

        if source is None or target is None:
            return False

        for idx, t in enumerate(source["tasks"]):
            if t["id"] == task_id:
                task = source["tasks"].pop(idx)
                target["tasks"].append(task)
                self._save()
                return True
        return False
