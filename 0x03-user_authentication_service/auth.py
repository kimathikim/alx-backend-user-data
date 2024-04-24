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

    def get_user_from_session_id(self, session_id: str) -> str:
        """This function returns the user by session"""

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session

        Args:
            user_id (int): user id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token

        Args:
            email (str): user email

        Raises:
            ValueError: if not found user

        Returns:
            str: reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update password

        Args:
            reset_token (str): reset token
            password (str): user password

        Raises:
            ValueError: if not found user
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id, hashed_password=_hash_password(password), reset_token=None
            )
        except NoResultFound:
            raise ValueError
