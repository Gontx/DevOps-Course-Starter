import datetime as dt
from datetime import date

# Create item class

class Item:

    # Initialize item
    def __init__(self,id_card,list,id_list,title,date_last_activity):
        self.id_card = id_card
        self.list = list
        self.id_list = id_list
        self.title = title
        self.date_last_activity = date_last_activity
    
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

    # Returns items completed today
    @property
    def recent_done_items(self):
        self._recent_done_items = []
        today = dt.date.today()
        for item in self.done_items:
            if item.date_last_activity.date() == today:
                self._recent_done_items.append(item)
        return self._recent_done_items

    # Returns items completed before today
    @property
    def older_done_items(self):
        self._old_done_items = []
        today = dt.date.today()
        for item in self.done_items:
            if item.date_last_activity.date() < today:
                self._old_done_items.append(item)
        return self._old_done_items

    # Returns number of completed items:
    @property
    def n_done(self):
        self._n_done = len(self.done_items)
        return self._n_done