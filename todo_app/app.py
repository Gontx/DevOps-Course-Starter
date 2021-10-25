from todo_app.data.session_items import delete_item
from flask import Flask, render_template, request, url_for, redirect, session
import requests
import flask_login
from todo_app.flask_config import Config
from todo_app.data import session_items as si
from todo_app.classes import mongoViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    # Connect to mongo
    si.connect_mongo()

    # All the routes and setup code etc
    # Index
    @app.route('/')
    def index():
        items = si.get_items()
        item_view_model = mongoViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    # Add item 
    @app.route('/create_item', methods = ['POST'])
    def create_item():
        title = request.form ['title']
        si.add_item(title)
        return redirect(url_for('index'))

    # Update item status
    @app.route('/item_status', methods = ['GET','POST'])
    def item_status():
        item_title = request.form ['item_title']
        item_status = request.form ['item_status']
        item = si.get_item(item_title)
        if item != None:
            si.save_item(item,item_status)
        return redirect(url_for('index'))

    # Delete item
    @app.route('/del_item', methods = ['GET','POST'])
    def del_item():
        del_title = request.form['del_title']
        delete_item(del_title)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app

login_manager = flask_login.LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    pass

@login_manager.user_loader
def load_user(user_id):
    return None

login_manager.init_app(app)