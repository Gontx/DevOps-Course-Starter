from flask import session
import requests
from auth import api_key, token
from todo_app.classes import Item

# Define base parameters
base_url = 'https://trello.com/1/'
id_board = 'sr8Gn9uE'
payload ={ 'key' : api_key , 'token' : token }
todo_id = '5fda74f60fc61c6f342225cf'

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' },
    { 'id': 3, 'status': 'Complete', 'title': 'test'}
]


def get_items():
    """
    Fetches all saved items from specified Trello board.

    Returns:
        list: The list of saved items.
    """

    # Request lists within the board
    r=requests.get(base_url + 'boards/' + id_board + '/lists' , params = payload)
    r=r.json()
    lists = r

    #Request cards on a list
    cards = []
    for list in lists:
        id_list = list['id']
        name_list = list['name']
        r=requests.get(base_url + 'lists/' + id_list + '/cards', params = payload)
        print (r.status_code)
        r=r.json()
        for card in r:
            cards.append(card)
    # Assign name, and status to item
    i=0
    items=[]
    for card in cards:
        for list in lists:
            if card['idList'] == list['id']:
                status = list['name']
                name = card['name']
                item=Item(i,status,name)
                items.append(item)
                i=i+1
    return session.get('items', items)


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1].id + 1 if items else 0

    item = Item(id , title , 'To do')

    # Create item card in Trello using to Do list as default
    r=requests.post(base_url+'cards?'+'idList='+todo_id+'&name='+title , params = payload)

    return 

def save_item(item):
    """
    Updates a card from the board. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def delete_item(id_num):
    """
    Removes the item for the ID given. After that re-asigns ID
    Args: 
        ID of the item to delete
    
    """
    items = get_items()
    for item in items:
        if id_num==item['id']:
            items.pop(id_num-1)
            for idx, item in enumerate(items):
                items[idx]['id']=idx+1

            session['items'] = items
