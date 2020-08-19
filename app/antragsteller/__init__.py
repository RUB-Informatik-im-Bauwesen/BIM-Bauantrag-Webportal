from flask import Blueprint

antragsteller = Blueprint('antragsteller', __name__)

from . import views