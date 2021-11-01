from todo_app.data.session_items import delete_item
from flask import Flask, render_template, request, url_for, redirect, session
import requests
import os
import flask_login
from flask_login import login_required, login_user, UserMixin, current_user
from oauthlib.oauth2 import WebApplicationClient
from todo_app.flask_config import Config
from todo_app.data import session_items as si
from todo_app.classes import ViewModel, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    # Connect to mongo
    si.connect_mongo()

    # All the routes and setup code etc
    # Index
    @app.route('/')
    @login_required
    def index():
        items = si.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    # Add item 
    @app.route('/create_item', methods = ['POST'])
    @login_required
    def create_item():
        title = request.form ['title']
        si.add_item(title)
        return redirect(url_for('index'))

    # Update item status
    @app.route('/item_status', methods = ['GET','POST'])
    @login_required
    def item_status():
        item_title = request.form ['item_title']
        item_status = request.form ['item_status']
        item = si.get_item(item_title)
        if item != None:
            si.save_item(item,item_status)
        return redirect(url_for('index'))

    # Delete item
    @app.route('/del_item', methods = ['GET','POST'])
    @login_required
    def del_item():
        del_title = request.form['del_title']
        delete_item(del_title)
        return redirect(url_for('index'))
    
    ### OAuth ###
    # Obtain GitHub OAuth Secrets:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    # Initialize login_manager class
    login_manager = flask_login.LoginManager()

    # Create client
    client = WebApplicationClient(client_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        # Add logic to redirect to the Github OAuth flow when unauthenticated
        # Request identity
        # Redirect to site
        # Return -> redirect to github
        redirecturl = client.prepare_request_uri("https://github.com/login/oauth/authorize")
        return redirect(redirecturl)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/login', methods = ['GET'])
    def login():
        code = request.args.get('code')
        token_url, headers, body = client.prepare_token_request('https://github.com/login/oauth/access_token', code = code )
        headers['Accept']= 'application/json'
        response = requests.post(token_url, headers = headers, data = body, auth = (client_id,client_secret))
        response = response.json()
        access_token = response['access_token']
        usr_url = 'https://api.github.com/user'
        headers = {'Authorization': 'token ' + access_token}
        usr_response = requests.get(usr_url, headers = headers )
        usr_response = usr_response.json()
        user = User(usr_response['id'])
        login_user(user)
        return redirect(url_for('index'))

    login_manager.init_app(app)
    
    ### MAIN ###
    if __name__ == '__main__':
        app.run()

    return app