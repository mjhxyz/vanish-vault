from flask import Blueprint, render_template, request, redirect

from vanish_vault.libs import utils

index = Blueprint('index', __name__)


@index.get('/')
def index_handler():
    return render_template('home.html')


@index.get('/share/<id>')
def share_hanlder_get(id):
    # TODO check id 是否存在
    return render_template('share_result.html', id=id)


@index.post('/share')
def share_handler():
    # TODO form check
    content = request.form.get('content')
    key = request.form.get('key')
    msg = utils.encrypt(content, key)
    return redirect(f'/share/{key}')
