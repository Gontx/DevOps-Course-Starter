from todo_app.data import session_items as si
from todo_app.classes import  ViewModel
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv
import datetime as dt
import pytest
import json
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    # Use our test integration config instead of the "real" version
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@staticmethod
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')

def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/boards/' + si.get_id_board() + '/lists':
        response = Mock()
        # sample_trello_lists_response should pointto some test response data
        sample_trello_lists_response='[{"id":"5fda74f60fc61c6f342225cf","name":"To Do","closed":false,"pos":16384,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false},{"id":"5fda74f60fc61c6f342225d0","name":"Doing","closed":false,"pos":32768,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false},{"id":"5fda74f60fc61c6f342225d1","name":"Done","closed":false,"pos":49152,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false}]'
        response.json.return_value =json.loads(sample_trello_lists_response)
        return response
    return None