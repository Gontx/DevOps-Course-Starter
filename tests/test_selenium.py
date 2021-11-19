from logging import DEBUG
import requests
import os
from dotenv import find_dotenv
import pytest
from dotenv import load_dotenv
from threading import Thread
from selenium import webdriver
from todo_app.app import create_app

dtformat = '%Y-%m-%dT%H:%M:%S.%fZ'

@pytest.fixture(scope ='module')
def app_with_temp_db():
    file_path = find_dotenv('.env') 
    load_dotenv(file_path, override=True)
    # CosmosDB  secrets:
    cosmos_database_name = os.getenv('DATABASE_NAME')
    cosmos_primary_master_key = os.getenv('PRIMARY_MASTER_KEY')
    cosmos_url = os.getenv("COSMOS_URL")
    cosmos_port = os.getenv("COSMOS_PORT")
    # Construct the new application
    app = create_app()
    app.config['LOGIN_DISABLED'] = True
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
    driver.implicitly_wait(30)
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'