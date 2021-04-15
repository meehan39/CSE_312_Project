from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request
import os
from werkzeug.utils import secure_filename

users = []



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = r'C:\Users\jonat\Desktop\Atom Projects\Project\server\static\uploads'

app.config['UPLOAD_FOLDER'] = r'C:\Users\jonat\Desktop\Atom Projects\Project\server\static\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

allowed_picture_types = set(['png', 'jpg', 'jpeg', 'gif'])



@app.route("/")
def login():
    return render_template('login.html')

@app.route("/home")
def home():
    username = request.args.get('username')
    password = request.args.get('password')

    return render_template('home.html', username=username)


@app.route("/create")
def create():

    # First is submitted with the form on login.html so it will only exist on the first load.
    First = request.args.get('First')
    username = request.args.get('username')
    password1 = request.args.get('password1')
    password2 = request.args.get('password2')

    if not First:
        if username and password1 and password2:
            if password1 == password2 and validate_password(password1):
                users.append((username,password1))
                return redirect(url_for('login')), flash('Account Created!','accept')
            elif(not validate_password(password1)):
                flash('Password must contain one number, one letter, and at least 8 characters.','error')
            else:
                flash('Passwords do not match.','error')
        elif not username:
            flash('Please enter a valid username.','error')

    return render_template('create.html')

def validate_password(password):
    digit = False
    alpha = False
    length = False
    for char in password:
        if char.isdigit():
            digit = True
        if char.isalpha():
            alpha = True
    if len(password) >= 8:
        length = True

    if digit and alpha and length:
        return True

    return False

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/chat")
def chat():
    return render_template('chat.html')

@app.route("/friends")
def friends():
    return render_template('friends.html')

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
