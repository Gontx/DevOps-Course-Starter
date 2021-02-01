
# Create item class

class Item:

    # Initialize item
    def __init__(self,id,status,title):
        self.id = id
        self.status = status
        self.title = title
    
    # Method to update item status
    def update_status(self,new_status):
        self.status = new_status


test = Item(2,'to do', 'test')
print(test.id,test.status,test.title)

test.update_status('in progress')
print(test.id,test.status,test.title)