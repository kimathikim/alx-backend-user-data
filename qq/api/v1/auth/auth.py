#!/usr/bin/env python3
"""This module has the authentication routes"""

import os
from typing import TypeVar

SESSION_NAME = "_my_session_id"


class Auth:
    """THIS CLASS HAS THE AUTHENTICATION METHODS"""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """This method checks if the path requires authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != "/":
            path = path + "/"
        for excluded_path in excluded_paths:
            if excluded_path.endswith(
                "*\
            "
            ) and path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """This method returns the authorization header"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """This method returns the current user"""
        return None

    def session_cookie(self, request=None):
        """This method returns a cookie value"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
