from .postgres_utils import exec_get_all, exec_get_one


"""
functions that are shared by both students and teachers
"""


def __format_assignments(assignments):
    """
    helper function
    Formats the assignment records into a specific format.

    Args:
        assignments (list): A list of assignment records, where each record is a tuple (title, instructions, due).

    Returns:
        list: A formatted list of assignment records, where each record is a tuple (title, instructions, formatted_due).
    """
    formatted = []
    for record in assignments:
        record = (record[0], record[1], record[2].strftime("%x %X"))
        formatted.append(record)
    return formatted


def get_assignments(course_id):
    """
    Retrieves a list of assignments for a specific course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        list: A list of formatted assignment records, where each record is a tuple (id, title, formatted_due).
    """
    query = """
    SELECT id, title, due
    FROM assignments
    WHERE course_id = %s
    ORDER BY due DESC;
    """
    assignments = exec_get_all(query, (course_id,))
    return __format_assignments(assignments)


def get_assignment(assignment_id):
    """
    Retrieves information about a specific assignment.

    Args:
        assignment_id (int): The ID of the assignment.

    Returns:
        tuple: A tuple containing the assignment ID, title, instructions, and formatted due date.
    """
    query = """
    SELECT id, title, instructions, due
    FROM assignments
    WHERE id = %s;
    """
    assignment = exec_get_one(query, (assignment_id,))
    return (assignment[0], assignment[1], assignment[2], assignment[3].strftime("%x %X"))
