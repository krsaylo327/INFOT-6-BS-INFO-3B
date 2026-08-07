from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Step 1: Configuration & Connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Step 2: The Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }

# Step 3: Initialize Database
with app.app_context():
    db.create_all()

# Step 4: CRUD Routes

# CREATE (POST)
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

# READ (GET all)
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# READ (GET one)
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

# UPDATE (PUT)
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)

    db.session.commit()
    return jsonify(book.to_dict())

# DELETE (DELETE)
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)