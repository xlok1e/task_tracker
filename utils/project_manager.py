import json
from pathlib import Path

class ProjectManager:
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
    
    def remove_task(self, project_id: int, column_id: int, task_id: int) -> bool:
        col = self.get_column(project_id, column_id)
        if col is None:
            return False
        
        for idx, t in enumerate(col["tasks"]):
            if t["id"] == task_id:
                col["tasks"].pop(idx)
                self._save()
                return True
        return False

    def update_task(self, project_id: int, column_id: int, task_id: int, task_name: str, description: str, priority: int, date: str) -> dict | None:
        col = self.get_column(project_id, column_id)
        if col is None:
            return None
        
        for task in col["tasks"]:
            if task["id"] == task_id:
                task["task_name"] = task_name
                task["description"] = description
                task["priority"] = priority
                task["date"] = date
                self._save()
                return task
        return None
    
    def add_project(self, project_name: str) -> dict | None:
        max_id = 0
        for project in self.data:
            if project["id"] > max_id:
                max_id = project["id"]
        new_id = max_id + 1
        project = {"id": new_id, "project_name": project_name, "project_columns": [
            {"id": 1, "column_name": "Backlog", "tasks": []},
            {"id": 2, "column_name": "In Progress", "tasks": []},
            {"id": 3, "column_name": "Done", "tasks": []}
        ]}
        self.data.append(project)
        self._save()
        return project

    def update_project(self, project_id: int, project_name: str) -> dict | None:
        for project in self.data:
            if project["id"] == project_id:
                project["project_name"] = project_name
                self._save()
                return project
        return None
    
    def delete_project(self, project_id: int) -> bool:
        for idx, project in enumerate(self.data):
            if project["id"] == project_id:
                self.data.pop(idx)
                self._save()
                return True
        return False