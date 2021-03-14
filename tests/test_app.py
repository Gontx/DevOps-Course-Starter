from todo_app.data import session_items as si
from todo_app.classes import  ViewModel
import datetime as dt
import pytest
from todo_app.app import app

class Unit_tests:
    @staticmethod
    def test_to_do_items():
        bOK = False
        items = si.get_items()
        item_view_model = ViewModel(items)
        to_do_items = item_view_model.to_do_items
        for item in to_do_items:
            if item.list == 'To Do':
                bOK = True
            else:
                bOK = False
                break
        assert bOK == True

    @staticmethod
    def test_doing_items():
        bOK = False
        items = si.get_items()
        item_view_model = ViewModel(items)
        doing_items = item_view_model.doing_items
        for item in doing_items:
            if item.list == 'Doing':
                bOK = True
            else:
                bOK = False
                break
        assert bOK == True

    @staticmethod
    def test_done_items():
        bOK = False
        items = si.get_items()
        item_view_model = ViewModel(items)
        done_items = item_view_model.done_items
        for item in done_items:
            if item.list == 'Done':
                bOK = True
            else:
                bOK = False
                break
        assert bOK == True

    @staticmethod 
    def test_recent_done_items():
        bOK = False
        # Get today
        today = dt.date.today()
        items = si.get_items()
        item_view_model = ViewModel(items)
        recent_items = item_view_model.recent_done_items
        for item in recent_items:
            if item.date_last_activity.date() == today:
                bOK = True
            else:
                bOK = False
                break
        assert bOK == True

    @staticmethod 
    def test_old_done_items():
        bOK = False
        # Get today
        today = dt.date.today()
        items = si.get_items()
        item_view_model = ViewModel(items)
        old_done_items = item_view_model.older_done_items
        for item in old_done_items:
            if item.date_last_activity.date() < today:
                bOK = True
            else:
                bOK = False
                break
        assert bOK == True

class Integration_tests:
    def test_index_page(client):
        response = client.get('/')
        assert response.status_code == 200

@pytest.fixture
def client():
    # Use our test integration config instead of the "real" version
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own
    function
        mock_get_requests.side_effect = mock_get_lists
        response = client.get('/')
    def mock_get_lists(url, params):
        if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value =sample_trello_lists_response
        return response
    return None