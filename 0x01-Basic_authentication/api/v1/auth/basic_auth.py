#!/usr/bin/env python3
"""BasicAuth Class"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """A class that inherit from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """Extract base64 string from the authorization header value"""
        # print(authorization_header)
        if (
            not authorization_header or
            type(authorization_header) is not str
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split("Basic ")[-1].strip()

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """decode base64"""
        if (
            not base64_authorization_header or
            type(base64_authorization_header) is not str
        ):
            return None
        try:
            decoded_b64 = b64decode(base64_authorization_header)
        except Exception:
            return None
        else:
            return decoded_b64.decode("utf-8")

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """extract email and password from the user credentials"""
        if (
            not decoded_base64_authorization_header or
            type(decoded_base64_authorization_header) is not str
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        return (credentials[0].strip(), credentials[1].strip())

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """define a user instance from user's credentials"""
        if (
            not user_email or type(user_email) is not
            str or not user_pwd or type(user_pwd) is not str
        ):
            return None
        users = User.search()
        if not User.count() or not len(users):
            return None
        for user in users:
            if user.email == user_email:
                if not user.is_valid_password(user_pwd):
                    return None
                else:
                    return user
        return None
