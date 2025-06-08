'''
Currently, this does not use password hashing.

This 2nd version of controller.py will use HTML (template), CSS, or Javascript files.
Flask functions renders template HTMLs.
It also has 4 frontend pages: /, /register, /login, and /user.

1. Home: This is the home page. It can go to either Register or Login page. 
2. Login: If login is successful it goes to the User page. It can also go to Register directly (if registerClicked:).
3. Register: If register is successful it goes directly to the User page instead of Login. It can also go to Login directly (if loginClicked:).
4. User: If logoutClicked, go to Home page.

Now use Next.js for frontend (while keeping Flask backend).
Now each Flask function returns JSON instead of template HTML.
'''


from flask import Flask, jsonify, request, redirect, url_for, session, render_template
from flask_session import Session
from flask_cors import CORS

from DB.SQLite_Manager import SQLite_Manager
from DB.SQLite_Manager import SQLResponse
from DB.User import User


def getSQLManager():
    manager = SQLite_Manager()
    return manager

# ----------------------------------------------------------------------------------------------------

app = Flask(__name__)
CORS(app,
     origins=["http://localhost:3000", "http://localhost:5000"],
     supports_credentials=True)
# DEBUG  Use a secure, random key in production
app.secret_key = 'your-secret-key'
# DEBUG
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def home():
    return jsonify({"status": "success",
                    "message": "Welcome to the API"})


@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':  # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    elif request.method == 'POST':
        data = request.get_json()  # Get JSON data instead of form data
        username = data.get('username')
        password = data.get('password')

        manager = getSQLManager()
        user = User.getFromDB(manager, username)

        if user == None:
            return jsonify({"status": "error", 
                            "message": "User not found"})
        if user.password == password:
            session['username'] = username
            return jsonify({
                "status": "success", 
                "message": "Logged in successfully",
                "user": {"username": username}
            })
        else:
            return jsonify({"status": "error", 
                            "message": "Invalid password"})
    else:
        return jsonify({"status": "error", "message": "Method not allowed"}), 405


@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':  # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data instead of form data
        username = data.get('username')
        password = data.get('password')

        manager = getSQLManager()
        newUser = User(username, password, 0)
        isSuccessful = newUser.insertIntoDB(manager)

        if isSuccessful:
            session['username'] = username  # Auto-login after registration
            return jsonify({
                "status": "success", 
                "message": "Registered successfully",
                "user": {"username": username}
            })
        else:
            return jsonify({"status": "error", 
                            "message": "Username already taken"})
    else:
        return jsonify({"status": "error", "message": "Method not allowed"}), 405

@app.route('/api/user', methods=['GET'])
def user():
    if 'username' not in session:
        return jsonify({"status": "error",
                        "message": "Not authenticated"}), 401
    return jsonify({
        "status": "success",
        "user": {"username": session['username']}
    })


@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({"status": "success",
                    "message": "Logged out successfully"})


# Add a route to check authentication status
@app.route('/api/check-auth')
def check_auth():
    if 'username' in session:
        return jsonify({
            "status": "success",
            "authenticated": True,
            "user": {"username": session['username']}
        })
    else:
        return jsonify({
            "status": "success",
            "authenticated": False
        })
    
# DEBUG
if __name__ == "__main__":
    app.run(debug=True)