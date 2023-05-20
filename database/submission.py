from database.postgres_utils import exec_get_one, exec_get_all

def create_submission(response, submitted_date_time, assignment_id, student_id):
    return 0

def get_submissions(assignment_id):
    """
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
