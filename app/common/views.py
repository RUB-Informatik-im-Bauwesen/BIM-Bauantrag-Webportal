from flask import render_template, send_file, abort, redirect, url_for
from . import bauantrag as bauantrag_blueprint
from .models import Nachricht
from flask_login import current_user
import os
from shutil import rmtree
from app import db

from app.rest import postJsonJson, getIdJson, \
    bauantrag_load, \
    bauantrag_data


@bauantrag_blueprint.route('/open/<id>', methods=['GET'])
def open(id):

    if current_user.activeRole == "Behörde":
        return redirect(url_for("behoerde.open", id=id))

    bauantrag = Nachricht.query.filter_by(id=id).first()

    data = {"path": os.path.join(bauantrag.path, "content"), "loadedId": bauantrag.ifcloadId}
    r = postJsonJson(bauantrag_load, data)
    answer = r.json()

    bauantrag.ifcloadId = answer["id"]

    if r.status_code is 201:
        r = getIdJson(bauantrag_data, answer["id"])
        answer = r.json()
        content = answer

    if current_user.activeRole == "Antragsteller":
        return render_template("app/antragsteller/open.html", bauantrag=bauantrag, ba_details=content)


@bauantrag_blueprint.route('/<id>', methods=['DELETE'])
def delete(id):

    bauantrag = Nachricht.query.filter_by(id=id).first()
    print(bauantrag)

    if bauantrag is None:
        return 'Resource not existing', 404

    if bauantrag.antragstellerID is not current_user.id:
        return 'No rights to delete the resource', 404

    if bauantrag.status is "erstellt":
        print('No rights to delete the resource')
        return 'No rights to delete the resource', 404


    path = os.path.abspath(bauantrag.path)
    print(path)

    if os.path.exists(path):
        rmtree(path)

    db.session.delete(bauantrag)
    db.session.commit()


    return '', 204


@bauantrag_blueprint.route('/download/<id>')
def static(id):

    ba = Nachricht.query.filter_by(id=id).first()

    print(ba)

    if ba is None:
        return "Id not found", 404

    if not (current_user.id is ba.antragsteller.id or current_user.activeRole is "Behörde"):
        return "No rights for downloading", 404

    resolve = os.path.abspath(os.path.join(ba.path, ba.filename))
    print(resolve)

    return send_file(resolve, as_attachment=True)