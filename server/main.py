from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from flask_socketio import emit
from . import socketio
from .models import User, Posts, Chat

from datetime import datetime, timedelta

<<<<<<< HEAD
# from flask_session import Session
=======
>>>>>>> 9a9f1c64de0dfb88438ea05ad91aa1e1f8465f76


main = Blueprint('main', __name__)


@socketio.on('like')
def like(id):
    post = Posts.query.get(id)
    post.likes = post.likes + 1
    likes = post.likes
    db.session.commit()

    # sends id and likes so split on -
    emit("add-like", {'data': id["id"]+ ";" + str(likes)},broadcast=True)

@socketio.on('dislike')
def like(id):
    post = Posts.query.get(id)
    post.likes = post.likes - 1
    likes = post.likes
    db.session.commit()

    # sends id and likes so split on ;
    emit("add-like", {'data': id["id"]+ ";" + str(likes)},broadcast=True)

@socketio.on('new')
def new():
    emit("new-post", broadcast=True)

@main.route('/', methods=['GET','POST'])
@login_required
def index():
<<<<<<< HEAD

=======
    #db.create_all()
    
>>>>>>> 9a9f1c64de0dfb88438ea05ad91aa1e1f8465f76
    posts = []
    post = request.args.get('post')
    if post != None:
        new_post = Posts(username = current_user.username, post=post, likes=0)
        db.session.add(new_post)
        db.session.commit()
        return(redirect(''))

    db_posts = Posts.query.all()
    for post in db_posts:
        posts.append([post.post,post.username,post.likes,post.id])

    # uncomment this (one at a time) to delete posts
    #db.session.query(Posts).delete()
    #db.session.query(Chat).delete()
    #db.session.commit()

    return render_template('feed.html',posts=reversed(posts), username = current_user.username)

@main.route('/create')
@login_required
def create_post():
    return render_template('create.html', username = current_user.username)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username, avatar=current_user.avatar)

@main.route('/messages', methods=['GET','POST'])
def messages():
    username = request.args.get('username')
    curr = current_user.username

    # This is a constant way to store the usernames so that both users have the same ordering.
    if curr<username:
        user1 = curr
        user2 = username
    else:
        user1 = username
        user2 = curr

    users=Chat.query.filter_by(users=user1+user2).first()
    history = "You and " + username + " havent chatted yet!\nWhy not send them a message?"
    if users != None:
        history = users.history

    return render_template('messages.html', username=username, user1=user1, user2=user2, history=history, sender=current_user.username)

@socketio.on('message')
def sendmessage(data):
    data=data['data'].split(';')

    # this way the message can contain ; nad still wotk properly.
    message = ';'.join(data[:-3])
    user1 = data[-3]
    user2 = data[-2]
    sender = data[-1]

    users=Chat.query.filter_by(users=user1+user2).first()
    if users == None:
        new_Chat = Chat(users=user1+user2,history = sender + ': ' + message +  '\n')
        db.session.add(new_Chat)
        db.session.commit()
    else:
        users.history = users.history + sender + ': ' + message +  '\n'
        db.session.commit()
    
    if (user1 != sender):
        receiver = user1
    else: 
        receiver = user2

    emit('received',{'data':receiver + ';' + sender}, broadcast=True)

    emit(user1+user2,{'message':message + ';' + sender}, broadcast=True)


@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html', username = current_user.username)

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

@main.route('/friends')
@login_required
def friends():
    return render_template('friends.html',students = User.query.all(), username = current_user.username)

@main.before_request
def update_last_active():
    users=User.query.all()
    current_user.active_time = datetime.now()
    ten_mins_ago =  datetime.now() - timedelta(minutes=10)
    db.session.commit()

    for i in users:

        date_time_obj = datetime.strptime(i.active_time, '%Y-%m-%d %H:%M:%S.%f')
        time_difference= datetime.now() - date_time_obj
        hours=str(str(time_difference)).split(":")[0]
        minutes=((str(time_difference)).split(":")[1]).split(":")[0]
        i.last_time= hours + " hours " + minutes + " minutes ago"
        if abs(datetime.now() - date_time_obj) <= timedelta(minutes=10):
            i.active= "True"
        else:
            i.active = "False"

    db.session.commit()
