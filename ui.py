import TaskInterface
import sys
import datetime as dt
import Task
# Menu for user management of ToDoList
# Is a user interface to interact with the ToDoList
class UserInterface:
    # Constructor
    def __init__(self, todo_list : TaskInterface.DataInterface):
        """
        Represents an command line terminal interface for managing the Tasks list
        Args:
        todo_list -- (ToDoList) - Tasks list to manage
        """
        if type(todo_list) is not TaskInterface.DataInterface:
            raise TypeError("UI only accepts a DataInterface object")
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
        
        task_status = input("Enter status (n: Not Started/ i: In Progress/ c: Completed): ").lower()
        if task_status not in ["n", "i", "c"]:
            print("You have entered an invalid status")
            return False

        if task_status == "c": task_status = "completed"
        elif task_status == "i": task_status = "in progress"
        else: task_status = "not started"

        task_priority = input("Enter priority (1: high | 2: medium | 3: low): ")
        if task_priority.lower() not in ["1", "2", "3"]:
            print("You have entered an invalid priority")
            return False

        if int(task_priority) == 1:
            task_priority = "high"
        elif int(task_priority) == 2:
            task_priority = "medium"
        else: task_priority = "low"

        # Create new Task obj
        new_task = Task.Task(task_desciption, deadline_str, task_status, task_priority)
        # Add Task to ToDoList
        return self.todo_list.add_task(new_task)

    def ui_remove_task(self):
        """
        Interface that asks terminal input to remove a Task from the Tasks list
        """

        # Print current task list to display Task ID
        self.todo_list.view_tasks()
        task_id_str = input("Please enter the Task ID to delete: ")
        if not task_id_str.isnumeric():
            print("Error. You entered an invalid character. Please only enter numerical characters")
            return False
        task_id = int(task_id_str)

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
        new_status = input("Enter new status -> n: not started/i: in progress/ c: completed or Press Enter to skip: ").lower()
        new_priority = input("Enter new priortiy. -> 1: high, 2: medium, 3: low or Press Enter to skip: ").lower()

        if new_status not in ["n", "i", "c"]:
            print("You have entered an invalid status")
            return False            
        if new_status == "n": new_status = "not started"
        elif new_status == "i": new_status == "in progress"
        elif new_status == "c": new_status = "completed"

        if new_priority.lower() not in ["1", "2", "3", ""]:
            print("You have entered an invalid priority")
            return False
        
        if new_priority == "1": new_priority = "high"
        elif new_priority == "2": new_priority = "medium"
        elif new_priority == "3": new_priority = "low"

        try:
            new_deadline = dt.datetime.strptime(new_deadline, "%m/%d/%Y %H:%M")
        except ValueError:
            print("Error! You entered an date in an invalid format")
            return False
        update_task = Task.Task(new_desc, new_deadline, new_status, new_priority)
                       
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
            print("5. Advanced Sorting Menu")
            print("q. Quit Program")
            user_input = input("Enter selection: ")

            if user_input == "1":
                if self.ui_add_new_task():
                    print("Successfully added new Task!")
                else: print("Task failed")

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


            elif user_input == "5":
                search_selection = None
                while search_selection != "c":
                    print("""
Please choose a sorting option:
1. Sort by Priority (Ascending)
2. Sort by Priority (Descending)
3. Sort Alphabetically (A-Z)
4. Sort Alphabetically (Z-A)
5. Sort by Status (Ascending)
6. Sort by Status (Descending)
7. Sort by Date Created (Ascending)
8. Sort by Date Created (Descending)
9. Sort by Deadline (Ascending)
10. Sort by Deadline (Descending)
11. q: Back to main menu                          
                        """)
                    search = input("Enter sort method: ").lower()
                    if search in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                        sorted_list = self.todo_list.sorter_interface(search)
                        # Define the headers
                        headers = ["Task ID", "Priority", "Description", "Status", "Date Created", "Deadline"]
    
                        # Print the headers
                        print(f"{headers[0]:<10} {headers[1]:<10} {headers[2]:<30} {headers[3]:<10} {headers[4]:<20} {headers[5]:<20}")
                        print("=" * 100)
    
                        # Print each row in the sorted list
                        for row in sorted_list:
                            print(f"{row[0]:<10} {row[1]:<10} {row[2]:<30} {row[3]:<10} {row[4]:<20} {row[5]:<20}")

                        self.todo_list.load_list_to_csv(sorted_list)
                    elif search == "q":
                        break

            # Quick program
            elif user_input == "q": 
                # Save Tasks list to csv
                sys.exit()
