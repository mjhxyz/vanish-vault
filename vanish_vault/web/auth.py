from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from vanish_vault.web import web
from vanish_vault.forms.auth import RegisterForm, LoginForm
from vanish_vault.models.user import User
from vanish_vault.models.base import db


@web.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('web.index_handler'))


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
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 使用登录插件登录
            login_user(user, remember=True)
            next = request.args.get('next')
            # 防止重定向攻击
            if not next or not next.startswith('/'):
                next = url_for('web.index_handler')
            return redirect(next)
        else:
            flash('该用户不存在或密码错误')
    return render_template('auth/login.html', form=form)
