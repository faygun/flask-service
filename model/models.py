import datetime
from . import db

class AccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accessToken = db.Column(db.String(500), nullable=False)
    token_created = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    def __init__(self, accessToken):
        self.accessToken = accessToken
        self.token_created = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'accessToken': self.accessToken,
            'token_created': self.token_created,
        }

    def __repr__(self):
        return '<Token %r>', self.accessToken