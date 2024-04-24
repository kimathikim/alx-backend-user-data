#!/usr/bin/env python3
"""This module encrypts password using bcrypt."""
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import bcrypt
from user import User


def _hash_password(password: str) -> str:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


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
            return (self._db.add_user(email, h_password))