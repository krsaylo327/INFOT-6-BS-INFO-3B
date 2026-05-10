from flask import Flask, jsonify
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)


if not os.getenv("SECRET_KEY"):
    print("ERROR: SECRET_KEY is missing!")
    exit()


users = {
    1: {
        "id": 1,
        "name": "X",
        "role": "Admin"
    },
    2: {
        "id": 2,
        "name": "Y",
        "role": "User"
    }
}


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):

    if id in users:
        return jsonify(users[id])

    return jsonify({
        "error": "User not found"
    }), 404


if __name__ == '__main__':
    app.run(debug=True)