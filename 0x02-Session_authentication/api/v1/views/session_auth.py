#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login():
    """handle session login"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
        
    try:
        users = User.search()
    except Exception:
        return jsonify({"error": "no user found for this email"}), 400
    if not User.count() or not len(users):
        return jsonify({"error": "no user found for this email"}), 400
    for user in users:
        if user.email == email:
            if not user.is_valid_password(password):
                return jsonify({"error": "wrong password"}), 401
            else:
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                cookie_name = os.getenv("SESSION_NAME")
                response = make_response(jsonify(user.to_json()))
                response.set_cookie(cookie_name, session_id)
                return response
    return jsonify({"error": "no user found for this email"}), 400


@app_views.route(
        "/auth_session/logout", methods=["DELETE"],
        strict_slashes=False
)
def session_logout():
    """handle session logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
