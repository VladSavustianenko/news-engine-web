from flask import request, jsonify

from domain.session import Session
from domain.user import User
from domain.user_preferences import UserPreference
from helpers.functions import authorisation_required
from utils import app, db


@app.route('/api/user/create', methods=['POST'])
def create_user():
    name = request.json.get('name')
    password = request.json.get('password')
    password_confirm = request.json.get('passwordConfirm')

    resp, status, user = User.register(name, password, password_confirm)

    if user:
        return Session.create_session(user=user)

    return resp, status


@app.route('/api/user/login', methods=['POST'])
def login():
    name = request.json.get('name')
    password = request.json.get('password')

    user = User.query.filter_by(name=name).first()
    if User.is_user_login_invalid(user, password):
        return jsonify({'message': 'Invalid credentials'}), 400

    return Session.create_session(user=user)


@app.route('/api/user/logout', methods=['POST'])
@authorisation_required
def logout(session):
    return Session.delete_session(session)


@app.route('/api/api/users/preferences', methods=['POST'])
@authorisation_required
def update_user_preferences(session):
    data = request.json
    topics_to_add = set(data.get('add', []))
    topics_to_remove = set(data.get('remove', []))

    if not topics_to_add and not topics_to_remove:
        return jsonify({"error": "No topics specified for add or remove actions"}), 400

    # Handle Additions
    for topic_name in topics_to_add:
        UserPreference.add_topic(session.user_id, topic_name)

    # Handle Removals
    for topic_name in topics_to_remove:
        UserPreference.remove_topic(session.user_id, topic_name)

    db.session.commit()
    return jsonify({"message": "User preferences updated successfully"}), 200
