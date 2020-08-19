from flask import Blueprint

behoerde = Blueprint('behoerde', __name__)

from . import views