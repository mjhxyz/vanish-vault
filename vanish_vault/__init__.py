from flask import Flask
from flask_login import LoginManager

from vanish_vault.libs.redis_utils import rclient
from vanish_vault.models.base import db


login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('vanish_vault.config.secure')
    app.config.from_object('vanish_vault.config.setting')

    register_blueprint(app)
    rclient.init_app(app)

    # 注册登录插件
    login_manager.init_app(app)
    # 设置登录页面
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册 SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from vanish_vault.web import web
    app.register_blueprint(web)
