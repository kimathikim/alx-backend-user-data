#!/usr/bin/env python3
"""This module has the sessionAuth class"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """This class defines all the function for session Authntication"""

    def __init__(self):
        """This is the constructor for the sessionAuth class"""
        super().__init__()
