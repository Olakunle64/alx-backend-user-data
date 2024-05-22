#!/usr/bin/env python3
"""SessionAuth Class"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """A SessionAuth class that inherits from Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a session ID for the user_id"""
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """get the current user"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy a session"""
        if not request:
            return False
        cookie_value = self.session_cookie(request)
        if not cookie_value:
            return False
        if not self.user_id_for_session_id(cookie_value):
            return False
        del self.user_id_by_session_id[cookie_value]
        return True
