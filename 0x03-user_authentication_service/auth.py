#!/usr/bin/env python3
"""This module has a _hash_password function"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import uuid
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
    - password (str): The password to hash.

    Returns:
    - bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate a uuid and return the string implementation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initializing"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        if not email or not password:
            return
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate user's credentials"""
        try:
            user_exist = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        valid_paswd = bcrypt.checkpw(
            password.encode(), user_exist.hashed_password)
        if valid_paswd:
            return True
        return False

    def create_session(self, email: str) -> str:
        """create a session id to the email"""
        id = _generate_uuid()
        try:
            user_exist = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user_id = user_exist.id
        try:
            user_exist = self._db.update_user(user_id, session_id=id)
            return id
        except ValueError:
            return None

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """"get a user with the session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """destroy user's session_id by updating it to None"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generate rest password token of a user with the email
            and save it to the database
        """
        id = _generate_uuid()
        try:
            user_exist = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user_id = user_exist.id
        self._db.update_user(user_id, reset_token=id)
        return id

    def update_password(self, reset_token: str, password: str) -> None:
        """update user's password"""
        try:
            user_exist = self._db.find_user_by(reset_token=reset_token)
            hashed_paswd = _hash_password(password)
            self._db.update_user(
                user_exist.id, hashed_password=hashed_paswd,
                reset_token=None
            )
            return None
        except NoResultFound:
            raise ValueError
