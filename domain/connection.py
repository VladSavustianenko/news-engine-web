from utils import db
from datetime import datetime


class Connection(db.Model):
    __tablename__ = 'Connection'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    connected = db.Column(db.DateTime, default=datetime.utcnow)
    disconnected = db.Column(db.DateTime, default=None)
    user = db.relationship('User', backref=db.backref('Connection', lazy=True))

    def __init__(self, user_id):
        self.user_id = user_id

    @classmethod
    def add_connection_item(cls, user_id):
        if user_id:
            connection_item = cls(user_id=user_id)
            db.session.add(connection_item)
            db.session.commit()

            return connection_item

    @classmethod
    def disconnect(cls, connection_id):
        connection_item = Connection.query.get(connection_id)

        if connection_item and connection_item.disconnected is None:
            connection_item.disconnected = datetime.utcnow()
            db.session.commit()