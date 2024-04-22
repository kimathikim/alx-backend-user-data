#!/usr/bin/env python3
"""Ths module defines the basic_auth class"""

import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """This class defines all the function for encoding and decoding
    user details"""

    def __init__(self) -> None:
        self._db = None
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """This method extracts the base64 authorization header"""
        if (
            authorization_header is None
            or isinstance(authorization_header, str) is False
        ):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """This modue decoded base64 data"""
        if (
            base64_authorization_header is None
            or isinstance(base64_authorization_header, str) is False
        ):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode(
                "\
            utf-8"
            )
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """this function returns the user email and password"""
        if (
            decoded_base64_authorization_header is None
            or isinstance(decoded_base64_authorization_header, str) is False
        ):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header.split(":")[1]
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar(
        "User"
    ):
        """returns the User instance based on his email and password"""
        if (
            not user_email
            or not isinstance(user_email, str)
            or not user_pwd
            or not isinstance(user_pwd, str)
        ):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """overloads Auth and
        retrieves the User instance for a request
        """
        try:
            header = self.authorization_header(request)
            base64_h = self.extract_base64_authorization_header(header)
            decode_h = self.decode_base64_authorization_header(base64_h)
            credents = self.extract_user_credentials(decode_h)
            return self.user_object_from_credentials(credents[0], credents[1])
        except Exception:
            return None
