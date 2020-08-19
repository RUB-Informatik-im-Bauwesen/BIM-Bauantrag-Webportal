from sqlalchemy.orm import relationship, backref
from app import db

from app.models import User


class Nachricht(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    antragstellerID = db.Column(db.Integer, db.ForeignKey('users.id'))
    antragsteller = relationship(User, foreign_keys=[antragstellerID])

    status = db.Column(db.String(128))
    bezeichnung = db.Column(db.Text)
    ifcloadId = db.Column(db.String(128))
    nachrichtentyp = db.Column(db.String(128))

    vorgaenger_id = db.Column(db.Integer, db.ForeignKey('nachricht.id'))
    vorgaenger = relationship('Nachricht',
                              remote_side=[id],
                              uselist=False,
                              foreign_keys=[vorgaenger_id],
                              backref=backref('nachfolger'))
