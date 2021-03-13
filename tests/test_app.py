from todo_app.data.session_items import delete_item, return_list_items, get_items
from flask import Flask, render_template, request, url_for, redirect, session
import requests
from todo_app.flask_config import Config
from todo_app.data import session_items as si
from todo_app.classes import Item, ViewModel
import os
from dotenv import load_dotenv


# Load .env variables
load_dotenv()
api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
id_board = os.getenv('ID_BOARD')


def test_just_one_list():
    lists = ['To Do','Doing','Done']
    for list in lists:
        items = return_list_items(list)
        for item in items:
            if item.list == list:
                bOK = True
            else:
                bOK = False
                break
        if bOK == False:
            break
    assert bOK == True

def test_to_do_items():
    list = 'To Do'
    items=ViewModel.to_do_items
    for item in items:
        if item.list == list:
            bOK = True
        else:
            bOK = False
            break
    if bOK == False:
        break
    assert bOK == True