#!/usr/bin/env python3
"""SessionExpAuth Class"""
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class that inherit from SessionAuth class"""
    def __init__(self):
        """initializing"""
        try:
            duration = int(os.getenv("SESSION_DURATION"))
            self.session_duration = duration
            # print("session_duration: ", self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a sessionID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        value_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = value_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get the user_id that belongs to the session_id"""
        if not session_id:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")
        if not self.user_id_by_session_id.get(session_id).get("created_at"):
            return None
        cr_at = self.user_id_by_session_id.get(session_id).get("created_at")
        exp_date = cr_at + timedelta(seconds=self.session_duration)
        if exp_date < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
