from database.postgres_utils import exec_commit, exec_get_one, exec_get_all
from database.db_utils import hash_password
import psycopg2


"""
all the functions a teacher user will call
"""

# teachers capabilities to control their own profile


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

# teachers capabilities to control classes


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
    WHERE teacher_id = %s
    ORDER BY title ASC;
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

# teachers capabilities to control assignments


def create_assignment(title, instructions, class_id):
    """
    creates an assignment with a name and instructions attached to a certain record in the classes table

    :param title: a string
    :param instructions: a string
    :param class_id: an int
    """
    query = """
    INSERT INTO assignments (title, instructions, class_id)
    VALUES (%s, %s, %s)
    """
    exec_commit(query, (title, instructions, class_id))


def get_assignments(class_id):
    """
    gets all the assignments from the referenced class

    :param class_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT id, title
    FROM assignments
    WHERE class_id = %s
    ORDER BY title ASC;
    """
    return exec_get_all(query, (class_id,))


def get_assignment(assignment_id):
    """
    get an assignment by its id

    :param assignment_id: an int
    :returns: a tuple
    """
    query = """
    SELECT id, title, instructions
    FROM assignments
    WHERE id = %s;
    """
    return exec_get_one(query, (assignment_id,))


def update_assignment(assignment_id, title, instructions):
    """
    updates the title and instructions of a given assignment

    :param assignment_id: an int
    :param title: a string
    :param instructions: a string
    """
    query = """
    UPDATE assignments
    SET title = %s, instructions = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, instructions, assignment_id))


def delete_assignment(assignment_id):
    """
    deletes the assignment attached to the id

    :param assignment_id: an int
    """
    query = """
    DELETE FROM assignments
    WHERE id = %s;
    """
    exec_commit(query, (assignment_id,))

# teachers capabilities to view submissions


def get_submissions(assignment_id):
    """
    get submissions by an assignment id

    :param assignment_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT submissions.id, assignments.title, students.last_name, students.first_name
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE assignment_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (assignment_id,))


def get_submission(submission_id):
    """
    get submissions by an assignment id

    :param assignment_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT submissions.id, assignments.title, submissions.response, students.last_name, students.first_name
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE submissions.id = %s;
    """
    return exec_get_one(query, (submission_id,))

# teachers capabilities to view students


def get_students(class_id):
    """
    select all students from a given class

    :param class_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT enrollments.id, students.last_name, students.first_name
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    WHERE enrollments.class_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (class_id,))


def get_student(enrollments_id):
    """
    select a students from a given class

    :param class_id: an int
    :returns: a tuple
    """
    query = """
    SELECT enrollments.id, students.last_name, students.first_name
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    WHERE enrollments.id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_one(query, (enrollments_id,))


def create_grade(title, total_points, enrollment_id, points_earned=None):
    """
    creates a grade for a given enrollment

    :param title: a string
    :param total_points: an int
    :param enrollment_id: an int
    """
    query = """
    INSERT INTO grades (title, points_earned, total_points, enrollment_id)
    VALUES(%s, %s, %s, %s);
    """
    exec_commit(query, (title, points_earned, total_points, enrollment_id))


def format_grades(results):
    formatted_results = []
    for entry in results:
        if entry[2] is None:
            formatted_results.append((entry[0], entry[1], entry[2]))
        else:
            formatted_results.append(
                (entry[0], entry[1], float(entry[2]) * 100))
    return formatted_results


def get_grades(enrollment_id):
    """
    gets grades of a certain student in a certain class

    :param enrollment_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT id, title, (points_earned / total_points)
    FROM grades
    WHERE enrollment_id = %s
    ORDER BY title ASC;
    """
    results = exec_get_all(query, (enrollment_id,))
    return format_grades(results)


def get_grade(grade_id):
    """
    gets a given grade

    :param grade_id: an int
    :returns: a tuple
    """
    query = """
    SELECT title, points_earned, total_points
    FROM grades
    WHERE id = %s;
    """
    result = exec_get_one(query, (grade_id,))
    if result[1] is None:
        return (result[0], result[1], float(result[2]))
    else:
        return (result[0], float(result[1]), float(result[2]))
