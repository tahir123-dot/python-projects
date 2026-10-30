
import json
from pathlib import Path


# ==========================================
# FILE PATH
# ==========================================

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"


# ==========================================
# LOAD TASKS
# ==========================================

def load_tasks():
    """Load tasks from JSON file."""

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

            if not isinstance(tasks, list):
                print("Invalid data format. Starting with empty tasks.")
                return []

            return tasks

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Warning: JSON file is corrupted. Starting with empty tasks.")
        return []

    except PermissionError:
        print("Error: Permission denied while reading tasks.")
        return []


# ==========================================
# SAVE TASKS
# ==========================================

def save_tasks(tasks):
    """Save tasks into JSON file."""

    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving tasks: {error}")
        return False


# ==========================================
# ADD TASK
# ==========================================

def add_task(tasks):
    """Add a new task."""

    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty!")
        return

    # Check duplicate tasks
    for task in tasks:
        if task["title"].casefold() == title.casefold():
            print("This task already exists!")
            return

    new_task = {
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    if save_tasks(tasks):
        print("Task added successfully!")


# ==========================================
# SHOW TASKS
# ==========================================

def show_tasks(tasks):
    """Display all tasks."""

    if not tasks:
        print("\nNo tasks available!")
        return

    print("\n========== YOUR TASKS ==========")

    for index, task in enumerate(tasks, start=1):

        status = "Done" if task["done"] else "Pending"

        print(f"{index}. {task['title']} [{status}]")

    print("================================")


# ==========================================
# GET TASK NUMBER
# ==========================================

def get_task_number(tasks):
    """Get and validate task number."""

    if not tasks:
        print("No tasks available!")
        return None

    try:
        number = int(input("Enter task number: ").strip())

        if number < 1 or number > len(tasks):
            print("Invalid task number!")
            return None

        # Convert user number into list index
        return number - 1

    except ValueError:
        print("Please enter a valid number!")
        return None


# ==========================================
# COMPLETE TASK
# ==========================================

def complete_task(tasks):
    """Mark a task as completed."""

    show_tasks(tasks)

    index = get_task_number(tasks)

    if index is None:
        return

    if tasks[index]["done"]:
        print("This task is already completed!")
        return

    tasks[index]["done"] = True

    if save_tasks(tasks):
        print("Task completed successfully!")


# ==========================================
# DELETE TASK
# ==========================================

def delete_task(tasks):
    """Delete a task."""

    show_tasks(tasks)

    index = get_task_number(tasks)

    if index is None:
        return

    deleted_task = tasks.pop(index)

    if save_tasks(tasks):
        print(f"Task '{deleted_task['title']}' deleted successfully!")


# ==========================================
# MENU FUNCTIONS
# ==========================================

def exit_program(tasks):
    """Exit the application."""

    print("Thank you for using Todo List!")
    return False


# Dictionary + Function pattern

menu_options = {
    "1": add_task,
    "2": show_tasks,
    "3": complete_task,
    "4": delete_task,
    "5": exit_program
}


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    tasks = load_tasks()

    print("\nWelcome to Python Todo List!")

    while True:

        print("\n========== TODO MENU ==========")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        print("================================")

        choice = input("Choose an option (1-5): ").strip()

        selected_function = menu_options.get(choice)

        if selected_function is None:
            print("Invalid option! Please choose 1-5.")
            continue

        if choice == "5":
            selected_function(tasks)
            break

        selected_function(tasks)


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
