from utils import db
from datetime import datetime


class ViewHistory(db.Model):
    __tablename__ = 'View_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)
    view_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('View_history', lazy=True))

    def __init__(self, user_id, topic_id, view_type):
        self.user_id = user_id
        self.topic_id = topic_id
        self.view_type = view_type

    @classmethod
    def add_history_item(cls, user_id, topic_id, view_type):
        if user_id and topic_id:
            history_item = cls(user_id=user_id, topic_id=topic_id, view_type=view_type)
            db.session.add(history_item)
            db.session.commit()
