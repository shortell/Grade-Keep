from flask import session
from flask_restful import Resource, request, abort


def is_logged_in():
    return session.get("id") is not None


def is_role(role):
    return session.get("account_type") == role


def is_session_valid(role):
    if not is_logged_in():
        abort(401, message="you must log in to make this request")
    if not is_role(role):
        abort(403, message="you must be a {} to make this request".format(role))
    return True
