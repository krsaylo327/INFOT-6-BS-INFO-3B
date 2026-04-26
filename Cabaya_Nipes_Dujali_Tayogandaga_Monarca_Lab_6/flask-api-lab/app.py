from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/greeting', methods=['GET'])
def greeting():
    return jsonify({"message": "Hello from Flask API!"})

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()  
    return jsonify(data)       

# Run the server
if __name__ == "__main__":
    app.run(port=5000)
