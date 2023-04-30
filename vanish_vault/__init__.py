from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('vanish_vault.config.secure')
    app.config.from_object('vanish_vault.config.setting')

    register_blueprint(app)
    return app


def register_blueprint(app):
    from vanish_vault.web.index import index
    app.register_blueprint(index)
