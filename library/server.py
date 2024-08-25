from urllib.parse import unquote
from urllib.parse import quote
from pymongo import MongoClient
from flask import make_response
from flask import jsonify
from flask import session
from http import HTTPStatus

import hashlib
import jwt
import os



def encode_alias(alias: str):
    return quote(alias.lower())


def decode_alias(alias: str):
    return unquote(alias).lower()


def hash_password(plain_password: str):
    plain_password = plain_password.strip()
    return hashlib.sha512(plain_password.encode("utf-8")).hexdigest()


def create_response(success=True, message="", data={}, status=HTTPStatus.OK):
    response = make_response(
        jsonify({
            "success": success,
            "message": message,
            "data": data,
        }),
        status
    )
    return response


def create_token(payload):
    SECRET=os.getenv("FLASK_SECRET")
    ALGORITHM="HS256"
    encoded = jwt.encode(
        payload=payload,
        key=SECRET,
        algorithm=ALGORITHM
    )
    return encoded


def verify_token(token):
    SECRET=os.getenv("FLASK_SECRET")
    ALGORITHM="HS256"
    try:
        decoded = jwt.decode(
            jwt=token,
            key=SECRET,
            algorithms=ALGORITHM
        )
        session["username"] = decoded["username"]
        return True
    except Exception as e:
        print(e)
        return False


