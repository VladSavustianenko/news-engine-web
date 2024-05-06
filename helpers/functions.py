from functools import wraps

from flask import request, jsonify

from domain.session import Session


def get_user_session_by_token(access_token):
    return Session.query.filter_by(access_token=access_token).first()


def authorisation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if not access_token:
            return jsonify({'message': 'Authorization is required'}), 401

        session = get_user_session_by_token(access_token)
        if not session:
            return jsonify({'message': 'Authorization is required'}), 401

        if 'session' in f.__code__.co_varnames:
            kwargs['session'] = session

        return f(*args, **kwargs)

    return decorated_function
