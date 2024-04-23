#!/Usr/bin/env python3
"""THis module defines the UserSession class"""

from model.base import Base


class UserSession(Base):
    """This class defines the uset session model"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
