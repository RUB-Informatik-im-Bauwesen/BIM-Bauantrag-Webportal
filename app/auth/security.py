from itsdangerous import URLSafeTimedSerializer

from flask import current_app as app

with app.app_context():
    ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
