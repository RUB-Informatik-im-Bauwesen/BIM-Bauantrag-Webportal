from flask import Blueprint

bauantrag = Blueprint('bauantrag', __name__, template_folder='../../templates')

from . import views