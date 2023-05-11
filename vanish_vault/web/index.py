from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_login import login_required, login_user, logout_user, current_user

from vanish_vault.libs import utils
from vanish_vault.forms.share import ShareForm
from . import web


@web.route('/', methods=['GET', 'POST'])
def index_handler():
    context = {
        'valid_time_minutes': current_app.config['VALIDE_TIME_MINUTES']
    }
    form = ShareForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        secret_key = form.secret_key.data
        valid_time = form.valid_time.data
        user = current_user
        if not user or not user.is_authenticated:
            user_id = 0
        else:
            user_id = user.id
        next_id = utils.save_content_using_mysql(
            content, secret_key, user_id, int(valid_time) * 60)
        return redirect(url_for('web.share_handler_get', key=next_id))

    return render_template('home.html', **context, form=form)


@web.post('/detail')
def detail_handler():
    # TODO form check
    id = request.form.get('id')
    key = request.form.get('key')
    content = utils.get_decrypted_content2(id, key)
    if not content:
        flash(f'消息【{id}】密码不正确!!', category='error')
        return redirect(url_for('web.share_handler_get', key=id))
    else:
        context = {'id': id, 'content': content}
        utils.delete_content(id)

    return render_template('detail.html', **context)


@web.get('/share/<key>')
def share_handler_get(key):
    # TODO check id 是否存在
    context = {'id': key}
    if not utils.is_key_exist(key):
        context['error'] = '消息不存在!!'
    return render_template('share_result.html', **context)
