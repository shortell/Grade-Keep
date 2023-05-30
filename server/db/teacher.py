from .postgres_utils import exec_commit, exec_get_all, exec_get_one, connect
from .db_utils import hash_password, timestamp_to_str, format_decimal
import psycopg2

# all the functions teacher users will be calling

# teacher table function


def create_teacher(first_name, last_name, username, password):
    """
    Creates a new teacher entry in the database.

    Args:
        first_name (str): The first name of the teacher.
        last_name (str): The last name of the teacher.
        username (str): The username of the teacher.
        password (str): The password of the teacher.

    Returns:
        bool: True if the teacher was successfully created, False if a unique constraint 
        violation occurred.
    """
    query = """
    INSERT INTO teachers (first_name, last_name, username, password)
    VALUES (%s, %s, %s, %s);
    """
    try:
        exec_commit(query, (first_name, last_name,
                            username, hash_password(password)))
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def get_teacher(teacher_id):
    """
    Retrieves teacher information based on the provided teacher ID.

    Args:
        teacher_id (int): The unique identifier of the teacher.

    Returns:
        tuple or None: A tuple containing the teacher's information, including their 
        ID, first name, last name, and username. Returns None if no teacher is found with the provided ID.
    """
    query = """
    SELECT id, first_name, last_name, username
    FROM teachers
    WHERE id = %s;
    """
    return exec_get_one(query, (teacher_id,))


def login(username, password):
    """
    Authenticates a teacher by verifying their username and password.

    Args:
        username (str): The username of the teacher.
        password (str): The password of the teacher.

    Returns:
        tuple or None: The ID of the authenticated teacher within a tuple if the login 
        credentials are correct. Returns None if the provided username and password combination is invalid.
    """
    query = """
    SELECT id
    FROM teachers
    WHERE username = %s AND password = %s;
    """
    return exec_get_one(query, (username, hash_password(password)))


def update_teacher(teacher_id, first_name, last_name, username, password):
    """
    Updates the information of a teacher in the database.

    Args:
        teacher_id (int): The ID of the teacher to be updated.
        first_name (str): The updated first name of the teacher.
        last_name (str): The updated last name of the teacher.
        username (str): The updated username of the teacher.
        password (str): The updated password of the teacher.

    Returns:
        bool: True if the teacher information was successfully updated, 
        False if a unique constraint violation occurred.
    """
    query = """
    UPDATE teachers
    SET first_name = %s, last_name = %s, username = %s, password = %s
    WHERE id = %s;
    """
    try:
        exec_commit(query, (first_name, last_name,
                            username, hash_password(password), teacher_id))
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def delete_teacher(teacher_id, password):
    """
    Deletes a teacher from the database.

    Args:
        teacher_id (int): The ID of the teacher to be deleted.
        password (str): The password of the teacher for authentication.

    Returns:
        None
    """
    query = """
    DELETE FROM teachers
    WHERE id = %s AND password = %s;
    """
    exec_commit(
        query, (teacher_id, hash_password(password)))

# student table function


def get_students(course_id):
    """
    Retrieves a list of students enrolled in a given course.

    This function is intended for teachers to use. It executes an SQL query to select all students
    from the specified course. The students are sorted by their last names in ascending order.

    Args:
        course_id (int): The ID of the course.

    Returns:
        list of tuples: A list of tuples containing the student ID, last name, and first name of each student.
    """
    query = """
    SELECT enrollments.id, students.last_name, students.first_name
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    WHERE enrollments.course_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (course_id,))


def get_student(enrollment_id):
    """
     Retrieves information about a student based on their enrollment ID.

    Args:
        enrollment_id (int): The enrollment ID of the student.

    Returns:
        tuple: A tuple containing the enrollment ID, last name, and first name of the student.
    """
    query = """
    SELECT enrollments.id, students.last_name, students.first_name
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    WHERE enrollments.id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_one(query, (enrollment_id,))


# course table functions

