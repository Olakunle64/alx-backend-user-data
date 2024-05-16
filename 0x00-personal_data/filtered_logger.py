#!/usr/bin/env python3
"""This module has a function called <filter_datum>
    that returns the log message obfuscated
"""

from typing import List
import re
import logging
import mysql.connector
import os

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
        ) -> str:
    """This function returns the log message obfuscated"""
    for field in fields:
        message = re.sub(rf'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This function returns the log message obfuscated"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """This function returns a logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """This function returns a connector to a database"""
    try:
        db_connector = mysql.connector.connect(
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME', 'holberton'),
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''))
        return db_connector
    except mysql.connector.Error as err:
        # print(f"Error: {err}")
        return None


def main() -> None:
    """Main function that retrieves and displays filtered user data"""
    db = get_db()
    if db is None:
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    fields_to_filter = ['name', 'email', 'phone', 'ssn', 'password']
    separator = '; '

    for row in rows:
        message = '; '.join([
            f"{key}={value}" for key, value in row.items()
        ])
        filtered_message = filter_datum(
            fields_to_filter, '***', message, separator
        )
        log_message = f"[HOLBERTON] user_data INFO {filtered_message}"
        print(log_message)

    cursor.close()
    db.close()
