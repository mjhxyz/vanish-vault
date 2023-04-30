from flask import Blueprint, render_template, request, redirect

from vanish_vault.libs import utils

index = Blueprint('index', __name__)


@index.get('/')
def index_handler():
    return render_template('home.html')


@index.get('/share/<id>')
def share_hanlder_get(id):
    # TODO check id 是否存在
    context = {'id': id}
    if not utils.is_id_exist(id):
        context['error'] = '消息不存在!!'
    return render_template('share_result.html', **context)


@index.post('/share')
def share_handler():
    # TODO form check
    content = request.form.get('content')
    key = request.form.get('key')
    encrypted_content = utils.encrypt(content, key)
    next_id = utils.save_content(encrypted_content, key)
    return redirect(f'/share/{next_id}')
