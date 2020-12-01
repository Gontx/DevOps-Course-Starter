from todo_app.data.session_items import delete_item
from flask import Flask, render_template, request, url_for, redirect, session

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
    return redirect(url_for('index'))

@app.route('/itemStatus', methods = ['GET','POST'])
def itemStatus():
    item_id = int(request.form ['itemID'])
    item_status = request.form ['itemStatus']
    item = si.get_item(item_id)
    updatedItem = {'id': item_id,'status': item_status,'title': item['title']}
    si.save_item(updatedItem)
    return redirect(url_for('index'))

@app.route('/status_sortItems', methods = ['GET','POST'])
def status_sortItems():
    initial_items = si.get_items()
    final_items = sorted(initial_items, key = lambda item:item['status'])
    session['items'] = final_items
    return redirect(url_for('index'))

@app.route('/IDsortItems', methods = ['GET','POST'])
def IDsortItems():
    initial_items = si.get_items()
    final_items = sorted(initial_items, key = lambda item:item['id'])
    session['items'] = final_items
    return redirect(url_for('index'))

@app.route('/delItem', methods = ['GET','POST'])
def delItem():
    del_ID = int(request.form['delID'])
    session['items'] = delete_item(del_ID)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
