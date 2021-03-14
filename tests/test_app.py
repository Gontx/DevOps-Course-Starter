from todo_app.data.session_items import delete_item, return_list_items, get_items
from flask import Flask, render_template, request, url_for, redirect, session
import requests
from todo_app.flask_config import Config
from todo_app.data import session_items as si
from todo_app.classes import Item, ViewModel

class Test:
    @staticmethod
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
        
    @staticmethod
    def test_to_do_items():
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