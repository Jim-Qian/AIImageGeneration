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


import os, json
from flask import Flask, jsonify, request, redirect, url_for, session, render_template
from flask_session import Session
from flask_cors import CORS
import redis

from DB.SQLite_Manager import SQLite_Manager
from DB.SQLite_Manager import SQLResponse
from DB.User import User
from APIs import OpenAI_Client


def getSQLManager():
    manager = SQLite_Manager()
    return manager

# ----------------------------------------------------------------------------------------------------
# Read secrets
script_dir = os.path.dirname(__file__)
secret_path = os.path.abspath(os.path.join(script_dir, "secrets.json"))
with open(secret_path, "r") as f:
    secrets = json.load(f)

# Create the Flask Server and set its CORS policy
app = Flask(__name__)
CORS(app,
     supports_credentials=True)

# Set Flask Server's secret key
app.secret_key = secrets.get("Flask_SecretKey")

# Session  No longer using file system:  app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.Redis(secrets.get("Redis_Server_URL_NoPort"), port=secrets.get("Redis_Server_Port"), db=0)
app.config["SESSION_PERMANENT"] = False  # Make session non-permanent. Valid until browser is closed.
app.config["SESSION_USE_SIGNER"] = True  # Adds security with signed cookies
Session(app)

# Basic Routes ----------------------------------------------------------------------------------------------------

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
        User_StartingBalance = secrets.get("User_StartingBalance")
        newUser = User(username, password, User_StartingBalance)
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
    manager = getSQLManager()
    user = User.getFromDB(manager, session["username"])
    if user == None:
        return jsonify({"status": "error",
                        "message": "The user has already been deleted from DB"}), 410

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
    if 'username' not in session:
        return jsonify({"status": "error",
                        "authenticated": False,
                        "message": "Not authenticated"}), 401
    manager = getSQLManager()
    user = User.getFromDB(manager, session["username"])
    if user == None:
        return jsonify({"status": "error",
                        "authenticated": False,
                        "message": "The user has already been deleted from DB"}), 410

    return jsonify({
        "status": "success",
        "authenticated": True,
        "user": {"username": session['username']}
    })

    
# Other Routes ----------------------------------------------------------------------------------------------------


@app.route('/api/getBalance', methods=['GET'])
def getBalance():
    if 'username' not in session:
        return jsonify({"status": "error",
                        "message": "Not authenticated"}), 401
    manager = getSQLManager()
    user = User.getFromDB(manager, session["username"])
    if user == None:
        return jsonify({"status": "error",
                        "message": "The user has already been deleted from DB"}), 410
    
    balance = user.balance
    
    return jsonify({
        "status": "success",
        "balance": balance
    })


@app.route('/api/getUnitCost', methods=['GET'])
def getUnitCost():
    unitCost = secrets.get("User_UnitCost")
    
    return jsonify({
        "status": "success",
        "unitCost": unitCost
    })

@app.route('/api/sendAIImageGenerationRequest', methods=['POST', 'OPTIONS'])
def sendAIImageGenerationRequest():
    if request.method == 'OPTIONS':  # Handle preflight request
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    if request.method == 'POST':
        if 'username' not in session:
            return jsonify({"status": "error",
                            "message": "Not authenticated"}), 401
        manager = getSQLManager()
        user = User.getFromDB(manager, session["username"])
        if user == None:
            return jsonify({"status": "error",
                            "authenticated": False,
                            "message": "The user has already been deleted from DB"}), 410

        data = request.get_json()
        size1 = data.get('size1')
        size2 = data.get('size2')
        prompt = data.get('prompt')

        if (not isinstance(size1, int) or not isinstance(size2, int) or 
            size1 > 2000 or size2 > 2000 or size1 <= 0 or size2 <= 0 or 
            not isinstance(prompt, str) or prompt == ""):
            return jsonify({"status": "error", 
                            "message": "Generation failed because of bad input"})

        url = OpenAI_Client.generate(prompt, size1, size2)
        # Even if generation failed, still gonna deduct. Maybe use a more complex pricing scheme in the future.
        unitCost = secrets.get("User_UnitCost")
        user.changeBalance(manager, user.balance - unitCost)

        if url != None:
            return jsonify({
                "status": "success", 
                "message": "Generation successful",
                "url": url
            })
        else:
            return jsonify({"status": "error", 
                            "message": "Generation failed"})
    else:
        return jsonify({"status": "error",
                        "message": "Method not allowed"}), 405

# ----------------------------------------------------------------------------------------------------
    

if __name__ == "__main__":
    # app.run(debug=True)  # DEBUG

    HTTPSCertificate_PublicKey = secrets.get("HTTPSCertificate_PublicKey")
    HTTPSCertificate_PrivateKey = secrets.get("HTTPSCertificate_PrivateKey")
    app.run(host='0.0.0.0',  # Allow access from any IP
            port=443,
            ssl_context=(HTTPSCertificate_PublicKey, HTTPSCertificate_PrivateKey))