from flask import Blueprint, render_template, request, redirect, flash, url_for

from vanish_vault.libs import utils

index = Blueprint('index', __name__)


@index.get('/')
def index_handler():
    return render_template('home.html')


@index.post('/detail')
def detail_handler():
    # TODO form check
    id = request.form.get('id')
    key = request.form.get('key')
    content = utils.get_decrypted_content(id, key)
    if not content:
        flash(f'消息【{id}】密码不正确!!')
        return redirect(url_for('index.share_hanlder_get', id=id))
    else:
        context = {'id': id, 'content': content}

    return render_template('detail.html', **context)


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
    next_id = utils.save_content(content, key)
    return redirect(f'/share/{next_id}')
