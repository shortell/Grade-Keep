import hashlib
import datetime
from server.db import postgres_utils


def create_database():
    """
    executes the queries in sql/create_schema.sql to create all the tables in the database
    """
    postgres_utils.exec_sql_file("sql/create_schema.sql")


def delete_database():
    """
    executes the queries in sql/drop_schema.sql to drop all the tables in the database
    """
    postgres_utils.exec_sql_file("sql/drop_schema.sql")


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
    postgres_utils.exec_sql_file("sql/seed_database.sql")


def hash_password(password):
    """
    hashes a password
    
    :param password: a string
    :returns: hashed string
    """
    tokens = bytes(password.encode())
    return hashlib.sha256(tokens).hexdigest()


def current_timestamp():
    """
    gets the current date and time

    :returns: a string"""
    return datetime.datetime.now().strftime("%x %X")
