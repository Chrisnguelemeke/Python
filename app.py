from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init marshmallow (for serializing to/from JSON)
ma = Marshmallow(app)


# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher


# Book Schema
class BookSchema(ma.Schema):
    id = ma.Integer()
    book_name = ma.String()
    author = ma.String()
    publisher = ma.String()

    class Meta:
        fields = ('id', 'book_name', 'author', 'publisher')

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Create a Book (CREATE)
@app.route('/book', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']

    new_book = Book(book_name, author, publisher)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


# Get All Books (READ)
@app.route('/book', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)


# Get Single Book (READ)
@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)


# Update a Book (UPDATE)
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']

    book.book_name = book_name
    book.author = author
    book.publisher = publisher

    db.session.commit()

    return book_schema.jsonify(book)


# Delete a Book (DELETE)
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)