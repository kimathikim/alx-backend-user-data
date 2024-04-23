#!/usr/bin/env python3
"""tnis module has has the routes for the session authentication"""

from os import getenv

from flask import jsonify, request
from models.user import User

from api.v1.views import app_views


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """This route should login the user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.auth.session_auth import SessionAuth

        session_id = SessionAuth().create_session(user.id)
        out = jsonify(user.to_json())
        session_name = getenv("SESSION_NAME")
        out.set_cookie(session_name, session_id)
        return out
    return jsonify({"error": "no user found for this email"}), 404


@app_views.route(
    "/auth_session/logout\
",
    methods=["DELETE"],
    strict_slashes=False,
)
def logout():
    """This route should logout the user"""
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    return jsonify({}), 404
