from flask import Flask

from vanish_vault.libs.redis_utils import rclient


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('vanish_vault.config.secure')
    app.config.from_object('vanish_vault.config.setting')

    register_blueprint(app)
    rclient.init_app(app)
    return app


def register_blueprint(app):
    from vanish_vault.web.index import index
    app.register_blueprint(index)
