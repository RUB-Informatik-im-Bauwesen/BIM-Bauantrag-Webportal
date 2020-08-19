from flask import current_app as app
import requests


bauantrag_load = app.config['REST_SERVICE_URL'] + "/bauantrag/load"
bauantrag_info = app.config['REST_SERVICE_URL'] + "/bauantrag/getInfo"
bauantrag_data = app.config['REST_SERVICE_URL'] + "/bauantrag/getData"
formellePruefung_update = app.config['REST_SERVICE_URL'] + "/formellePruefung/update"
formellePruefung_data = app.config['REST_SERVICE_URL'] + "/formellePruefung/data"


def postJsonJson(link, data):
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    r = requests.post(link, json=data, headers=headers)
    return r


def getIdJson(link, id):
    r = requests.get(link+"/"+id)
    return r
