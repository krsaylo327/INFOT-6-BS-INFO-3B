# 1. Initialization: Import required tools from flask module
from flask import Flask, request, jsonify

# Initialize your app using app = Flask(__name__)
app = Flask(__name__)

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

# 4. The Run Command: Standard Python main block running on port 5000
if __name__ == "__main__":
    app.run(port=5000, debug=True)

