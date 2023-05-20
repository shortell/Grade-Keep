from database.postgres_utils import exec_get_one, exec_get_all


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
