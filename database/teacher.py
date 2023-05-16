from database.postgres_utils import exec_commit, exec_get_one, exec_get_all
from database.db_utils import hash_password
import psycopg2


"""
all the functions a teacher user will call
"""


def create_teacher(username, password):
    """
    attempts to add record to teacher table if username is unique
    teachers are created with a unique id generated, first and last name set to empty strings

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
    return exec_get_one(query, (username, hash_password(password)))


def update_teacher(teacher_id, first_name, last_name):
    """
    updates the teachers first and last name

    :param teacher_id: an int
    :param first_name: a string
    :param last_name: a string
    """
    query = """
    UPDATE teachers
    SET first_name = %s, last_name = %s
    WHERE id = %s;
    """
    exec_commit(query, (first_name, last_name, teacher_id))


def delete_teacher(teacher_id, password):
    """
    deletes a teacher from the table

    :param teacher_id: an int
    :param password: a string that gets hashed
    """
    query = """
    DELETE FROM teachers
    WHERE id = %s AND password = %s;
    """
    exec_commit(query, (teacher_id, hash_password(password)))


def create_class(title, teacher_id):
    """
    creates a class for a teacher with a given title

    :param title: a string
    :param teacher_id: an int
    """
    query = """
    INSERT INTO classes (title, teacher_id)
    VALUES (%s, %s);
    """
    exec_commit(query, (title, teacher_id))


def get_classes(teacher_id):
    """
    gets classes associated with the given teacher id
    :param teacher_id: an int
    :return: a list of tuples
    """
    query = """
    SELECT id, title
    FROM classes
    WHERE teacher_id = %s;
    """
    results = exec_get_all(query, (teacher_id,))
    return results


def update_class(class_id, title):
    """
    updates the title of the class

    :param class_id: an int
    :param title: a string
    """
    query = """
    UPDATE classes
    SET title = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, class_id))


def delete_class(class_id):
    """
    deletes a class from the table

    :param class_id: an int
    """
    query = """
    DELETE FROM classes
    WHERE id = %s;
    """
    exec_commit(query, (class_id,))
