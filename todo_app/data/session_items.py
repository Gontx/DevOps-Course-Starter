import os
import datetime as dt
import pymongo
from dotenv import load_dotenv
from todo_app.classes import Item

# Secret key loading:
secret_key = os.getenv('SECRET_KEY')

# Datetime format:
dtformat = '%Y-%m-%dT%H:%M:%S.%fZ'

# Function to connect to mongo
def connect_mongo():
    load_dotenv()
    # CosmosDB  secrets:
    cosmos_connection_string = os.getenv('COSMOS_CONNECTION_STRING')
    database_name = os.getenv('DATABASE_NAME')
    # Connect to CosmosDB using mongo api:
    client = pymongo.MongoClient(cosmos_connection_string)
    global db
    db = client.todoappdb

def get_items():
    """
    Fetches all saved items from specified session.

    Returns:
        list: The list of saved items.
    """
    # Obtain collections within database (lists within board):
    dblists = db.list_collection_names()
    
    # Obtain documents in each collection
    items = []
    for dblist in dblists:
        dblist_name = db[dblist]
        for doc in dblist_name.find():
            status = doc['status']
            title = doc['title']
            date_last_modified = doc['date modified']
            item = Item(status,title,date_last_modified)
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
    doc = {'title':title, 'status':'to do' , 'date modified':dt.datetime.utcnow()}
    to_do_items = db['to do']
    to_do_items.insert_one(doc)

def save_item(item,target_list):
    """
    Updates a card from the board with the target list. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    
    collection_to = db[target_list]
    doc = {'title':item.title, 'status':target_list , 'date modified':dt.datetime.utcnow()}
    collection_to.insert_one(doc)

    collection_from = db[item.status]
    docu = collection_from.find_one({'title':item.title})
    collection_from.delete_one(docu)

def delete_item(title):
    """
    Removes the item for title given. 
    Args: 
        title of the item to delete
    
    """
    item = get_item(title)
    collection = db[item.status]
    item_to_delete = collection.find_one({'title': title})
    collection.delete_one(item_to_delete)   