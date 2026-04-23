from flask import Blueprint

clerk = Blueprint('clerk', __name__, url_prefix='/clerk')

from . import routes