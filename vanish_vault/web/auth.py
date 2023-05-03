from flask import render_template, request, redirect, url_for

from vanish_vault.web import web
from vanish_vault.forms.auth import RegisterForm
from vanish_vault.models.user import User
from vanish_vault.models.base import db


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))

    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'