def create_course(title, description, teacher_id):
    """
    Creates a new course in the database.

    Args:
        title (str): The title of the course.
        description (str): A description of the course.
        teacher_id (int): The ID of the teacher assigned to the course.

    Returns:
        None
    """
    query = """
    INSERT INTO courses (title, description, teacher_id)
    VALUES (%s, %s, %s);
    """
    exec_commit(query, (title, description, teacher_id))


def get_courses(teacher_id):
    """
     Retrieves a list of courses taught by a specific teacher.

    Args:
        teacher_id (int): The ID of the teacher.

    Returns:
        list: A list of tuples containing the course ID and title of each course taught by the teacher.
    """
    query = """
    SELECT id, title
    FROM courses
    WHERE teacher_id = %s
    ORDER BY title ASC;
    """
    results = exec_get_all(query, (teacher_id,))
    return results


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


def update_course(course_id, title, description):
    """
    Updates the title and description of a course.

    Args:
        course_id (int): The ID of the course to update.
        title (str): The new title of the course.
        description (str): The new description of the course.

    Returns:
        None
        """
    query = """
    UPDATE courses
    SET title = %s, description = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, description, course_id))


def delete_course(course_id):
    """
    Deletes a course from the database based on the given course ID.

    Args:
        course_id (int): The ID of the course to delete.

    Returns:
        None
    """
    query = """
    DELETE FROM courses
    WHERE id = %s;
    """
    exec_commit(query, (course_id,))

# assignment table functions


def create_assignment(title, instructions, due, course_id):
    """
    Creates a new assignment and inserts it into the database.

    Args:
        title (str): The title of the assignment.
        instructions (str): The instructions for the assignment.
        due (datetime): The due date and time for the assignment.
        course_id (int): The ID of the course the assignment belongs to.

    Returns:
        None

    """
    query = """
    INSERT INTO assignments (title, instructions, due, course_id)
    VALUES (%s, %s, %s, %s)
    """
    exec_commit(query, (title, instructions, due, course_id))


# def __format_assignments(assignments):
#     """
#     helper function
#     Formats the assignment records into a specific format.

#     Args:
#         assignments (list): A list of assignment records, where each record is a tuple (title, instructions, due).

#     Returns:
#         list: A formatted list of assignment records, where each record is a tuple (title, instructions, formatted_due).
#     """
#     formatted = []
#     for record in assignments:
#         record = (record[0], record[1], record[2].strftime("%x %X"))
#         formatted.append(record)
#     return formatted


# def get_assignments(course_id):
#     """
#     Retrieves a list of assignments for a specific course.

#     Args:
#         course_id (int): The ID of the course.

#     Returns:
#         list: A list of formatted assignment records, where each record is a tuple (id, title, formatted_due).
#     """
#     query = """
#     SELECT id, title, due
#     FROM assignments
#     WHERE course_id = %s
#     ORDER BY due DESC;
#     """
#     assignments = exec_get_all(query, (course_id,))
#     return __format_assignments(assignments)


# def get_assignment(assignment_id):
#     """
#     Retrieves information about a specific assignment.

#     Args:
#         assignment_id (int): The ID of the assignment.

#     Returns:
#         tuple: A tuple containing the assignment ID, title, instructions, and formatted due date.
#     """
#     query = """
#     SELECT id, title, instructions, due
#     FROM assignments
#     WHERE id = %s;
#     """
#     assignment = exec_get_one(query, (assignment_id,))
#     return (assignment[0], assignment[1], assignment[2], assignment[3].strftime("%x %X"))


def update_assignment(assignment_id, title, instructions, due_date):
    """
    Updates the details of a specific assignment in the database.

    Args:
        assignment_id (int): The ID of the assignment to update.
        title (str): The new title of the assignment.
        instructions (str): The new instructions for the assignment.
        due_date (datetime): The new due date for the assignment.

    Returns:
        None
    """
    query = """
    UPDATE assignments
    SET title = %s, instructions = %s, due = %s
    WHERE id = %s;
    """
    exec_commit(
        query, (title, instructions, due_date, assignment_id))


