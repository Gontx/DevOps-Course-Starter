from todo_app.data import session_items as si
from todo_app.classes import  ViewModel
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv
import datetime as dt
import pytest
import json

class TestUnit:
    @staticmethod
    def test_to_do_items():
        bOK = False
        items = si.get_items()
        item_view_model = ViewModel(items)
        to_do_items = item_view_model.to_do_items
        assert len(to_do_items) > 0
        for item in to_do_items:
            assert item.list == "To Do"
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
        assert len(doing_items) > 0
        for item in doing_items:
            assert item.list == "Doing"
    
    @staticmethod
    def test_done_items():
        bOK = False
        items = si.get_items()
        item_view_model = ViewModel(items)
        done_items = item_view_model.done_items
        assert len(done_items) > 0
        for item in done_items:
            assert item.list == "Done"

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