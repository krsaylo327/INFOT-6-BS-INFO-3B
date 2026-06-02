from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Step 3: Initialize the Database
with app.app_context():
    db.create_all()

# Step 4: The CRUD Logic

# CREATE (POST)
@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author}), 201

# READ (GET) - Get all books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    all_books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author} for book in all_books])

# READ (GET) - Get a single book by ID
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

# UPDATE (PUT)
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

# DELETE
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
