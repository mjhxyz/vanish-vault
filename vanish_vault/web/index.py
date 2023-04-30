from flask import Blueprint, render_template

index = Blueprint('index', __name__)


@index.get('/')
def index_handler():
    return render_template('home.html')
