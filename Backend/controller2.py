'''
Currently, this does not use password hashing.

This 2nd version of controller.py will use HTML (template), CSS, or Javascript files.
Flask functions renders template HTMLs.
It also has 4 frontend pages: /, /register, /login, and /user.

1. Home: This is the home page. It can go to either Register or Login page. 
2. Login: If login is successful it goes to the User page. It can also go to Register directly (if registerClicked:).
3. Register: If register is successful it goes directly to the User page instead of Login. It can also go to Login directly (if loginClicked:).
4. User: If logoutClicked, go to Home page.
'''


from flask import Flask, request, redirect, url_for, session, render_template
from flask_session import Session

from DB.SQLite_Manager import SQLite_Manager
from DB.SQLite_Manager import SQLResponse
from DB.User import User


def getSQLManager():
    manager = SQLite_Manager()
    return manager

# ----------------------------------------------------------------------------------------------------

app = Flask(__name__)
# DEBUG  Use a secure, random key in production
app.secret_key = 'your-secret-key'
# DEBUG
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        manager = getSQLManager()
        user = User.getFromDB(manager, username)

        if user == None:
            return 'User not found.'
        if user.password == password:
            # DEBUG
            # session['user_id'] = user['id']

            # DEBUG
            if user.isAdmin:
                # DEBUG
                # return 'Logged in successfully as Admin.'
                pass
            session['username'] = username
            return redirect(url_for('user'))
            # return 'Logged in successfully.'
        else:
            # DEBUG
            return 'Invalid password.'
    
    # If request.method == 'GET':
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        manager = getSQLManager()
        newUser = User(username, password, 0)
        isSuccessful = newUser.insertIntoDB(manager)
        if isSuccessful:
            session['username'] = username  # Auto-login after registration
            return redirect(url_for('user'))
        if not isSuccessful:
            return 'Username already taken.'

    return render_template('register.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')