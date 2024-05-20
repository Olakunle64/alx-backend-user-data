#!/usr/bin/env python3
"""Authentication Class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require path"""
        if not path or not excluded_paths or not len(excluded_paths):
            return True
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if not request or not request.args.get("Authorization"):
            return None
        else:
            return request.args.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None