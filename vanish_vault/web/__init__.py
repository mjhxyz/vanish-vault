from flask import Blueprint

web = Blueprint('web', __name__)

from vanish_vault.web import index
from vanish_vault.web import auth
