from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import current_user
from . import antragsteller
from app.common.models import Nachricht
import os
from shutil import rmtree
from run import app
from app import db
from zipfile import ZipFile
from flask_login import login_required
from app.rest import postJsonJson, getIdJson, \
    bauantrag_load,\
    bauantrag_info


@antragsteller.route('/', methods=['GET'])
def index():
    bauantraege = Nachricht.query.filter_by(antragstellerID=current_user.id)
    return render_template("app/antragsteller/start.html", bauantraege=bauantraege)


@antragsteller.route('/upload', methods=['POST'])
def upload():
    r = request

    file = request.files['file']

    nachricht = Nachricht()
    nachricht.filename = file.filename
    db.session.add(nachricht)
    db.session.flush()

    repo_path = os.path.abspath(app.root_path + "/../bauantraege/")
    nachricht.path = os.path.join(repo_path, str(nachricht.id)) + "/"
    print(nachricht.path)

    store_path = os.path.join(nachricht.path, file.filename)
    print(store_path)

    if not os.path.exists(os.path.dirname(store_path)):
        os.makedirs(os.path.dirname(store_path))

    file.save(os.path.join(nachricht.path, file.filename))

    content_path = os.path.join(nachricht.path, "content")
    if not os.path.exists(os.path.dirname(content_path)):
        os.makedirs(os.path.dirname(content_path))

    with ZipFile(store_path, 'r') as xbau_zip:
        try:
            xbau_zip.extractall(content_path)
        except Exception as e:
            print(e)

    index_exists = os.path.exists(os.path.join(content_path, 'index.xbau'))
    if not index_exists:
        return 'Keine Index-Datei (index.xbau) enthalten', 404

    data = {"path": os.path.join(nachricht.path, "content"), "loadedId": nachricht.ifcloadId}
    # r = requests.post(link, json=data, headers=headers)
    r = postJsonJson(bauantrag_load, data)
    answer = r.json()
    nachricht.ifcloadId = answer["id"]

    if r.status_code is 201:
        r = getIdJson(bauantrag_info, answer['id'])
        answer = r.json()

        nachricht.nachrichtentyp = answer['nachrichtentyp']
        nachricht.bezeichnung = answer['bezeichnung']
        nachricht.antragstellerID = current_user.id
        nachricht.status = "erstellt"

        db.session.add(nachricht)
        db.session.commit()



    response = {}
    response['bauantrag_id'] = nachricht.id

    return jsonify(response)


@antragsteller.route('bauantrag/einreichen/<id>', methods=['GET'])
def einreichen(id):
    bauantrag = Nachricht.query.filter_by(id=id, antragstellerID=current_user.id).first()

    bauantrag.status = 'eingereicht'
    db.session.add(bauantrag)
    db.session.commit()

    return redirect("/", code=302)
