from database.postgres_utils import exec_commit
from database.db_utils import hash_password

def register(username, password):
    query = """
    INSERT INTO teachers (username, password)
    VALUES (%s, %s);
    """
    return exec_commit(query, (username, hash_password(password)))