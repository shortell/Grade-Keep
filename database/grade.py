from database.postgres_utils import exec_commit


def create_grade(title, total_points, class_id):
    """
    creates a grade for a given enrollment

    :param title: a string
    :param total_points: an int
    :param class_id: an int
    """
    query = """
    INSERT INTO grades (title, total_points, class_id)
    VALUES(%s, %s, %s);
    """
    exec_commit(query, (title, total_points, class_id))
