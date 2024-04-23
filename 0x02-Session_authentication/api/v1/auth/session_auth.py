#!/usr/bin/env python3
"""This module has the sessionAuth class"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """This class returns the user id by session id"""
        if session_id is None or isinstance(session_id, str) is False:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """This method returns the user based on there cookie value user_id"""
        session_id = Auth().session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User().get(user_id)
        return user
