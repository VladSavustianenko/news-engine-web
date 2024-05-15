from flask import jsonify

from domain.user import User
from domain.view_history import ViewHistory
from utils import app


@app.route('/info', methods=['GET'])
def get_info():
    user_count = User.query.count()
    views_count = ViewHistory.query.count()

    return jsonify({
        'Users number': user_count,
        'Views number': views_count,
    })
