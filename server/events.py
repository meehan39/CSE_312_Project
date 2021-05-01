# code reference: https://www.youtube.com/watch?v=q42zgGaYYzE

from flask_socketio import SocketIO, join_room, emit, leave_room, send
from flask import session
from . import socketio
from .models import Posts


@socketio.on('join', namespace='/message')
def join(mesag):
    room_name = session.get('chatName')
    # username = session.get('username')
    join_room(room_name)
    emit('status', {'msg': session.get('username') + 'has entered the chat'}, room=room_name)


@socketio.on('text', namespace='/message')
def text(mesag):
    room_name = session.get('chatName')
    # username = session.get('username')
    emit('message', {'msg': session.get('username') + ' : ' + mesag['msg']}, room=room_name)


@socketio.on('leave', namespace='/message')
def leave(mesag):
    room_name = session.get('chatName')
    # username = session.get('username')
    leave_room(room_name)
    session.clear()
    emit('status', {'msg': session.get('username') + 'has left the chat.'}, room=room_name)
