from database.postgres_utils import connect, exec_commit, exec_get_one, exec_get_all
from database.db_utils import hash_password, current_timestamp
import psycopg2

# all the functions teacher users will be calling

# teacher table function


def create_teacher(first_name, last_name, username, password):
    """
    TESTED
    attempts to add record to teacher table if username is unique
    teachers are created with a unique id generated, first and last name set to empty strings

    :param first_name: a string
    :param last_name: a string
    :param username: a string
    :param password: a string that gets hashed
    :returns: True if teacher is created and False otherwise
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
    TESTED
    gets a teacher given their id

    :param teacher_id: an int
    :returns: a tuple
    """
    query = """
    SELECT id, first_name, last_name, username
    FROM teachers
    WHERE id = %s;
    """
    return exec_get_one(query, (teacher_id,))


def login(username, password):
    """
    TESTED
    gets a teacher that matches the given username and hashed password

    :param username: a string
    :param password: a string that gets hashed
    :returns: a tuple
    """
    query = """
    SELECT id, first_name, last_name, username
    FROM teachers
    WHERE username = %s AND password = %s;
    """
    return exec_get_one(query, (username, hash_password(password))) is not None


def update_teacher(teacher_id, first_name, last_name, username, password):
    """
    TESTED
    updates the teachers first and last name

    :param teacher_id: an int
    :param first_name: a string
    :param last_name: a string
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
    TESTED
    deletes a teacher from the table

    :param teacher_id: an int
    :param password: a string that gets hashed
    """
    query = """
    DELETE FROM teachers
    WHERE id = %s AND password = %s;
    """
    exec_commit(query, (teacher_id, hash_password(password)))

# student table function


def get_students(class_id):
    """
    TESTED
    for teachers to use
    select all students from a given class

    :param class_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT enrollments.id, students.last_name, students.first_name
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    WHERE enrollments.course_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (class_id,))


def get_student(enrollment_id):
    """
    TESTED
    select a students from a given course

    :param enrollment_id: an int
    :returns: a tuple
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

def create_course(title, teacher_id):
    """
    TESTED
    creates a course for a teacher with a given title

    :param title: a string
    :param teacher_id: an int
    """
    query = """
    INSERT INTO courses (title, teacher_id)
    VALUES (%s, %s);
    """
    exec_commit(query, (title, teacher_id))


def get_courses(teacher_id):
    """
    TESTED
    gets courses that a specific teacher is teaching
    :param teacher_id: an int
    :return: a list of tuples
    """
    query = """
    SELECT id, title
    FROM courses
    WHERE teacher_id = %s
    ORDER BY title ASC;
    """
    results = exec_get_all(query, (teacher_id,))
    return results


def update_course(course_id, title):
    """
    TESTED
    updates the title of the course

    :param course_id: an int
    :param title: a string
    """
    query = """
    UPDATE courses
    SET title = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, course_id))


def delete_course(course_id):
    """
    TESTED
    deletes a course from the table

    :param course_id: an int
    """
    query = """
    DELETE FROM courses
    WHERE id = %s;
    """
    exec_commit(query, (course_id,))

# assignment table functions


def create_assignment(title, instructions, due, course_id):
    """
    TESTED
    creates an assignment with a name and instructions attached to a certain record in the courses table

    :param title: a string
    :param instructions: a string
    :param due: a string
    :param course_id: an int
    """
    query = """
    INSERT INTO assignments (title, instructions, due, course_id)
    VALUES (%s, %s, %s, %s)
    """
    exec_commit(query, (title, instructions, due, course_id))


def get_assignments(course_id):
    """
    TESTED
    gets all the assignments from the referenced course

    :param course_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT id, title, due
    FROM assignments
    WHERE course_id = %s
    ORDER BY due DESC;
    """
    return exec_get_all(query, (course_id,))


def get_assignment(assignment_id):
    """
    TESTED
    get an assignment by its id

    :param assignment_id: an int
    :returns: a tuple
    """
    query = """
    SELECT id, title, instructions, due
    FROM assignments
    WHERE id = %s;
    """
    return exec_get_one(query, (assignment_id,))


def update_assignment(assignment_id, title, instructions, due_date):
    """
    TESTED
    updates the title and instructions of a given assignment

    :param assignment_id: an int
    :param title: a string
    :param instructions: a string
    :param due: a string
    """
    query = """
    UPDATE assignments
    SET title = %s, instructions = %s, due = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, instructions, due_date, assignment_id))


