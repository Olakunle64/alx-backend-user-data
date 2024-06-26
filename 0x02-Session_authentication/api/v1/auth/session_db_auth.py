#!/usr/bin/env python3
"""SessionDBAuth Class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user import User
from models.user_session import UserSession
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """A SessionDBAuth that inherit from SessionExpAuth"""
    def create_session(self, user_id=None):
        """create a session id and save the user_id and
            session id to the database
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        newUserSession = UserSession()
        newUserSession.user_id = user_id
        newUserSession.session_id = session_id
        newUserSession.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get the user_id based on session_id in the database"""
        if not session_id or not UserSession.count():
            return None
        user = UserSession.search({"session_id": session_id})
        if not user:
            return None
        if self.session_duration <= 0:
            return user[0].user_id
        if not user[0].created_at:
            return None
        cr_at = user[0].created_at
        exp_date = cr_at + timedelta(seconds=self.session_duration)
        if exp_date < datetime.utcnow():
            return None
        return user[0].user_id

    def destroy_session(self, request=None):
        """Destroy UserSession based on the session_id from cookie"""
        if not request:
            return False
        cookie_value = self.session_cookie(request)
        if not cookie_value:
            return False
        if not self.user_id_for_session_id(cookie_value):
            return False
        user = UserSession.get(self.user_id_for_session_id(cookie_value))
        user.remove()
        UserSession.save()
        return True
