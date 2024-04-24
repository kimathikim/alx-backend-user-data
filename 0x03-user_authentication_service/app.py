#!/usr/bin/env python3
"""Flask application"""

from flask import Flask, jsonify, request
from auth import Auth

auth = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def test():
    """This is a test route:"""
    return jsonify({"message": "Bienvenue"})


@app.route("/user", methods=["POST"], strict_slashes=False)
def register_user():
    """Register a new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
