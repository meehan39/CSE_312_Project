from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = r'C:\Users\jonat\Desktop\Atom Projects\Project\server\static\uploads'

app.config['UPLOAD_FOLDER'] = r'C:\Users\jonat\Desktop\Atom Projects\Project\server\static\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

allowed_picture_types = set(['png', 'jpg', 'jpeg', 'gif'])

users = []

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/home")
def home():
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        if (username,password) in users:
            return render_template('home.html', username=username)


@app.route("/create")
def create():
    username = request.args.get('username')
    password1 = request.args.get('password1')
    password2 = request.args.get('password2')

    if username and password1 and password2:
        if password1 == password2:
            users.append((username,password1))
            return redirect(url_for('login'))

    # also alert the user that passwords dont match
    return render_template('create.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_picture_types



#saves the uploaded file to the static folder
@app.route('/home', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('home.html', filename=filename)
#displays the image on the page
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
