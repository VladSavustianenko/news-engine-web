from datetime import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token

from utils import db


class Session(db.Model):
    __tablename__ = 'Session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    access_token = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token

    @classmethod
    def create_session(cls, user):
        if not user:
            return jsonify({'message': 'Invalid user ID'}), 400

        access_token = create_access_token(identity=user.id)

        if not access_token:
            return jsonify({'message': 'Invalid access token'}), 400

        session = cls(user_id=user.id, access_token=access_token)
        db.session.add(session)
        db.session.commit()

        return jsonify({'accessToken': access_token, 'user': {'id': user.id, 'name': user.name}}), 200

    @staticmethod
    def delete_session(session):
        db.session.delete(session)
        db.session.commit()

        return jsonify({'message': 'Logout successful'}), 200

