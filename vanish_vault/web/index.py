from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_login import login_required

from vanish_vault.libs import utils
from . import web


@web.get('/')
def index_handler():
    context = {
        'valid_time_minutes': current_app.config['VALIDE_TIME_MINUTES']
    }
    return render_template('home.html', **context)


@web.post('/detail')
def detail_handler():
    # TODO form check
    id = request.form.get('id')
    key = request.form.get('key')
    content = utils.get_decrypted_content(id, key)
    if not content:
        flash(f'消息【{id}】密码不正确!!', category='error')
        return redirect(url_for('web.share_hanlder_get', id=id))
    else:
        context = {'id': id, 'content': content}
        utils.delete_content(id)

    return render_template('detail.html', **context)


@web.get('/share/<id>')
def share_hanlder_get(id):
    # TODO check id 是否存在
    context = {'id': id}
    if not utils.is_id_exist(id):
        context['error'] = '消息不存在!!'
    return render_template('share_result.html', **context)


@web.post('/share')
def share_handler():
    # TODO form check
    content = request.form.get('content')
    key = request.form.get('key')
    valid_time = request.form.get('valid_time')
    next_id = utils.save_content(content, key, int(valid_time) * 60)
    return redirect(f'/share/{next_id}')
