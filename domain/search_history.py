from utils import db
from datetime import datetime


class SearchHistory(db.Model):
    __tablename__ = 'Search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    value = db.Column(db.String, nullable=False)
    search_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('Search_history', lazy=True))

    def __init__(self, user_id, value, search_type):
        self.user_id = user_id
        self.value = value
        self.search_type = search_type

    @classmethod
    def add_history_item(cls, user_id, value, search_type):
        if user_id and value:
            history_item = cls(user_id=user_id, value=value, search_type=search_type)
            db.session.add(history_item)
            db.session.commit()
