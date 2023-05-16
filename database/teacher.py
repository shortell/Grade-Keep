from database.postgres_utils import exec_commit, exec_get_all
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


def get_teacher(username, password):
    """
    gets a teacher that matches the given username and hashed password

    :param username: a string
    :param password: a string that gets hashed
    :returns: a list with a single tuple that will have one teacher if a match is found or empty if not
    """
    query = """
    SELECT id, first_name, last_name
    FROM teachers
    WHERE username = %s AND password = %s;
    """
    return exec_get_all(query, (username, hash_password(password)))


def update_teacher(id, first_name, last_name):
    """
    updates the teachers first and last name

    :param id: an int
    :param first_name: a string
    :param last_name: a string
    """
    query = """
    UPDATE teachers
    SET first_name = %s, last_name = %s
    WHERE id = %s;
    """
    exec_commit(query, (first_name, last_name, id))
