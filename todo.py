import datetime as dt
import sys
import csv
import os

## TODO Store data in a CSV file instead of List

# individual Task
class Task:

    # Constructor
    def __init__(self, description="", deadline = None, status = "Not Started", priority = "low"):
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
        self.date_added = dt.datetime.now().strftime("%m/%d/%Y %H:%M")
        
        # convert priority to int values
        self.priority = priority.lower()
    
    # define print statement for Task class
    def __repr__(self) -> str:
        """
        Define how Task obj should be represented
        """
        return f"Description: {self.description}\t Deadline: {self.deadline}\t Status: {self.status}\t Priority: {self.priority}"

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

    def change_status(self, new_status):
        """
        Sets the task status
        Args:
        new_status -- (str) new task status
        """
        self.status = new_status


# Format of CSV:
# Task ID,Task Priority,Task Description,Task StatusTask Created,Task Deadline

class CSVhandler():

    def __init__(self, file_path = "hit.csv"):
        self.path = file_path

    

    # Add a list of Task (ToDoList) to a csv 
    # Append list to the csv file
    def add_todo_to_csv(self, task : Task ):
        next_id = self.get_last_task_id() + 1
        with open(self.path, "a", newline="") as csv_file:
            csv_file_writer = csv.writer(csv_file)
            
            csv_file_writer.writerow([next_id, task.priority, task.description, task.status, task.date_added, task.deadline])



    def get_last_task_id(self):
        """
        Finds the last task ID in the CSV
        Return -- (int) Task ID of last entry or 0 if empty
        """
        last_line = None
        with open(self.path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip header
            row = next(csv_reader)
            for row in csv_reader:
                last_line = row
        if last_line == None:
            return 0
        return int(last_line[0])
    
    def print_csv_file(self):
        """
        Outputs contents of the csv to terminal view
        """
        print("{:<20} {:<20} {:<30} {:<20} {:<20} {:<30}".format("Task ID", "Task Priority", "Description", "Status", "Date added", "Deadline"))
        print("-" * 110)  # Separator line
        with open(self.path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader) # Skip header
            for row in csv_reader:
                print("{:<20} {:<20} {:<30} {:<20} {:<20} {:<30}".format(row[0], row[1], row[2], row[3], row[4] , row[5]))

    def validate_task_id(self, task_id):
        """
        Validates whether a task exists in the csv file

        Args:
            task_id -- (int) Task to search csv for
        """
        try:
            with open(self.path, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                row = next(csv_reader)
                for row in csv_reader:
                    
                    if int(row[0]) == task_id:
                        # Task found
                        return True
                    
        except: print("Error searching for task")
        return False
        
    def update_csv_file(self, task, id):
        # Create temp file 
        temp_file = self.path + ".tmp"
        task_found = False
        if not self.validate_task_id(id):
            print("Error. You entered an invalid Task ID")
            return False

        with open(self.path, "r", newline="") as csv_file, open(temp_file, "w", newline="") as csv_tmp:
            csv_writer = csv.writer(csv_tmp)
            csv_reader = csv.reader(csv_file)
            
            header = next(csv_reader)
            csv_writer.writerow(header) # Write header to temp file
            
            

            for row in csv_reader:
                if int(row[0]) == id:
                    updated_priority = task.priority if task.priority != "" else row[1]
                    updated_description = task.description if task.description != "" else row[2]
                    updated_status = task.status if task.status != "" else row[3]
                    updated_deadline = task.deadline if task.deadline != "" else row[5]
                    date_added = row[4]

                    csv_writer.writerow([id, updated_priority, updated_description, updated_status, date_added, updated_deadline])
                    task_found = True
                    
                else:
                    csv_writer.writerow(row)
                
    
        if task_found:
            os.replace(temp_file, self.path)
        else:
            os.remove(temp_file)

    def remove_task(self, task_id):
        if not self.validate_task_id(task_id):
            print("Error. You entered an invalid Task ID")
            return False
        
        tmp_file = self.path + ".tmp"
        task_removed = False

        with open(self.path, "r") as csv_file, open(tmp_file, "w", newline="") as tmp_csv_file:
            csv_writer = csv.writer(tmp_csv_file)
            
            csv_reader = csv.reader(csv_file)
            
            header = next(csv_reader)
            csv_writer.writerow(header) # Write header to temp file
            task_id_counter = 0
            

            for row in csv_reader:
                # check if the row does not match the ID
                if int(row[0]) != task_id:
                    # If we have not found the task, add to tmp file
                    if not task_removed:
                        csv_writer.writerow(row)
                        
                    # If we found the task, we have to modify the task IDs afterwards to match up to prevent gaps in IDs
                    else:
                        
                        row[0] = task_id_counter
                        csv_writer.writerow(row)
                        task_id_counter += 1
                else:
                    # skip
                    task_removed = True
                    # Set ID to None to ensure previous if check returns False and thus executes for the rest of the tasks
                    task_id_counter = task_id
                    task_id = None


    
        if task_removed:
            os.replace(tmp_file, self.path)
            return True
        else:
            os.remove(tmp_file)
            return False

         


# holds the actual data -> List of Tasks
class ToDoList: 

    def __init__(self, csv_obj : CSVhandler):
        self.tasks = []
        self.file_path = csv_obj.path
        self.csv_obj = csv_obj
        self.task = None
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
       
        self.csv_obj.add_todo_to_csv(new_task)

    # Remove task from list
    def remove_task(self, remove_task_id : int):
        """
        Remove a task from the Tasks list
        Args:
        remove_task_id -- (int) remove task with the ID from Tasks list
        """
        return self.csv_obj.remove_task(remove_task_id)
        
       

    def view_tasks(self):
        """
        Output to terminal a list of all Tasks in the Task list
        """
        self.csv_obj.print_csv_file()

    def validate_task_id(self, task_id):
        """
        Check if an ID is in the Tasks list
        Args:
        task_id -- (int) return true if task_id matches an element in the Tasks list, False otherwise
        """
 
        return False   

    
    def update_task(self, update_task, task_id):

        """
        Update an existing Task in Tasks list with new task data
        Args:
        task_id -- (int) Represents which task to update
        update_desc -- (str) new task description
        update_deadline -- (datetime) new task deadline
        update_status -- (str) new task status
        update_priority -- (str) new task priority
        """   
        
        self.csv_obj.update_csv_file(update_task, task_id)
    
  
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
        # try:
        #     task_id = int(task_id_str)
        #     if not self.todo_list.validate_task_id(task_id):
        #         print("Error. You entered an invalid task ID")
        #         return False 
        # except: 
        #     print("Error! You have entered an incorrect value. Please ensure you are entering a valid number")
        #     return False

        task_id = int(task_id_str)
        new_desc = input("Enter new description. Press Enter to skip: ").lower()
        new_deadline = input("Enter new deadline in (mm/dd/yyyy hh:mm) format. Press Enter to skip: ")   
        new_status = input("Enter new staus. Press Enter to skip: ").lower()
        new_priority = input("Enter new priortiy. Press Enter to skip: ").lower()

        if new_priority.lower() not in ["low", "medium", "high", ""]:
            return False
        

        try:
            new_deadline = dt.datetime.strptime(new_deadline, "%m/%d/%Y %H:%M")
        except:
            if new_deadline != "":
                print("Error! You entered an date in an invalid format")
                return False
        update_task = Task(new_desc, new_deadline, new_status, new_priority)
                       
        return self.todo_list.update_task(update_task, task_id)

    
    def display_main_menu(self):
        """
        Interface to allow ter2minal input to manage the Tasks List
        
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
            elif user_input == "q": 
                # Save Tasks list to csv
                sys.exit()





my_csv_handler = CSVhandler()
my_list_todo = ToDoList(my_csv_handler)
ui = UserInterface(my_list_todo)
ui.display_main_menu()



