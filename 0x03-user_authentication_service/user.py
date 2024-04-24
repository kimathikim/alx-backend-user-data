#!/usr/bin/env python3
"""This module provides the User class for the database."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    A class representing a user in a database.

    Attributes:
    - id (int): The unique identifier for the user.
    - email (str): The email address of the user.
    - hashed_password (str): The hashed password of the user.
    - session_id (str): The session ID of the user, if logged in.
    - reset_token (str): The reset token for the user, if requested.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
