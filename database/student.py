import psycopg2

from database.postgres_utils import exec_get_one, exec_get_all, exec_commit
from database.db_utils import hash_password, current_timestamp

# student table function


def create_student(first_name, last_name, username, password):
    """
    attempts to add record to student table if username is unique
    student are created with a unique id generated, first and last name set to empty strings

    :param first_name: a string
    :param last_name: a string
    :param username: a string
    :param password: a string that gets hashed
    :returns: True if teacher is created and False otherwise
    """
    query = """
    INSERT INTO students (first_name, last_name, username, password)
    VALUES (%s, %s, %s, %s);
    """
    try:
        exec_commit(query, (first_name, last_name,
                    username, hash_password(password)))
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def get_student(student_id):
    """
    gets a student given their id

    :param student_id: an int
    :returns: a tuple
    """
    query = """
    SELECT id, first_name, last_name, username
    FROM students
    WHERE username = %s AND password = %s;
    """
    return exec_get_one(query, (student_id,))


def get_student(username, password):
    """
    gets a student that matches the given username and hashed password

    :param username: a string
    :param password: a string that gets hashed
    :returns: a tuple
    """
    query = """
    SELECT first_name, last_name, username
    FROM students
    WHERE username = %s AND password = %s;
    """
    return exec_get_one(query, (username, hash_password(password)))


def update_student(student_id, first_name, last_name):
    """
    updates the students first and last name

    :param student_id: an int
    :param first_name: a string
    :param last_name: a string
    """
    query = """
    UPDATE students
    SET first_name = %s, last_name = %s
    WHERE id = %s;
    """
    exec_commit(query, (first_name, last_name, student_id))


def delete_student(student_id, password):
    """
    deletes a student from the table

    :param student_id: an int
    :param password: a string that gets hashed
    """
    query = """
    DELETE FROM students
    WHERE id = %s AND password = %s;
    """
    exec_commit(query, (student_id, hash_password(password)))

# course table functions


def get_courses(student_id):
    """
    gets the courses a student is enrolled in

    :param student_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT courses.id, courses.title
    FROM enrollments
    INNER JOIN courses ON enrollments.course_id = courses_id
    WHERE enrollments.student_id = %s
    ORDER BY courses.title ASC;
    """
    return exec_get_all(query, (student_id,))


# submission table functions

def create_submission(response, assignment_id, student_id):
    """
    creates a submission with the given response, assignment id, and student id
    sets the turned in timestamp as the current date and time

    :param response: a string
    :param assignment_id: an int
    :param student_id: an int
    """
    query = """
    INSERT INTO submissions (response, turned_in, assignment_id, student_id)
    VALUES (%s, %s, %s, %s)
    """
    now = current_timestamp()
    exec_commit(query, (response, now, assignment_id, student_id))


def update_submission(submission_id, response):
    """
    updates the response of a submission

    :param submission_id: an int
    :param response: a string
    """
    query = """
    UPDATE submissions
    SET response = %s
    WHERE id = %s;
    """
    exec_commit(query, (response, submission_id))


def delete_submission(submission_id):
    """
    deletes a submission given a submission id
    :param submission_id: an int
    """
    query = """
    DELETE FROM submissions
    WHERE id = %s;
    """
    exec_commit(query, (submission_id,))
