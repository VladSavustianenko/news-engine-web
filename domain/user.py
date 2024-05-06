from datetime import datetime

from flask import jsonify

from utils import db


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    _EMAIL_PATTERN = r'^[a-zA-Z][a-zA-Z0-9_-]{3,40}$'
    _PASSWORD_MIN_LENGTH = 6
    _PASSWORD_MAX_LENGTH = 20

    @classmethod
    def register(cls, name, password, password_confirm):
        if not name or not password or not password_confirm:
            return jsonify({'message': 'All fields are required'}), 400, None

        if len(name) < 3:
            return jsonify({'message': 'Name is too short'}), 400, None

        if len(name) > 30:
            return jsonify({'message': 'Name is too long'}), 400, None

        if len(password) < cls._PASSWORD_MIN_LENGTH:
            return jsonify({'message': 'Password is too short'}), 400, None

        if len(password) > cls._PASSWORD_MAX_LENGTH:
            return jsonify({'message': 'Password is too long'}), 400, None

        if not cls.__compare_passwords(password, password_confirm):
            return jsonify({'message': 'Passwords do not match'}), 400, None

        if cls.query.filter_by(name=name).first():
            return jsonify({'message': 'User with this name already exists'}), 400, None

        user = cls(name=name, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201, user

    @staticmethod
    def is_user_login_invalid(user, password):
        return not user or user.password != password

    @staticmethod
    def __compare_passwords(password, password_confirm):
        return password == password_confirm
