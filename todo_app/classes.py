
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

    @property
    def to_do_items(self):
        self._to_do_items = []
        for item in self.items:
            if item.list == 'To Do':
                self._to_do_items.append(item)
        return self._to_do_items

    @property
    def doing_items(self):
        self._doing_items = []
        for item in self.items:
            if item.list == 'Doing':
                self._doing_items.append(item)
        return self._doing_items

    @property
    def done_items(self):
        self._done_items = []
        for item in self.items:
            if item.list == 'Done':
                self._done_items.append(item)
        return self._done_items

    # Returns all done items
    @property
    def show_all_done_items():
        return

    # Returns items completed today
    @property
    def recent_done_items():
        return

    # Returns items completed before today
    @property
    def older_done_items():
        return