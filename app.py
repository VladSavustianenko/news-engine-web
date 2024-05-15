import os

from utils import db, app
from routes.user import *
from routes.news import *
from routes.info import *
# from routes.socket import *

port = int(os.environ.get("PORT", 5000))

with app.app_context():
    db.create_all()  # Creates all tables
    db.create_all(bind='news')  # Creates all tables


if __name__ == '__main__':
    # socketio.run(app, host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port)
