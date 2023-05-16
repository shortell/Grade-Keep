from database.postgres_utils import exec_commit
from database.db_utils import hash_password
import psycopg2

def create_teacher(username, password):
    """
    attempts to add record to teacher table if username is unique
    unique id generated, first and last name set to empty strings
    
    :param username: a string
    :param password: a string that gets hashed
    :returns: True if teacher is created and False otherwise
    """
    query = """
    INSERT INTO teachers (username, password)
    VALUES (%s, %s);
    """
    try:
        exec_commit(query, (username, hash_password(password)))
        return True
    except psycopg2.errors.UniqueViolation:
        return False