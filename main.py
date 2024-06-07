import datetime as dt
import CSVHandler
import ui as UserInterface
import ToDoList

 
  


my_csv_handler = CSVHandler.CSVhandler()
my_list_todo = ToDoList.ToDoList(my_csv_handler)
ui = UserInterface.UserInterface(my_list_todo)
ui.display_main_menu()



