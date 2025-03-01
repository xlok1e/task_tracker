import json
import keyboard


def get_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

        return data


def display_project_columns(project_id):
    all_projects = get_json("main.json")

    for project in all_projects:
        if project["id"] == project_id:
            for column in project["project_columns"]:
                print(f"{column['column_name']}")

                for task in column["tasks"]:
                    print('   ' + task["task_name"])

                print()

            print("Нажмите 'B' для возврата назад")

            while True:
                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_DOWN and event.name.lower() == 'b':
                    display_projects()
                    return


def display_projects():
    all_projects = get_json("main.json")

    if not all_projects:
        print("No projects found")
    else:
        print('Мои проекты:')
        for index, project in enumerate(all_projects, start=1):
            print(f"{index}. {project['project_name']}")

    while True:
        event = keyboard.read_event(suppress=True)

        if event.event_type == keyboard.KEY_DOWN and event.name.isdigit():

            project_index = int(event.name) - 1
            project_id = all_projects[project_index]["id"]

            display_project_columns(project_id)
            return


display_projects()
