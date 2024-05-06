from utils import db


class UserPreference(db.Model):
    __tablename__ = 'User_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref=db.backref('User_preferences', lazy=True))

    def __init__(self, user_id, topic):
        self.user_id = user_id
        self.topic = topic

    @classmethod
    def add_topic(cls, user_id, topic_name):
        if not cls.query.filter_by(user_id=user_id, topic=topic_name).first():
            new_preference = cls(user_id=user_id, topic=topic_name)
            db.session.add(new_preference)
            db.session.commit()

    @classmethod
    def remove_topic(cls, user_id, topic_name):
        preference_to_remove = cls.query.filter_by(user_id=user_id, topic=topic_name).first()
        if preference_to_remove:
            db.session.delete(preference_to_remove)
            db.session.commit()
