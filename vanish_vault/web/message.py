from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required

from vanish_vault.web import web
from vanish_vault.models.message import Message
from vanish_vault.libs import utils


@login_required
@web.route('/message/list')
def message_list():
    messages = Message.query.all()
    for message in messages:
        message.remaining = utils.to_remaining_time(message.expire_at)
    return render_template('message.html', messages=messages)
