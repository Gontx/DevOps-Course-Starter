from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run()
