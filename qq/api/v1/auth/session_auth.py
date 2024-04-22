#!/usr/bin/env python3
"""This module contains the SessionAuth class"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None or isinstance(user_id, str) is False:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or isinstance(session_id, str) is False:
            return None
        return self.user_id_by_session_id.get(session_id)
