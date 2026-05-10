# book

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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }


with app.app_context():
    db.create_all()


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book added successfully",
        "book": new_book.to_dict()
    }), 201


@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()

    return jsonify([
        book.to_dict() for book in all_books
    ])


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)

    db.session.commit()

    return jsonify({
        "message": "Book updated successfully",
        "book": book.to_dict()
    })


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "message": "Book deleted successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)