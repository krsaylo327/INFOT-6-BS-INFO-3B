# 1. Initialization: Import required tools from flask module
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from Flask-specific file (.flaskenv)
load_dotenv('.flaskenv')

# Ensure SECRET_KEY present before starting the app
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    print('ERROR: SECRET_KEY not found in environment. Exiting.')
    raise SystemExit(1)

# Initialize your app using app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# 2. The GET Endpoint (/api/greeting)
@app.route('/api/greeting', methods=['GET'])
def greeting():
    # Return a JSON response with a greeting message
    return jsonify({"message": "Hello! Welcome to your Python Flask API!"})

# 3. The POST Endpoint (/api/echo)
@app.route('/api/echo', methods=['POST'])
def echo():
    # Data Capture: Grab the incoming JSON payload
    data = request.get_json()
    
    # Logic: Return that exact data back to the user
    return jsonify(data)

# 4. The User Profile Endpoint (/api/users/<id>)
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    # Route parameter id is captured from the URL
    if id == 1:
        return jsonify({"id": 1, "name": "X", "role": "User Profile"})
    elif id == 2:
        return jsonify({"id": 2, "name": "Y", "role": "User Profile"})
    else:
        return jsonify({"error": "User not found"}), 404

# 5. The Run Command: Standard Python main block running on port 5000
if __name__ == "__main__":
    app.run(port=5000, debug=True)

