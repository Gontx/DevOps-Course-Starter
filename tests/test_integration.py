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
        test_app.config['LOGIN_DISABLED'] = True

        # Add fake items to mongomock
        mclient = pymongo.MongoClient(mongo_protocol+"://"+mongo_usr+":"+mongo_psw+"@"+mongo_url+"/"+default_database+"?w=majority")
        #mclient = pymongo.mongoclient(mongo_url)
        db = mclient.testboard

        insert_document('Test item 1','to do',db)
        insert_document('Test item 2','doing',db)
        insert_document('Test item 3','done',db)

        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

class TestIntegration:
    @staticmethod
    def test_index_page(client):
        response = client.get('/')
        assert response.status_code == 200

def insert_document(title, status, db):
    db_used = db[status]
    doc = {'title':title, 'status':status, 'date modified':dt.datetime.utcnow()}
    db_used.insert_one(doc)
