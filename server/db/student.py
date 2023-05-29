import psycopg2

from .postgres_utils import exec_commit, exec_get_all, exec_get_one
from .db_utils import hash_password, timestamp_to_str, format_decimal

# student table function


def create_student(first_name, last_name, username, password):
    """
    Creates a new student entry in the database.

    Args:
        first_name (str): The first name of the student.
        last_name (str): The last name of the student.
        username (str): The username of the student.
        password (str): The password of the student.

    Returns:
        bool: True if the student was successfully created, False if a unique constraint 
        violation occurred.
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
    Retrieves student information based on the provided student ID.

    Args:
        student_id (int): The unique identifier of the student.

    Returns:
        tuple or None: A tuple containing the student's information, including their 
        ID, first name, last name, and username. Returns None if no student is found with the provided ID.
    """
    query = """
    SELECT id, first_name, last_name, username
    FROM students
    WHERE id = %s;
    """
    return exec_get_one(query, (student_id,))


def login(username, password):
    """
    Authenticates a student by verifying their username and password.

    Args:
        username (str): The username of the student.
        password (str): The password of the student.

    Returns:
        tuple or None: The ID of the authenticated student within a tuple if the login 
        credentials are correct. Returns None if the provided username and password combination is invalid.
    """
    query = """
    SELECT id
    FROM students
    WHERE username = %s AND password = %s;
    """
    return exec_get_one(query, (username, hash_password(password)))


def update_student(student_id, first_name, last_name, username, password):
    """
    Updates the information of a student in the database.

    Args:
        student_id (int): The ID of the student to be updated.
        first_name (str): The updated first name of the student.
        last_name (str): The updated last name of the student.
        username (str): The updated username of the student.
        password (str): The updated password of the student.

    Returns:
        bool: True if the student information was successfully updated, 
        False if a unique constraint violation occurred.
    """
    query = """
    UPDATE students
    SET first_name = %s, last_name = %s, username = %s, password = %s
    WHERE id = %s;
    """
    try:
        exec_commit(query, (first_name, last_name, username,
                            hash_password(password), student_id))
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def delete_student(student_id, password):
    """
    Deletes a student from the database.

    Args:
        student_id (int): The ID of the student to be deleted.
        password (str): The password of the student for authentication.

    Returns:
        None
    """
    query = """
    DELETE FROM students
    WHERE id = %s AND password = %s;
    """
    exec_commit(
        query, (student_id, hash_password(password)))

# course table functions


def get_courses(student_id):
    """
    Retrieves the list of courses enrolled by a student.

    Args:
        student_id (int): The ID of the student.

    Returns:
        list: A list of tuples, where each tuple represents a course with its 
        ID and title. If the student is not enrolled in any courses, an empty list is returned.
    """
    query = """
    SELECT courses.id, courses.title
    FROM enrollments
    INNER JOIN courses ON enrollments.course_id = courses.id
    WHERE enrollments.student_id = %s
    ORDER BY courses.title ASC;
    """
    return exec_get_all(query, (student_id,))


def get_course(course_id):
    """
    Retrieves information about a specific course based on the provided course ID.

    Args:
        course_id (int): The ID of the course.

    Returns:
        tuple or None: A tuple containing the course information, including its ID, 
        title, and description. Returns None if no course is found with the provided ID.
    """
    query = """
    SELECT id, title, description
    FROM courses
    WHERE id = %s;
    """
    return exec_get_one(query, (course_id,))


# submission table functions

def create_submission(response, assignment_id, student_id):
    """
    Creates a new submission for an assignment.

    Args:
        response (str): The response or content of the submission.
        assignment_id (int): The ID of the assignment for which the submission is created.
        student_id (int): The ID of the student who is making the submission.

    Returns:
        None
    """
    query = """
    INSERT INTO submissions (response, turned_in, assignment_id, student_id)
    VALUES (%s, %s, %s, %s)
    """
    now = timestamp_to_str()
    exec_commit(
        query, (response, now, assignment_id, student_id))


def get_submission(student_id, assignment_id):
    """
    Retrieves the submission details of a student for a specific assignment.

    Args:
        student_id (int): The ID of the student.
        assignment_id (int): The ID of the assignment.

    Returns:
        tuple or None: A tuple containing the submission details, including the response content
        and the timestamp when it was turned in. Returns None if no submission is found for the provided student and assignment.
    """
    query = """
    SELECT response, turned_in
    FROM submissions
    WHERE student_id = %s AND assignment_id = %s;
    """
    return exec_get_one(query, (student_id, assignment_id))


def update_submission(submission_id, response):
    """
    Updates the response content of a submission.

    Args:
        submission_id (int): The ID of the submission to be updated.
        response (str): The updated response content.

    Returns:
        None
    """
    query = """
    UPDATE submissions
    SET response = %s
    WHERE id = %s;
    """
    exec_commit(query, (response, submission_id))


def delete_submission(submission_id):
    """
    Deletes a submission from the database.

    Args:
        submission_id (int): The ID of the submission to be deleted.

    Returns:
        None
    """
    query = """
    DELETE FROM submissions
    WHERE id = %s;
    """
    exec_commit(query, (submission_id,))


# grades and scores table functions


def get_score_average_by_course(student_id, course_id):
    """
    Calculates and formats the average score percentage achieved by a student in a specific course.

    Args:
        student_id (int): The ID of the student.
        course_id (int): The ID of the course.

    Returns:
        float or None: The average score percentage as a float representation (e.g., "75.00%" for 75%).
        Returns None if no scores are found for the provided student and course.
    """
    query = """
    SELECT AVG(points_earned / grades.total_points)
    FROM scores
    INNER JOIN grades ON scores.grade_id = grades.id
    WHERE grades.course_id = %s AND scores.student_id = %s;
    """
    score_avg = exec_get_one(query, (course_id, student_id))
    return format_decimal(score_avg[0]) if score_avg is not None else score_avg


def get_grades(student_id, course_id):
    """
    Retrieves the grades and related information for a specific student in a given course.

    Args:
        student_id (int): The ID of the student.
        course_id (int): The ID of the course.

    Returns:
        list of tuples or None: A list of tuples representing each grade and its details,
        including the grade ID, title, percentage score achieved, and the timestamp when it 
        was posted. Returns None if no grades are found for the provided student and course.
    """
    query = """
    SELECT grades.id, grades.title, (scores.points_earned / grades.total_points), posted
    FROM grades
    INNER JOIN scores ON grades.id = scores.grade_id
    WHERE grades.course_id = %s AND scores.student_id = %s
    ORDER BY posted DESC;
    """
    return exec_get_all(query, (course_id, student_id))


def get_score(student_id, grade_id):
    """
    Retrieves the details of a specific score for a given student and grade.

    Args:
        student_id (int): The ID of the student.
        grade_id (int): The ID of the grade.

    Returns:
        tuple or None: A tuple representing the score details, including the score ID,
        grade title, points earned, total points possible, and any associated comment.
        Returns None if no score is found for the provided student and grade.
    """
    query = """
    SELECT scores.id, grades.title, scores.points_earned, grades.total_points, scores.comment
    FROM scores
    INNER JOIN grades ON scores.grade_id = grades.id
    WHERE scores.student_id = %s AND scores.grade_id = %s;
    """
    return exec_get_one(query, (student_id, grade_id))
