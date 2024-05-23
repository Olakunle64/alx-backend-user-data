#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    """A UserSession class that inherit from Base"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialiazing"""
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
