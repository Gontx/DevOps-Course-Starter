
# Create item class

class Item:

    # Initialize item
    def __init__(self,id_card,list,id_list,title):
        self.id_card = id_card
        self.list = list
        self.id_list = id_list
        self.title = title
    
    # Method to update item status
    def update_status(self,new_status):
        self.status = new_status

class ViewModel:
    def __init__(self,items):
        self._items = items
    
    @property
    def items(self):
        return self._items