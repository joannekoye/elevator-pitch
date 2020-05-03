from flask import render_template
from app import app

@app.route('/')
def index():
    '''
    returns index and data
    '''
    title = 'Home - Elevator Pitch'
    return render_template('index.html', title = title)




