from logging import DEBUG
import requests
import os
import pytest
from dotenv import load_dotenv
from threading import Thread
from selenium import webdriver
from todo_app.app import create_app

# MongoDB secrets loading:
load_dotenv()
mongo_usr = os.getenv('MONGO_USR')
mongo_psw = os.getenv('MONGO_PSW')
mongo_url = os.getenv('MONGO_URL')
default_database = os.getenv('DEFAULT_DATABASE')
mongo_protocol = os.getenv('MONGO_PROTOCOL')

dtformat = '%Y-%m-%dT%H:%M:%S.%fZ'

@pytest.fixture(scope ='module')
def app_with_temp_db():
    # Construct the new application
    app = create_app()

    # start the app in its own thread
    thread = Thread(target=lambda:app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    #Tear Down
    thread.join(1)

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--privileged')
    with webdriver.Chrome('./chromedriver',options=opts) as driver:
        yield driver

# Tests
def test_task_journey(driver,app_with_temp_db):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'