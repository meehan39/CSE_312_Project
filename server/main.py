from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db

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

@main.route('/message')
@login_required
def messages():
    return render_template('message.html')

@main.route('/friends')
@login_required
def friends():
    return render_template('friends.html')

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
