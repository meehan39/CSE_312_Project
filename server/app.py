from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

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
    
    return redirect(url_for('login'))

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

if __name__ == '__main__':
    app.run(debug=True)
