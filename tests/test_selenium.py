import requests
import os
import datetime as dt
from dotenv import load_dotenv
from todo_app.classes import Item

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
    id_board = r['id']
    return id_board

def delete_board(id_board):
    # Deletes the speciafied board
    r=requests.delete(base_url+'boards/'+id_board, params = payload)

id_new_board = create_board('TestBoard69')
delete_board (id_new_board)