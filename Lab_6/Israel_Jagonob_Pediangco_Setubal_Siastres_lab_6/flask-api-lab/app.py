from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/greeting', methods=['GET'])
def greeting():
    return jsonify({
        "message": "Hello from Flask!"
    })

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)