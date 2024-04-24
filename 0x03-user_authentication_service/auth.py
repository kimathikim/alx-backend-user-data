#!/usr/bin/env python3
"""This module encrypts password using bcrypt."""

import bcrypt


def _hash_password(password: str) -> str:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
