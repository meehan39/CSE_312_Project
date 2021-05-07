# code reference: https://www.youtube.com/watch?v=rXQAKGSOcjk

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from flask_socketio import SocketIO, join_room, emit, leave_room, send
from . import socketio
from .models import User, Posts

#import datetime
from datetime import datetime, timedelta

# from flask_session import Session


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
    #db.session.commit()

    return render_template('feed.html',posts=reversed(posts))

@main.route('/create')
@login_required
def create_post():
    return render_template('create.html')

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
            #print("reloaded pge")
            return render_template('message.html', session=session)
        else:
            #print('nothing wa')
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

@main.before_request
def update_last_active():
    users=User.query.all()
    current_user.active_time = datetime.now()
    ten_mins_ago =  datetime.now() - timedelta(minutes=10)
    # if abs(current_user.active_time - ten_mins_ago) < timedelta(minutes=10) :
    #     print("hello")
    #print(current_user.active - ten_mins_ago)
    db.session.commit()

    for i in users:
        #print(i.username)
        #print(i.active_time)
        #i.last_time= (datetime.now() -  datetime.strptime(i.active_time, '%Y-%m-%d %H:%M:%S.%f'))

        date_time_obj = datetime.strptime(i.active_time, '%Y-%m-%d %H:%M:%S.%f')
        time_difference= datetime.now() - date_time_obj
        #print("Difference is below")
        #print(time_difference)
        hours=str(str(time_difference)).split(":")[0]
        #print("hours below")
        #print(hours)
        minutes=((str(time_difference)).split(":")[1]).split(":")[0]
        #print("minutes below")
        #print(minutes)

        i.last_time= hours + " hours " + minutes + " minutes ago"
        #print("object")
        #print(date_time_obj)
        #print("ten minutes ago")
        #print(ten_mins_ago)
        #print("Difference Below")
        #print(abs(datetime.now() - date_time_obj))
        if abs(datetime.now() - date_time_obj) <= timedelta(minutes=10):
            #print("username below is active")
            #print(i.username)
            i.active= "True"
        else:
            i.active = "False"

    db.session.commit()
