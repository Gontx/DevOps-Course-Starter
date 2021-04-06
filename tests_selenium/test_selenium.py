import requests
import os
import datetime as dt
import pytest
from dotenv import load_dotenv
from todo_app.classes import Item
from threading import Thread

# Load .env variables
load_dotenv()
api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
id_board = os.getenv('ID_BOARD')
dtformat = '%Y-%m-%dT%H:%M:%S.%fZ'

# Define base parameters
base_url = 'https://trello.com/1/'
payload ={ 'key' : api_key , 'token' : token }

def create_board(board_name):
    # Creates a new Trello board and returns the created board's ID
    payload = { 'key' : api_key , 'token' : token , 'name' : board_name }
    r=requests.post(base_url+'boards/' , params = payload)
    r=r.json()
    id_board = r['shortUrl']
    id_board = id_board.rsplit('/', 1)[-1]
    id_board_long = r['id']
    return id_board,id_board_long

def delete_board(id_board):
    # Deletes the speciafied board
    r=requests.delete(base_url+'boards/'+id_board, params = payload)

@pytest.fixture(scope ='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    (id_board,id_board_long) = create_board('SeleniumTestBoard')
    os.environ['ID_BOARD'] = id_board

    # Construct the new application
    application = app.create_app()

    # start the app in its own thread
    thread = Thread(target=lambda:application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    #Tear Down
    thread.join(1)
    delete_board (id_board_long)