def delete_assignment(assignment_id):
    """
    Deletes a specific assignment from the database.

    Args:
        assignment_id (int): The ID of the assignment to delete.

    Returns:
        None
    """
    query = """
    DELETE FROM assignments
    WHERE id = %s;
    """
    exec_commit(query, (assignment_id,))

# submission table functions


def __format_submissions(submissions):
    """
    Formats a list of submissions into a specific format.

    Args:
        submissions (list): A list of submissions, where each submission is a tuple of five elements:
                            (element1, element2, element3, element4, timestamp).

    Returns:
        list: A list of formatted submissions, where each formatted submission is a tuple of five elements:
              (element1, element2, element3, element4, formatted_timestamp).
    """
    formatted = []
    for record in submissions:
        formatted.append((record[0], record[1], record[2],
                         record[3], timestamp_to_str(record[4])))
    return formatted


def get_submissions(assignment_id):
    """
    Retrieves a list of submissions for a specific assignment.

    Args:
        assignment_id (int): The ID of the assignment.

    Returns:
        list: A list of submission records, where each record contains the submission ID,
        assignment title, student's last name, student's first name, and submission status.
    """
    query = """
    SELECT submissions.id, assignments.title, students.last_name, students.first_name, submissions.turned_in
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE assignment_id = %s
    ORDER BY students.last_name ASC;
    """
    submissions = exec_get_all(query, (assignment_id,))
    return __format_submissions(submissions)


def get_submission(submission_id):
    """
    Retrieves information about a specific submission.

    Args:
        submission_id (int): The ID of the submission.

    Returns:
        tuple: A tuple containing the submission ID, assignment title, submission response, student's last name, student's first name, and submission status.
    """
    query = """
    SELECT submissions.id, assignments.title, submissions.response, students.last_name, students.first_name, submissions.turned_in
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE submissions.id = %s;
    """
    submission = exec_get_one(query, (submission_id,))
    return (submission[0], submission[1], submission[2], submission[3], submission[4], timestamp_to_str(submission[5]))


# grades and scores table functions

def __get_grade_id(title, course_id, cur):
    """
    helper function
    Retrieves the ID of a grade based on the grade title and course ID.

    Args:
        title (str): The title of the grade.
        course_id (int): The ID of the course the grade belongs to.
        cur (cursor): The database cursor object.

    Returns:
        tuple or None: A tuple containing the ID of the grade, if found.
        Returns None if no grade with the specified title and course ID is found.
    """
    query = """
    SELECT id
    FROM grades
    WHERE title = %s AND course_id = %s;
    """
    cur.execute(query, (title, course_id))
    return cur.fetchone()


def __get_student_ids(course_id, cur):
    """
    Retrieves the student IDs enrolled in a specific course.

    Args:
        course_id (int): The ID of the course.
        cur (cursor): The database cursor object.

    Returns:
        list: A list of student IDs enrolled in the course.
    """
    query = """
    SELECT student_id
    FROM enrollments
    WHERE course_id = %s;
    """
    cur.execute(query, (course_id,))
    return cur.fetchall()


def create_grade(title, total_points, course_id):
    """
    Creates a new grade for a specific course.

    Args:
        title (str): The title of the grade.
        total_points (float): The total points available for the grade.
        course_id (int): The ID of the course the grade belongs to.

    Returns:
        bool: True if the grade creation is successful,
        False if a grade with the same title already exists in the course.
    """
    query = """
    INSERT INTO grades (title, total_points, posted, course_id)
    VALUES(%s, %s, %s, %s);
    """
    now = timestamp_to_str()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(query, (title, total_points, now, course_id))
        grade_id = __get_grade_id(title, course_id, cur)
        student_ids = __get_student_ids(course_id, cur)
        for id in student_ids:
            __create_score(grade_id, id[0], cur)
        conn.commit()
        conn.close()
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def __format_grades(grades):
    """
    Formats the grades records for display.

    Args:
        grades (list): A list of grade records.

    Returns:
        list: A formatted list of grade records, where each record contains the grade ID,
        title, formatted total points, and formatted posted timestamp.
    """
    formatted = []
    for record in grades:
        record = (record[0], record[1], format_decimal(
            record[2]), record[3].strftime("%x %X"))
        formatted.append(record)
    return formatted


