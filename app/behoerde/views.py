from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import current_user
from . import behoerde
from app.common.models import Nachricht
import os
from shutil import rmtree

from app import db
from zipfile import ZipFile
from flask_login import login_required
from flask import current_app as app

from app.rest import postJsonJson, getIdJson, \
    bauantrag_load, \
    bauantrag_info, \
    bauantrag_data, \
    formellePruefung_update, \
    formellePruefung_data


@behoerde.route('/', methods=['GET'])
def index():
    bauantraege = Nachricht.query.filter_by(status="eingereicht")
    return render_template("app/behoerde/start.html", bauantraege=bauantraege)


@behoerde.route('open/<id>', methods=["GET"])
def open(id):
    bauantrag = Nachricht.query.filter_by(id=id).first()

    print(bauantrag.ifcloadId)

    data = {"path": os.path.join(bauantrag.path, "content"), "loadedId": bauantrag.ifcloadId}
    print(data)
    r = postJsonJson(bauantrag_load, data)
    answer = r.json()

    bauantrag.ifcloadId = answer["id"]

    if r.status_code is 201:
        r = getIdJson(bauantrag_data, answer["id"])
        answer = r.json()
        content = answer

    formellePruefung = {}

    if len(bauantrag.nachfolger) > 0:

        nachricht = bauantrag.nachfolger[0]

        data = {"path": os.path.join(nachricht.path, "content"), "loadedId": nachricht.ifcloadId}
        print(data)
        r = postJsonJson(formellePruefung_data, data)
        answer = r.json()

        print(answer)

        formellePruefung = {}

        if answer["befundBeteiligte"]:
            formellePruefung["befundBeteiligte"] = answer["befundBeteiligte"]
        if answer["befundBauvorhaben"]:
            formellePruefung["befundBauvorhaben"] = answer["befundBauvorhaben"]
        if answer["befundLokalisierung"]:
            formellePruefung["befundLokalisierung"] = answer["befundLokalisierung"]
        if answer["befundAnlageMangel"]:
            formellePruefung["befundAnlageMangel"] = answer["befundAnlageMangel"]
        if answer["befundAnlageFehlt"]:
            formellePruefung["befundAnlageFehlt"] = answer["befundAnlageFehlt"]
        if answer["befundAbweichung"]:
            formellePruefung["befundAbweichung"] = answer["befundAbweichung"]
        if answer["frist"]:
            formellePruefung["frist"] = answer["frist"]


    return render_template("app/behoerde/open.html", bauantrag=bauantrag, ba_details=content, formellePruefung=formellePruefung)


@behoerde.route('/formellePruefung/speichern', methods=['POST'])
def formellePruefungAbschicken():

    if not current_user.activeRole == "Behörde":
        return "Keine Berechtigung zur Ausführung dieser Operation", 404

    vorgaenger = Nachricht.query.filter_by(id=request.form.get('vorgaengerNachrichtId')).first()

    data = {}
    nachricht = None

    print(vorgaenger.nachfolger)

    if len(vorgaenger.nachfolger) > 0:
        nachricht = vorgaenger.nachfolger[0]
    else:
        nachricht = Nachricht()
        nachricht.vorgaenger = vorgaenger
        db.session.add(nachricht)
        db.session.flush()

        repo_path = os.path.abspath(app.root_path + "/../bauantraege/")
        nachricht.path = os.path.join(repo_path, str(nachricht.id))
        store_path = os.path.join(nachricht.path, 'content')+"/"
        if not os.path.exists(os.path.dirname(store_path)):
            oldmask = os.umask(000)
            os.makedirs(os.path.dirname(store_path), 0o775)
            os.umask(oldmask)

        nachricht.nachrichtentyp = "0201"
        nachricht.status = "erstellt"
        nachricht.filename = ""




    if request.form.get('toggleBeteiligte'):
        data["befundBeteiligte"] = request.form["textareaBeteiligte"]

    if request.form.get('toggleBauvorhaben'):
        data["befundBauvorhaben"] = request.form["textareaBauvorhaben"]

    if request.form.get('toggleLokalisierung'):
        data["befundLokalisierung"] = request.form["textareaLokalisierung"]

    if request.form.get('toggleAnlageMangel'):
        data["befundAnlageMangel"] = request.form["textareaAnlageMangel"]

    if request.form.get('toggleAnlageFehlt'):
        data["befundAnlageFehlt"] = request.form["textareaAnlageFehlt"]

    if request.form.get('toggleAbweichung'):
        data["befundAbweichung"] = request.form["textareaAbweichung"]

    #print (data)

    if request.form.get('frist'):
        data["frist"] = request.form["frist"]

    data['path'] = nachricht.path
    data['vorgaengerPath'] = vorgaenger.path


    postJsonJson(formellePruefung_update, data)

    db.session.commit()


    return redirect(url_for('bauantrag.open', id=vorgaenger.id))

