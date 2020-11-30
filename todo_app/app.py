from flask import Flask, render_template, request, url_for, redirect

from todo_app.flask_config import Config
from todo_app.data import session_items as si

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    items = si.get_items()
    return render_template('index.html', items =items)

@app.route('/form', methods = ['GET','POST'])
def form():
    title = request.form ['title']
    si.add_item(title)
    items = si.get_items()
    return render_template('index.html', items = items)

@app.route('/itemStatus', methods = ['GET','POST'])
def itemStatus():
    item_id = request.form ['itemID']
    item_status = request.form ['itemStatus']
    item = si.get_item(item_id)
    updatedItem = {'id': item_id, 'title': item.title, 'status': item_status}
    si.save_item(updatedItem)
    items = si.get_items()
    return render_template('index.html', items = items)

@app.route('/sortItems', methods = ['GET','POST'])
def sortItems():
    initial_items = si.get_items()
    final_items = sorted(initial_items, key = lambda item:item['status'])
    for item in final_items:
        si.save_item(item)
    items = si.get_items
    return render_template('index.html', items = items)

if __name__ == '__main__':
    app.run()
