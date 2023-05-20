from database.postgres_utils import exec_commit, exec_get_one, exec_get_all


def create_assignment(title, instructions, due, course_id):
    """
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
    gets all the assignments from the referenced course

    :param course_id: an int
    :returns: a list of tuples
    """
    query = """
    SELECT id, title, due
    FROM assignments
    WHERE course_id = %s
    ORDER BY title ASC;
    """
    return exec_get_all(query, (course_id,))


def get_assignment(assignment_id):
    """
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
    deletes the assignment attached to the id

    :param assignment_id: an int
    """
    query = """
    DELETE FROM assignments
    WHERE id = %s;
    """
    exec_commit(query, (assignment_id,))
