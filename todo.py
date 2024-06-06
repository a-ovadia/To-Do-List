import datetime as dt
import sys
import csv
## TODO Store data in a CSV file instead of List

# individual Task
class Task:
    task_id = 1

    # Constructor
    def __init__(self, description, deadline = None, status = "Not Started", priority = "Low"):
        """
        Represents a task with a description, deadline, staus, and priority
        Args:
        description -- (str) Description of task
        deadline -- (datetime) Deadline of task
        status -- (str) status of task
        priority -- (str) - priority of task
        
        """
        self.description = description
        self.deadline = deadline
        self.status = status
        self.date_added = dt.datetime.now()
        
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
    
    # define print statement for Task class
    def __repr__(self) -> str:
        """
        Define how Task obj should be represented
        Args:
        self
        """
        return f"Task ID: {self.id}\t Description: {self.description}\t Deadline: {self.deadline}\t Status: {self.status}\t Priority: {self.priority}"

    def set_description(self, desc):
        """
        Sets the task description
        Args:
        desc --  (str) new task description
        """

        self.description = desc

    def set_deadline(self, date):
        """
        Sets the task deadline
        Args:
        date -- (datetime) new task deadline
        """

        self.deadline = date
    
    def set_status(self, status):
        """
        Sets the task status 
        Args:
        status -- (str) new task status
        """

        self.status = status

    def set_priority(self, priority):
        """
        Sets the task priority
        Args:
        priority -- (str) new task priority
        """

        self.priority = priority

    def get_task_id(self): 
        """Returns the ID of the task""" 
        return self.id
     

    def change_status(self, new_status):
        """
        Sets the task status
        Args:
        new_status -- (str) new task status
        """
        self.status = new_status


# holds the actual data -> List of Tasks
class ToDoList: 

    def __init__(self):
        self.tasks = []
    """
    Represents a collection of Tasks objects
    """
   
    # Add a new task
    def add_task(self, new_task : Task):
        """
        Adds a new Task to the Tasks list
        Args:
        new_task -- (Task) New Task
        """
        self.tasks.append(new_task)

    # Remove task from list
    def remove_task(self, remove_task_id : int):
        """
        Remove a task from the Tasks list
        Args:
        remove_task_id -- (int) remove task with the ID from Tasks list
        """

        for task in self.tasks:
            if task.id == remove_task_id:
                self.tasks.remove(task)
                return True
        return False
       

    def view_tasks(self):
        """
        Output to terminal a list of all Tasks in the Task list
        """
        for task in self.tasks:
            print(task)

    def validate_task_id(self, task_id):
        """
        Check if an ID is in the Tasks list
        Args:
        task_id -- (int) return true if task_id matches an element in the Tasks list, False otherwise
        """
        for task in self.tasks:
            if task_id == task.id:
                return True
        return False
    
    def get_task(self, task_id : int):
        """
        Returns a Task from a Task ID
        Args:
        task_id -- (int) Return Task from Task lists matching number. Otherwise return False
        """
        for task in self.tasks:
            if task.id == task_id:
                return task 
        return False
    

    
    def update_task(self, task_id, update_desc="", update_deadline = "", update_status = "", update_priority = ""):

        """
        Update an existing Task in Tasks list with new task data
        Args:
        task_id -- (int) Represents which task to update
        update_desc -- (str) new task description
        update_deadline -- (datetime) new task deadline
        update_status -- (str) new task status
        update_priority -- (str) new task priority
        """

        # Validate task_id
        if not self.validate_task_id(task_id):
            return False
        task = self.get_task(task_id)

        if update_desc != "":
            task.set_description(update_desc)
        if update_deadline != "":
            task.set_deadline(update_deadline)
        if update_status != "":
            task.set_status(update_status)
        if update_priority != "":
            task.set_priority(update_priority)
        return True

