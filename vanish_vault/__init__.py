from flask import Flask

from vanish_vault.libs.redis_utils import rclient
from vanish_vault.models.base import db


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('vanish_vault.config.secure')
    app.config.from_object('vanish_vault.config.setting')

    register_blueprint(app)
    rclient.init_app(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from vanish_vault.web import web
    app.register_blueprint(web)
