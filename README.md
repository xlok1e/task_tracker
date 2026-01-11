# Task Tracker

A minimalist Kanban-style task management application with project organization.

## About

This project was developed as part of a 2nd year college internship at Vyatka State University college. It demonstrates desktop application development using Python and Qt framework.

## Features

- **Kanban Board**: Organize tasks across three columns (Backlog, To-Do, Done)
- **Multiple Projects**: Create and manage multiple project lists
- **Drag & Drop**: Intuitive task movement between columns
- **Task Management**: Add, edit, and delete tasks with priorities and descriptions
- **Local Storage**: All data stored locally in JSON format
- **Clean UI**: Minimalist, user-friendly interface

## Tech Stack

- **PySide6**: Qt for Python framework for GUI
- **JSON**: Local data persistence
- **Python 3**: Core programming language

## Installation

1. Clone the repository:

```bash
git clone https://github.com/xlok1e/task_tracker.git
cd task_tracker
```

2. Install dependencies:

```bash
pip install PySide6
```

3. Run the application:

```bash
python main.py
```

## Usage

- **Create Project**: Click "Add Project" to create a new task list
- **Add Tasks**: Use the "+" buttons in each column to add tasks
- **Move Tasks**: Drag and drop tasks between columns
- **Edit/Delete**: Click on tasks to edit or remove them
- **Manage Projects**: Click the gear icon to rename or delete projects

## Project Structure

```
task_tracker/
├── models/          # Data storage (JSON files)
├── resources/       # UI resources and stylesheets
│	└── styles.qss   # Stylesheet for UI components
├── ui/              # User interface components
│   ├── dialogs/     # Dialog windows
│   └── resources/   # UI resources and stylesheets
├── utils/           # Utility classes (ProjectManager)
└── main.py          # Application entry point
```