def delete_assignment(assignment_id):
    """
    TESTED
    deletes the assignment attached to the id

    :param assignment_id: an int
    """
    query = """
    DELETE FROM assignments
    WHERE id = %s;
    """
    exec_commit(query, (assignment_id,))

# submission table functions


def get_submissions(assignment_id):
    """
    TESTED
    get submissions by an assignment id

    :param assignment_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT submissions.id, assignments.title, students.last_name, students.first_name, submissions.turned_in
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE assignment_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (assignment_id,))


def get_submission(submission_id):
    """
    TESTED
    get submissions by an assignment id

    :param assignment_id: an int
    :returns: a tuple
    """
    query = """
    SELECT submissions.id, assignments.title, submissions.response, students.last_name, students.first_name, submissions.turned_in
    FROM ((submissions
    INNER JOIN assignments ON submissions.assignment_id = assignments.id)
    INNER JOIN students ON submissions.student_id = students.id)
    WHERE submissions.id = %s;
    """
    return exec_get_one(query, (submission_id,))


# grades and scores table functions

def __get_grade_id(title, course_id, cur):
    """
    helper function that gets the id of the grade just created

    :param title: a string
    :param course_id: an int
    :param cur: cursor object
    :returns: a tuple
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
    helper function that gets all the student ids from a given course

    :param course_id: an int
    :param cur: cursor object
    :returns: a list of tuples
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
    TESTED
    attempts to create a grade for a given course fails if there is 
    already a grade with the same title in the same course
    if the grade is successfully created then scores for the entire class are created

    :param title: a string
    :param total_points: an int
    :param course_id: an int
    :returns: true if grade is created and false otherwise
    """
    query = """
    INSERT INTO grades (title, total_points, posted, course_id)
    VALUES(%s, %s, %s, %s);
    """
    now = current_timestamp()
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


def get_all_grades_avg(course_id):
    """
    TESTED
    gets the avg of each grade in a specific course

    :param course_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT grades.id, grades.title, AVG(scores.points_earned / grades.total_points), grades.posted
    FROM grades
    INNER JOIN scores ON grades.id = scores.grade_id
    WHERE grades.course_id = %s
    GROUP BY grades.id
    ORDER BY grades.posted DESC;
    """
    return exec_get_all(query, (course_id,))


def update_grade(grade_id, title, total_points):
    """
    TESTED
    creates a grade for a given enrollment

    :param grade_id: an int
    :param title: a string
    :param total_points: an int
    """
    query = """
    UPDATE grades
    SET title = %s, total_points = %s
    WHERE id = %s;
    """
    exec_commit(query, (title, total_points, grade_id))


def delete_grade(grade_id):
    """
    TESTED
    deletes a specific grade

    :param grade_id: an int
    """
    query = """
    DELETE FROM grades
    WHERE id = %s;
    """
    exec_commit(query, (grade_id,))


def __create_score(grade_id, student_id, cur):
    """
    creates a score given a grade id, student id, and earned points which is null by default
    cursor is passed in so multiple connections don't have to be opened and closed

    :param grade_id: an int
    :param student_id: an int
    :param cur: cursor object
    :points_earned: an int
    """
    query = """
    INSERT INTO scores (grade_id, student_id)
    VALUES (%s, %s);
    """
    cur.execute(query, (grade_id, student_id))


def get_scores(grade_id):
    """
    TESTED
    gets all the scores from a specific grade

    :param grade_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT scores.id, grades.title, (scores.points_earned / grades.total_points), students.last_name, students.first_name
    FROM ((scores
    INNER JOIN grades ON scores.grade_id = grades.id)
    INNER JOIN students ON scores.student_id = students.id)
    WHERE scores.grade_id = %s
    ORDER BY students.last_name ASC;
    """
    return exec_get_all(query, (grade_id,))


def get_score(score_id):
    """
    TESTED
    gets a specific score

    :param score_id: an int
    :returns: a tuple
    """
    query = """
    SELECT grades.title, scores.points_earned, grades.total_points, scores.comment, students.last_name, students.first_name
    FROM ((scores
    INNER JOIN grades ON scores.grade_id = grades.id)
    INNER JOIN students ON scores.student_id = students.id)
    WHERE scores.id = %s;
    """
    return exec_get_one(query, (score_id,))


def update_score(score_id, points_earned, comments=''):
    """
    TESTED
    updates a specific score

    :param score_id: an int
    :param points_earned: an int
    :returns: a tuple
    """
    query = """
    UPDATE scores
    SET points_earned = %s, comment = %s
    WHERE id = %s;
    """
    exec_commit(query, (points_earned, comments, score_id))