def get_all_grades_avg(course_id):
    """
    Retrieves the average scores for all grades in a specific course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        list: A list of grade records with their average scores,
        sorted by the posted timestamp in descending order.
    """
    query = """
    SELECT grades.id, grades.title, AVG(scores.points_earned / grades.total_points), grades.posted
    FROM grades
    INNER JOIN scores ON grades.id = scores.grade_id
    WHERE grades.course_id = %s
    GROUP BY grades.id
    ORDER BY grades.posted DESC;
    """
    grades = exec_get_all(query, (course_id,))
    return __format_grades(grades)


def update_grade(grade_id, title, total_points):
    """
    Updates the details of a grade.

    Args:
        grade_id (int): The ID of the grade to update.
        title (str): The new title for the grade.
        total_points (int): The new total points for the grade.

    Returns:
        None
    """
    query = """
    UPDATE grades
    SET title = %s, total_points = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, total_points, grade_id))


def delete_grade(grade_id):
    """
    Deletes a grade from the database.

    Args:
        grade_id (int): The ID of the grade to delete.

    Returns:
        None
    """
    query = """
    DELETE FROM grades
    WHERE id = %s;
    """
    exec_commit(query, (grade_id,))


def __create_score(grade_id, student_id, cur):
    """
    Creates a score entry for a grade and a student.

    Args:
        grade_id (int): The ID of the grade.
        student_id (int): The ID of the student.
        cur (cursor): The database cursor to execute the query.

    Returns:
        None
    """
    query = """
    INSERT INTO scores (grade_id, student_id)
    VALUES (%s, %s);
    """
    cur.execute(query, (grade_id, student_id))


def __format_scores(scores):
    """
    Formats the scores retrieved from the database.

    Args:
        scores (list): A list of score records retrieved from the database.

    Returns:
        list: A formatted list of score records.
    """
    formatted = []
    for record in scores:
        record = (record[0], record[1], format_decimal(
            record[2]), record[3], record[4])
        formatted.append(record)
    return formatted


def get_scores(grade_id):
    """
    Retrieves scores for a specific grade from the database.

    Args:
        grade_id (int): The ID of the grade.

    Returns:
        list: A formatted list of score records for the grade.
    """
    query = """
    SELECT scores.id, grades.title, (scores.points_earned / grades.total_points), students.last_name, students.first_name
    FROM ((scores
    INNER JOIN grades ON scores.grade_id = grades.id)
    INNER JOIN students ON scores.student_id = students.id)
    WHERE scores.grade_id = %s
    ORDER BY students.last_name ASC;
    """
    scores = exec_get_all(query, (grade_id,))
    return __format_scores(scores)


def get_score(score_id):
    """
    Retrieves a specific score from the database.

    Args:
        score_id (int): The ID of the score.

    Returns:
        tuple: A formatted tuple representing the score information.
    """
    query = """
    SELECT grades.title, scores.points_earned, grades.total_points, scores.comment, students.last_name, students.first_name
    FROM ((scores
    INNER JOIN grades ON scores.grade_id = grades.id)
    INNER JOIN students ON scores.student_id = students.id)
    WHERE scores.id = %s;
    """
    score = exec_get_one(query, (score_id,))
    formatted_score = (score[0], format_decimal(
        score[1], 1), format_decimal(score[2], 1), score[3], score[4], score[5])
    return formatted_score


def update_score(score_id, points_earned, comments=''):
    """
    Updates the score information in the database for a specific score.

    Args:
        score_id (int): The ID of the score.
        points_earned (float): The points earned for the score.
        comments (str, optional): Additional comments for the score. Defaults to an empty string.

    Returns:
        None
    """
    query = """
    UPDATE scores
    SET points_earned = %s, comment = %s
    WHERE id = %s;
    """
    exec_commit(query, (points_earned, comments, score_id))
