import requests
import os
import datetime as dt
import pymongo
from dotenv import load_dotenv
from todo_app.classes import Item

# Load .env variables
load_dotenv()
api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
id_board = os.getenv('ID_BOARD')

# MongoDB secrets loading:
mongo_usr = os.getenv('MONGO_USR')
mongo_psw = os.getenv('MONGO_PSW')
mongo_url = os.getenv('MONGO_URL')
default_database = os.getenv('DEFAULT_DATABASE')

# Datetime format:
dtformat = '%Y-%m-%dT%H:%M:%S.%fZ'

# Connect to MongoDB ATLAS:
client = pymongo.MongoClient("mongodb+srv://"+mongo_usr+":"+mongo_psw+"@"+mongo_url+"/"+default_database+"?w=majority")
print (client.list_database_names())
db = client.board
# Define base parameters
base_url = 'https://trello.com/1/'
payload ={ 'key' : api_key , 'token' : token }

def get_items():
    """
    Fetches all saved items from specified session.

    Returns:
        list: The list of saved items.
    """
    # Obtain collections within database (lists within board):
    dblists = db.list_collection_names()
    print (dblists)
    print (dblists[0])

    # Obtain documents in each collection
    docs = []
    for dblist in dblists:
        dblist_name = db[dblist]
        for doc in dblist_name.find():
            docs.append(doc)
    
    # Assign name and status to item
    items = []
    for doc in docs:
        for dblist in dblists:
            if doc['status'] == dblist:
                status = doc['status']
                title = doc['title']
                date_created = doc['date created']
                item=Item(status,title,date_created)
                items.append(item)
    return items
        
    # Request lists within the board
    r=requests.get(base_url + 'boards/' + get_id_board() + '/lists' , params = payload)
    r=r.json()
    lists = r

    #Request cards on a list
    cards = []
    for list in lists:
        id_list = list['id']
        name_list = list['name']
        r=requests.get(base_url + 'lists/' + id_list + '/cards', params = payload)
        r=r.json()
        for card in r:
            cards.append(card)

    # Assign name, and status to item
    items=[]
    for card in cards:
        for list in lists:
            if card['idList'] == list['id']:
                status = list['name']
                name = card['name']
                id_item = card ['id']
                id_list = list ['id']
                date_last_activity = card['dateLastActivity']
                date_last_activity = dt.datetime.strptime(date_last_activity,dtformat)
                item=Item(id_item,status,id_list,name,date_last_activity)
                items.append(item)
    return items

def get_item(title):
    """
    Fetches the saved item with the specified item title.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.title == title), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    # Add document to collection
    doc = {'title':title, 'status':'to do' , 'date created':dt.datetime.utcnow()}
    to_do_items=db['to_do_items']
    doc_id = to_do_items.insert_one(doc).inserted_id

def save_item(item,target_list):
    """
    Updates a card from the board with the target list. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
   
    # obtain id_list for target list
    r=requests.get(base_url + 'boards/' + get_id_board() + '/lists' , params = payload)
    r=r.json()
    
    for list in r:
        if target_list == list['name']:
            id_list = list['id']
            break

    # Update card
    r=requests.put(base_url + 'cards/' + item.id_card + '?idList=' + id_list , params = payload) 

def delete_item(id_title):
    """
    Removes the item for the ID given. After that re-asigns ID
    Args: 
        ID of the item to delete
    
    """

    items = get_items()

    for item in items:
        if item.title == id_title:
            r=requests.delete(base_url + 'cards/' + item.id_card, params = payload)
            break  

def get_id_board():
    return os.getenv('ID_BOARD')   