import datetime as dt
from datetime import date
from flask_login import UserMixin

# Create item class
class Item:
    # Initialize item
    def __init__(self,status,title,date_last_modified):
        self.status = status
        self.title = title
        self.date_last_modified = date_last_modified
    # Method to update item status
    def update_status(self,new_status):
        self.status = new_status
        
# Create User class
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

# Create ViewModel class
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
            if item.status == 'to do':
                self._to_do_items.append(item)
        return self._to_do_items

    @property
    def doing_items(self):
        self._doing_items = []
        for item in self.items:
            if item.status == 'doing':
                self._doing_items.append(item)
        return self._doing_items

    @property
    def done_items(self):
        self._done_items = []
        for item in self.items:
            if item.status == 'done':
                self._done_items.append(item)
        return self._done_items

    # Returns items completed today
    @property
    def recent_done_items(self):
        self._recent_done_items = []
        today = dt.date.today()
        for item in self.done_items:
            if item.date_last_modified.date() == today:
                self._recent_done_items.append(item)
        return self._recent_done_items

    # Returns items completed before today
    @property
    def older_done_items(self):
        self._old_done_items = []
        today = dt.date.today()
        for item in self.done_items:
            if item.date_last_modified.date() < today:
                self._old_done_items.append(item)
        return self._old_done_items

    # Returns number of completed items:
    @property
    def n_done(self):
        self._n_done = len(self.done_items)
        return self._n_done

    # Returns number of recent completed items:
    @property
    def n_recent_done(self):
        self._n_recent_done = len(self.recent_done_items)
        return self._n_recent_done
