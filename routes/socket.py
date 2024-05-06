from datetime import datetime

from flask import request
from flask_socketio import emit

from domain.connection import Connection
from helpers.functions import authorisation_required
from utils import socketio


# Global dictionary to track user connections
user_connections = {}


@socketio.on('connect')
@authorisation_required
def test_connect(session):
    print('Client connected', session.user_id, request.sid)
    # Store the connection in the database
    connection_item = Connection.add_connection_item(session.user_id)

    # Track the connection in the global dictionary
    user_connections[request.sid] = {
        'user_id': session.user_id,
        'connection_id': connection_item.id
    }


@socketio.on('disconnect')
def test_disconnect():
    connection_info = user_connections.pop(request.sid, None)

    if connection_info:
        print('Client disconnected', connection_info['user_id'], request.sid)
        Connection.disconnect(connection_info['connection_id'])
