import hashlib
from database.postgres_utils import exec_sql_file


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
    tokens = bytes(password.encode())
    return hashlib.sha256(tokens).hexdigest()


def get_current_datetime():
    return datetime.datetime.now().strftime("%x %X")
