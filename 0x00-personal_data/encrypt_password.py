#!/usr/bin/env python3
"""This module has a function for encrypting user password"""

import base64
import bcrypt
import hashlib


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.

    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if hashed password is the same as the original
        password

        Return true if they are the same otherwise false
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
