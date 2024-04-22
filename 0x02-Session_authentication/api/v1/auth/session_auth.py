#!/usr/bin/env python3
"""This module has the sessionAuth class"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """This class defines all the function for session Authntication"""

    user_id_by_session_id = {}

    def __init__(self):
        """This is the constructor for the sessionAuth class"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """This class creates a session id for the user"""
        if user_id is None or isinstance(user_id, str) is False:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
