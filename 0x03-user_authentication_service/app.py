#!/usr/bin/env python3
"""Flask application"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def test():
    """This is a test route:"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Register a new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """login

    Returns:
        str: messege
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logs out by deleting the session from the user and the cookie"""
    session_id = request.cookie.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """profile

    Return:
       str: message
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """get_reset_password

    Return:
       str: message
    """
    email = request.form.get("email")
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """update_password

    Return:
       str: message
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_psw = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify(
            {
                "email": f"{email}",
                "message": "\
        Password updated",
            }
        ), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
