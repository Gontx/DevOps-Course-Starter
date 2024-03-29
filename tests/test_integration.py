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
   
    # CosmosDB  secrets:
    cosmos_database_name = os.getenv('DATABASE_NAME')
    cosmos_url = os.getenv("COSMOS_URL")
    cosmos_port = os.getenv("COSMOS_PORT")
    cosmos_connection_string = os.getenv('COSMOS_CONNECTION_STRING')
    # Mongomock
    with mongomock.patch(servers=((f'{cosmos_database_name}.{cosmos_url}', int(cosmos_port)),)):
        # Create the new app.
        test_app = create_app()
        test_app.config['LOGIN_DISABLED'] = True

        # Connect to CosmosDB using mongo api:
        mclient = pymongo.MongoClient(cosmos_connection_string)
        
        # Add fake items to mongomock
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
