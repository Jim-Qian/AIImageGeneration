'''
Currently, this does not use password hashing.
'''


from flask import Flask, request, redirect, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from DB.SQLite_Manager import SQLite_Manager
from DB.SQLite_Manager import SQLResponse
from DB.User import User


def getSQLManager():
    manager = SQLite_Manager()
    return manager


app = Flask(__name__)
# DEBUG  Use a secure, random key in production
app.secret_key = 'your-secret-key'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        manager = getSQLManager()
        newUser = User(username, password, 0)
        isSuccessful = newUser.insertIntoDB(manager)
        if not isSuccessful:
            return 'Username already taken.'
        return redirect('/login')
    
    # If request.method == 'GET':
    return render_template_string("""
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Register">
        </form>
    """)

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
                return 'Logged in successfully as Admin.'

            return 'Logged in successfully.'
        else:
            return 'Invalid password.'

    # If request.method == 'GET':
    return render_template_string("""
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# DEBUG
app.run(debug=True)
# app.run()


