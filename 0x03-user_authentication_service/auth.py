#!/usr/bin/env python3
"""This module encrypts password using bcrypt."""

from sqlalchemy.orm.exc import NoResultFound
from db import DB
import bcrypt
from user import User
import uuid


def _hash_password(password: str) -> str:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This function registers the user and stores their
        details in the database"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            h_password = _hash_password(password)
            return self._db.add_user(email, h_password)

    def valid_login(self, email: str, password: str) -> bool:
        """This function checks if the user login is valid"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """This function creates a session ID for the user"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
