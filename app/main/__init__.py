from flask import Blueprint, url_for, redirect
import os
from flask_login import login_required, logout_user, current_user


main = Blueprint('main', __name__, template_folder='../../templates')

from flask import send_file, render_template, jsonify, make_response


@main.route('/')
@login_required
def index():

    if current_user.activeRole == "Antragsteller":
        #return render_template('app/antragsteller/start.html')
        return redirect(url_for("antragsteller.index"))
    if current_user.activeRole == "Behörde":
        return redirect(url_for("behoerde.index"))
    return render_template('app/start.html')


@main.route('static/<path:filename>')
def static(filename):
    resolve = os.path.abspath(main.root_path+"/../../static/"+filename)
    return send_file(resolve)
