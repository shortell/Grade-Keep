from database.postgres_utils import exec_commit, exec_get_all


def create_course(title, teacher_id):
    """
    creates a course for a teacher with a given title

    :param title: a string
    :param teacher_id: an int
    """
    query = """
    INSERT INTO courses (title, teacher_id)
    VALUES (%s, %s);
    """
    exec_commit(query, (title, teacher_id))


def get_teachers_courses(teacher_id):
    """
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


def get_students_courses(student_id):
    """
    gets courses a student is enrolled in
    :param student_id: an int
    :return: a list of tuples
    """
    query = """
    SELECT courses.id, courses.title
    FROM enrollments
    INNER JOIN courses ON enrollments.course_id = courses.id
    WHERE enrollments.student_id = %s
    ORDER BY title ASC;
    """
    results = exec_get_all(query, (student_id,))
    return results


def update_course(course_id, title):
    """
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
    deletes a course from the table

    :param course_id: an int
    """
    query = """
    DELETE FROM courses
    WHERE id = %s;
    """
    exec_commit(query, (course_id,))
