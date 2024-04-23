#!/usr/bin/env python3
"""This modele contans the class for sessioin expiration authentication"""

from os import getenv

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """This class defines the all the methods form session expiration"""

    def __init__(self):
        """This is the constructor for the session expiration class"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """This method overloads the same function of session_auth class"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """THis method overloads the same function of session_auth class"""
        if not session_id:
            return None
        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if "created_at" not in session_dict:
            return None
        delta = timedelta(seconds=self.session_duration)
        if session_dict["created_at"] + delta < datetime.now():
            return None
        return session_dict["user_id"]
