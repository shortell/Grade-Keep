import hashlib
import datetime
from .postgres_utils import exec_sql_file


def create_database():
    """
    executes the queries in sql/create_schema.sql to create all the tables in the database
    """
    exec_sql_file("sql/create_schema.sql")


def delete_database():
    """
    executes the queries in sql/drop_schema.sql to drop all the tables in the database
    """
    exec_sql_file("sql/drop_schema.sql")


def initialize_database():
    """
    drops all tables in the database then creates them again
    used for testing purposes
    """
    delete_database()
    create_database()


def seed_database():
    """
    seeds the database for testing purposes
    """
    exec_sql_file("sql/seed_database.sql")


def hash_password(password):
    """
    hashes a password

    :param password: a string
    :returns: hashed string
    """
    tokens = bytes(password.encode())
    return hashlib.sha256(tokens).hexdigest()


def timestamp_to_str(timestamp=datetime.datetime.now()):
    """
    gets the current date and time

    :returns: a string"""
    return timestamp.strftime("%x %X")


def format_decimal(input, multiplier=100):
    if input is not None:
        return round(float(input) * multiplier, 2)
    return None
