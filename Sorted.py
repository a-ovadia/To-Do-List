
# Class used to provide sorting capabilities
class Sorter:

    def __init__(self, sort_option, sort_data):
        self.option = sort_option.lower()
        self.data = sort_data
    
    def set_sort_option(self, option):
        self.option = option

    def set_sort_data(self, data):
        self.data = data
    
    def get_sort_option(self):
        return self.option
    
    def get_sort_data(self):
        return self.data
    
    def priority_key(self, item):
        """Custom key for sorting by priority."""
        priority_map = {'high': 1, 'medium': 2, 'low': 3}
        return priority_map.get(item[1].lower()) 

    """
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
"""
    def sort(self):
        if self.option == "1":
            return sorted(self.data, key=self.priority_key)

        elif self.option == "2":
            return sorted(self.data, key=self.priority_key, reverse=True)
