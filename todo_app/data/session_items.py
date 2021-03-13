from flask import session
import requests
import os
from dotenv import load_dotenv
from todo_app.classes import Item

# Load .env variables
load_dotenv()
api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
id_board = os.getenv('ID_BOARD')

# Define base parameters
base_url = 'https://trello.com/1/'
payload ={ 'key' : api_key , 'token' : token }

def get_items():
    """
    Fetches all saved items from specified session.

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
                id_item = card ['id']
                id_list = list ['id']
                item=Item(i+1,id_item,status,id_list,name)
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

    # Obtain todo_id
    r=requests.get(base_url + 'boards/' + id_board + '/lists' , params = payload)
    r=r.json()
    
    for list in r:
        if 'To Do' == list['name']:
            todo_id = list['id']
            break

    # Create item card in Trello using to Do list as default
    r=requests.post(base_url+'cards?'+'idList='+todo_id+'&name='+title , params = payload)
    r=r.json()
    # Obtain trello item id
    id_card = r['id']
    # Obtain trello list id
    id_list = r['idList']
    

def save_item(item,target_list):
    """
    Updates a card from the board with the target list. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
   
    # obtain id_list for target list
    r=requests.get(base_url + 'boards/' + id_board + '/lists' , params = payload)
    r=r.json()
    
    for list in r:
        if target_list == list['name']:
            id_list = list['id']
            break

    # Update card
    r=requests.put(base_url + 'cards/' + item.id_card + '?idList=' + id_list , params = payload)

    return 

def delete_item(id_num):
    """
    Removes the item for the ID given. After that re-asigns ID
    Args: 
        ID of the item to delete
    
    """

    items = get_items()

    for item in items:
        if item.id == id_num:
            r=requests.delete(base_url + 'cards/' + item.id_card, params = payload)
            break        
    return