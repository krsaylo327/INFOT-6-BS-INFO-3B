from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book added successfully"
    })

@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    result = []

    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author
        })

    return jsonify(result)

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json()

    book.title = data['title']
    book.author = data['author']

    db.session.commit()

    return jsonify({
        "message": "Book updated successfully"
    })

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "message": "Book deleted successfully"
    })

if __name__ == '__main__':
    app.run(port=5000)