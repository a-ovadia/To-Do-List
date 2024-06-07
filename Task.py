import datetime as dt

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