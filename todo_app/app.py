from todo_app.data.session_items import delete_item
from flask import Flask, render_template, request, url_for, redirect, session

import requests

from todo_app.flask_config import Config
from todo_app.data import session_items as si
from todo_app.classes import Item

app = Flask(__name__)
app.config.from_object(Config)

# Index
@app.route('/')
def index():
    items = si.get_items()
    return render_template('index.html', items =items)

# Add item 
@app.route('/form', methods = ['GET','POST'])
def form():
    title = request.form ['title']
    si.add_item(title)
    items = si.get_items()
    return redirect(url_for('index'))

# Update item status
@app.route('/item_status', methods = ['GET','POST'])
def item_status():
    item_id = int(request.form ['item_id'])
    item_status = request.form ['item_status']
    item = si.get_item(item_id)
    if item != None:
        si.save_item(item,item_status)
    return redirect(url_for('index'))

# Sort items by status
@app.route('/status_sortItems', methods = ['GET','POST'])
def status_sortItems():
    initial_items = si.get_items()
    final_items = sorted(initial_items, key = lambda item:item['status'])
    session['items'] = final_items
    return redirect(url_for('index'))

# Sort items by id
@app.route('/id_sort_items', methods = ['GET','POST'])
def id_sort_items():
    initial_items = si.get_items()
    final_items = sorted(initial_items, key = lambda item:item['id'])
    session['items'] = final_items
    return redirect(url_for('index'))

# Delete item
@app.route('/del_item', methods = ['GET','POST'])
def del_item():
    items = si.get_items()
    del_id = int(request.form['del_id'])
    delete_item(del_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
