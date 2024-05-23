#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.getenv("AUTH_TYPE") == "auth":
    auth = Auth()
if os.getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
if os.getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()
if os.getenv("AUTH_TYPE") == "session_exp_auth":
    auth = SessionExpAuth()
if os.getenv("AUTH_TYPE") == "session_db_auth":
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """Method that runs before each request to
        handle authentication.
    """
    if not auth:
        return  # No auth required

    # Check if the request path requires authentication
    if auth.require_auth(
        request.path,
        [
            '/api/v1/status/', '/api/v1/unauthorized/',
            '/api/v1/forbidden/', '/api/v1/auth_session/login/'
        ]
    ):
        if (
            not auth.authorization_header(request) and
            not auth.session_cookie(request)
        ):
            abort(401)  # Unauthorized
        if not auth.current_user(request):
            abort(403)  # Forbidden
    request.current_user = auth.current_user(request)


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
