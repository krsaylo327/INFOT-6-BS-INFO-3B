from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Check for SECRET_KEY
if not os.getenv("SECRET_KEY"):
    print("Error: SECRET_KEY not set")
    exit()

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    if id == 1:
        return jsonify({"id": 1, "name": "Alice"})
    elif id == 2:
        return jsonify({"id": 2, "name": "Bob"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)