# Menu for user management of ToDoList
# Is a user interface to interact with the ToDoList
class UserInterface:
    

    def __init__(self, todo_list : ToDoList):
        """
        Represents an command line terminal interface for managing the Tasks list
        Args:
        todo_list -- (ToDoList) - Tasks list to manage
        """

        self.todo_list = todo_list

    def ui_add_new_task(self):
        """
        Interfaces that asks terminal input to create a new Task to Tasks list
        """

        task_desciption = input("Enter task Description\n")
        if task_desciption == "":
            print("Error. You have not entered a task description")
            return False
        deadline_str = input("Enter deadline in (mm/dd/yyyy hh:mm) format: ")
        # convert deadline_str into a datetime format
        try:
            # Convert deadline_str into a datetime format
            deadline_dt = dt.datetime.strptime(deadline_str, "%m/%d/%Y %H:%M")
        except ValueError:
            print("Invalid date format. Please use (mm/dd/yyyy hh:mm).")
            return False
        
        task_status = input("Enter status (Not Started/In Progress/Completed): ")
        if task_status.lower() not in ["not started", "in progress", "completed"]:
            print("You have entered an invalid status")
            return False

        task_priority = input("Enter priority (low or medium or high): ")
        if task_priority.lower() not in ["low", "medium", "high"]:
            print("You have entered an invalid priority")
            return False

        # Create new Task obj
        new_task = Task(task_desciption, deadline_str, task_status, task_priority)
        # Add Task to ToDoList
        self.todo_list.add_task(new_task)

    def ui_remove_task(self):
        """
        Interface that asks terminal input to remove a Task from the Tasks list
        """

        # Print current task list to display Task ID
        self.todo_list.view_tasks()
        task_id_str = input("Please enter the Task ID to delete: ")
        try:
            task_id = int(task_id_str)
        except: return False

        return self.todo_list.remove_task(task_id)
    
    def ui_update_task(self):
        """
        Interfaces that asks terminal input to create a new Tasks details to modify an existing Task
        """
        task_id_str = input("Please enter which task # to update: ")
        # Ensure task ID exists. Return False if it doesn't exist
        try:
            task_id = int(task_id_str)
            if not self.todo_list.validate_task_id(task_id):
                print("Error. You entered an invalid task ID")
                return False 
        except: 
            print("Error! You have entered an incorrect value. Please ensure you are entering a valid number")
            return False

        new_desc = input("Enter new description. Press Enter to skip: ").lower()
        new_deadline = input("Enter new deadline in (mm/dd/yyyy hh:mm) format. Press Enter to skip: ")   
        new_status = input("Enter new staus. Press Enter to skip: ").lower()
        new_priority = input("Enter new priortiy. Press Enter to skip: ").lower()

        try:
            new_deadline = dt.datetime.strptime(new_deadline, "%m/%d/%Y %H:%M")
        except:
            if new_deadline != "":
                print("Error! You entered an date in an invalid format")
                return False
                       
        return self.todo_list.update_task(task_id, new_desc, new_deadline, new_status, new_priority)

    
    def display_main_menu(self):
        """
        Interface to allow terminal input to manage the Tasks List
        
        """

        while True:

            print("1. Add a new Task")
            print("2. View all Tasks")
            print("3. Remove Task: ")
            print("4. Update task")
            print("q. Quit Program")
            user_input = input("Enter selection: ")

            if user_input == "1":
                self.ui_add_new_task()

            # View Tasks
            if user_input == "2":
                self.todo_list.view_tasks()

            # Remove Task
            elif user_input == "3":
                deletion_successful = self.ui_remove_task()
                if deletion_successful: print("Success. Task deleted successfully")
                else: print("Error - Something went wrong when trying to delete the task. Please ensure you entered a valid task ID #")

            # Update Task
            elif user_input == "4":
                self.todo_list.view_tasks()
                if not self.ui_update_task():
                    print("Update Failed")

            # Quick program
            elif user_input == "q": sys.exit()


class CSVhandler:

    def __init__(self, csv_file_path):

        self.csv_path = csv_file_path
        


     
    def add_task(self, new_task : Task):
        with open(self.csv_path, "a", newline="") as save_task:
            csv_writer = csv.writer(save_task)
        
            csv_writer.writerow([new_task.id, new_task.description, new_task.date_added, new_task.deadline, new_task.status, new_task.priority])
