from todo_app.data import session_items as si
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv
import pytest
import pymongo
import mongomock
import os
import datetime as dt

@pytest.fixture
def client():
    # Use our test integration config instead of the "real" version
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)
    # MongoDB secrets loading:
    mongo_usr = os.getenv('MONGO_USR')
    mongo_psw = os.getenv('MONGO_PSW')
    mongo_url = os.getenv('MONGO_URL')
    default_database = os.getenv('DEFAULT_DATABASE')
    mongo_protocol = os.getenv('MONGO_PROTOCOL')    
    
    # Mongomock
    with mongomock.patch(servers=((mongo_url, 27017),)):
        # Create the new app.
        test_app = create_app()

        # Add fake items to mongomock
        mclient = pymongo.MongoClient(mongo_protocol+"://"+mongo_usr+":"+mongo_psw+"@"+mongo_url+"/"+default_database+"?w=majority")
        #mclient = pymongo.mongoclient(mongo_url)
        db = mclient.testboard

        to_do_items = db['to do']
        doc_todo = {'title': 'Test item 1', 'status':'to do' , 'date modified':dt.datetime.utcnow()}
        to_do_items.insert_one(doc_todo)

        doing_items = db['doing']
        doc_doing = {'title': 'Test item 2', 'status':'doing' , 'date modified':dt.datetime.utcnow()}
        doing_items.insert_one(doc_doing)

        done_items = db['done']
        doc_done = {'title': 'Test item 3', 'status':'done' , 'date modified':dt.datetime.utcnow()}
        done_items.insert_one(doc_done)

        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

@staticmethod
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200