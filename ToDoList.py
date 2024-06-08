import CSVHandler
import Task

# holds the actual data -> List of Tasks
class ToDoList: 
    # Constructor
    def __init__(self, csv_obj : CSVHandler):
        self.csv_obj = csv_obj
     
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