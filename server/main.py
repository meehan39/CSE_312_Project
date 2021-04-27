# code reference: https://www.youtube.com/watch?v=rXQAKGSOcjk

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from flask_socketio import SocketIO, join_room, emit, leave_room
from . import socketio
# from flask_session import Session


main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('feed.html')

@main.route('/profile')
@login_required
def profile():
    # print(app.config['UPLOAD_FOLDER'])
    return render_template('profile.html', username=current_user.username, avatar=current_user.avatar)

@main.route('/message_index')
@login_required
def messages():
    print('messages index')
    return render_template('message_index.html')

@main.route('/message', methods=['GET', 'POST'])
def send_message():
    print("in send message")
    if request.method == "POST":
        print("recieved post")
        username = request.form['username']
        room = request.form['chatName']
        session['username'] = username
        session['chatName'] = room
        return render_template('message.html', room=room)
    else:
        if session.get('username') is not None and session.get('chatName') is not None:
            print("reloaded pge")
            return render_template('message.html', session=session)
        else:
            print('nothing wa')
            return redirect(url_for('messages'), 302)


# @main.route('/friends')
# @login_required
# def friends():
#     return render_template('friends.html',students = User.query.all())

@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files['file']

    allowed_picture_types = set(['png', 'jpg', 'jpeg', 'gif'])
    allowed_file = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_picture_types

    if file and allowed_file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('./server/static/uploads', filename))
        current_user.avatar = filename
        db.session.commit()

    return redirect(url_for('main.profile'))
