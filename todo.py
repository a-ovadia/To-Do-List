# individual task in ToDoList class
class Task:
    task_id = 1

    def __init__(self, description, deadline = None, status = "Not Started", priority = "Low"):
        self.description = description
        self.deadline = deadline
        self.status = status
        self.priority = priority
        self.id = Task.task_id
        Task.task_id += 1
    
    def set_description(self, desc):
        self.description = desc

    def set_deadline(self, date):
        self.deadline = date
    
    def set_status(self, status):
        self.status = status

    def set_priority(self, priority):
        self.priority = priority

    def get_task_id(self): return self.id

class ToDoList:

    ToDo = []

    def __init__(self): print("h")

    # Add a new task
    def add_task(self, new_task : Task):
        self.ToDo.append(new_task)

    # Remove task from list
    def remove_task(self, remove_task : Task): print("hg")




class UserInterface:

    def __init__():
        print("Main Menu")

    
    def display_main_menu(self):
        print("1. View all tasks")