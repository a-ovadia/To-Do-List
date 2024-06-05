import datetime as dt

# individual Task
class Task:
    task_id = 1

    def __init__(self, description, deadline = None, status = "Not Started", priority = "Low"):
        self.description = description
        self.deadline = deadline
        self.status = status
        
        # convert priority to int values
        if priority.lower() == "low":
            self.priority = 3
        elif priority.lower() == "medium":
            self.priority = 2
        elif priority.lower() == "high":
            self.priority = 1

        # Set Task ID
        self.id = Task.task_id
        # Incrament Task ID
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

    def change_status(self, new_status):
        self.status = new_status

# holds the actual data -> List of Tasks
class ToDoList: 

    def __init__(self):
        self.tasks = []

    # Add a new task
    def add_task(self, new_task : Task):
        self.tasks.append(new_task)

    # Remove task from list
    def remove_task(self, remove_task_id : int):
        for task in self.tasks:
            if task.id == remove_task_id:
                self.tasks.remove(task)
        """
            Need to handle errors
        """

    def view_tasks(self):
        return


# Menu for user management of ToDoList
# Is a user interface to interact with the ToDoList
class UserInterface:

    def __init__(self, todo_list : ToDoList):
        self.todo_list = todo_list

    def add_new_task(self):
        task_desciption = input("Enter task Description\n")
        deadline_str = input("Enter deadline in (mm/dd/yyyy hh:mm) format: ")
        # convert deadline_str into a datetime format
        task_status = input("Enter status (not started or in progress): ")
        task_priority = input("Enter priority (low or medium or high)")
        # Create new Task obj
        new_task = Task(task_desciption, deadline_str, task_status, task_priority)
        # Add Task to ToDoList
        self.todo_list.add_task(new_task)
        self.view_tasks()

    


    def display_main_menu(self):
        print("1. Add a new Task")
        print("2. View all Tasks")

        if input() == "2":
            self.todo_list.view_tasks()

my_list = ToDoList()
ui = UserInterface(my_list)
ui.display_main_menu()