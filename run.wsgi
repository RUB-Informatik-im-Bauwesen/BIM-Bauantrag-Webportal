activate_this = '/var/www/webportal/venv/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0,'/var/www/webportal/')

sys.stdout = sys.stderr

from app import create_app

application = create_app('development')
