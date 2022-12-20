import os, requests
from flask_sqlalchemy import SQLAlchemy
from model.models import AccessToken
from utility import config
from utility.encode_decode import encodeString

def getTokenFromDB(db:SQLAlchemy):
    tokenEntity = db.session.execute(db.select(AccessToken)).scalar()
    return tokenEntity

def getToken(db:SQLAlchemy):
    tokenEntity = db.session.execute(db.select(AccessToken)).scalar()

    print("getToken was called.")
    return tokenEntity

def deleteToken(db, existToken):
    db.session.delete(existToken)
    db.session.commit()

def generateToken(db:SQLAlchemy, existToken = None):
    authHeaders= {
        "Content-Type":"application/x-www-form-urlencoded",
        "Authorization":f"Basic {encodeString(config.CLIENT_ID + ':' + config.CLIENT_SECRET)}"
    }

    authBody={
        "grant_type":"client_credentials",
        "scope" : "access_token_only"
    }
    
    response = requests.post(f"{config.BASE_URI}{config.AUTH_URI}", headers = authHeaders, data = authBody)

    tokenData = response.json()


    if existToken:
        db.session.delete(existToken)

    tokenEntity = AccessToken(accessToken = tokenData["access_token"])

    db.session.add(tokenEntity)

    db.session.commit()
    
    print("generateToken was called.")

    return tokenEntity