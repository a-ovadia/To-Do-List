import Task
import csv
import os
# Format of CSV:
# Task ID,Task Priority,Task Description,Task StatusTask Created,Task Deadline


# Todo initialize new csv file and set the headers
class CSVhandler:
    # Constructor
    def __init__(self, file_path = "My Task Lists.csv"):
        if ".csv" not in file_path:
            raise FileNotFoundError("The filename must end in .csv")
        self.path = file_path
        self.initialze_csv_file_headers()

    def __repr__(self):
        return f"CSV file: {self.path}"

    def initialze_csv_file_headers(self):
        try:
            with open(self.path, "x", newline="") as new_csv_file:
                csv_writer = csv.writer(new_csv_file)
                row = ["Task ID", "Priority", "Description", "Status", "Dated Created", "Deadline" ]
                csv_writer.writerow(row)
        except Exception as e:
            print(f"An error occured with trying to modify {self.path}")

    def set_path(self, file_path):
        self.path = file_path

    def get_path(self):
        return self.path

    # Add a list of Task (ToDoList) to a csv 
    # Append list to the csv file
    def add_todo_to_csv(self, task : Task ):
        """
        Appends a Task to the task list csv
        Args:
            task -- (Task) Task to add
        """
        next_id = self.get_last_task_id() + 1
        try:
            with open(self.path, "a", newline="") as csv_file:
                csv_file_writer = csv.writer(csv_file)
                
                csv_file_writer.writerow([next_id, task.priority, task.description, task.status, task.date_added, task.deadline])
                return True
        except Exception as e:
            print(f"An error has occurred when trying to add a new task {e}")
            return False


    def get_last_task_id(self):
        """
        Finds the last task ID in the CSV
        Return -- (int) Task ID of last entry or 0 if empty
        """
        last_line = None
        with open(self.path, "r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    last_line = row
        if last_line is None or not last_line[0].isnumeric():
            return 0
        try:
            return int(last_line[0])
        except ValueError:
            return 0
    
    def print_csv_file(self):
        """
        Outputs contents of the csv to terminal view
        """
        print("{:<8} {:<13} {:<40} {:<20} {:<20} {:<30}".format("Task ID", "Task Priority", "Description", "Status", "Date added", "Deadline"))
        print("-" * 110)  # Separator line
        try:
            with open(self.path, "r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader) # Skip header
                for row in csv_reader:
                    try:
                        if row[0].isnumeric():
                            print("{:<8} {:<13} {:<30} {:<20} {:<20} {:<30}".format(row[0], row[1], row[2], row[3], row[4] , row[5]))

                    except FileNotFoundError:
                        print(f"Error: The file '{self.path}' does not exist.")
                    except IndexError as e:
                        print(f"Error: Missing data in CSV row. {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
        except Exception as e:
            print(f"An exception occured when trying to read the file {e}")

    def validate_task_id(self, task_id):
        """
        Validates whether a task exists in the csv file

        Args:
            task_id -- (int) Task to search csv for
        """
        try:
            with open(self.path, "r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                row = next(csv_reader)
                for row in csv_reader:
                    
                    if int(row[0]) == task_id:
                        # Task found
                        return True
                    
        except: print("Error searching for task")
        return False
        
    def update_csv_file(self, task, id):
        """
        Updates one Task stored in the tasks list csv
        Args:
            task -- (Task) New Task data to replace an existing Task
            id -- (int) Task ID of position of Task in the csv to update

        """
        # Create temp file 
        temp_file = self.path + ".tmp"
        task_found = False
        if not self.validate_task_id(id):
            print("Error. You entered an invalid Task ID")
            return False
        try:
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
        except Exception as e:
            print(f"An exception occured when trying to read the file {e}")
    
        if task_found:
            os.replace(temp_file, self.path)
        else:
            os.remove(temp_file)

    def remove_task(self, task_id):
        """
        Removes a task from the task list csv
        Args:
            task_id -- (int) Position of the task to remove
        """
        if not self.validate_task_id(task_id):
            print("Error. You entered an invalid Task ID")
            return False
        
        tmp_file = self.path + ".tmp"
        task_removed = False
        try: 
            with open(self.path, "r", newline="") as csv_file, open(tmp_file, "w", newline="") as tmp_csv_file:
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
        except Exception as e:
            print(f"An exception occured when trying to read the file {e}")

    
        if task_removed:
            os.replace(tmp_file, self.path)
            return True
        else:
            os.remove(tmp_file)
            return False


    def load_csv_to_list(self):
        """
        Outputs contents of the csv to a list
        """
        task_list = []
        try:
            with open(self.path, "r", newline="") as csv_file:

                csv_reader = csv.reader(csv_file)
                next(csv_reader) # Skip header
                for row in csv_reader:
                    task_list.append(row)
        except Exception as e:
            print(f"An exception occured when trying to read the file {e}")
        return task_list
    
    def load_list_to_csv(self, task_list):
        try:
            with open(self.get_path(), "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                row = ["Task ID", "Priority", "Description", "Status", "Dated Created", "Deadline" ]
                csv_writer.writerow(row)
                for entry in task_list:
                    csv_writer.writerow(entry)
        except Exception as e:
            print(f"An exception occured when trying to read the file {e}")