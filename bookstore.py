import os, urllib
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId 


bookstore = Flask(__name__)
bookstore.secret_key = os.environ.get('SECRET_KEY')

user = urllib.parse.quote_plus(os.environ.get('MONGO_USER'))
password = urllib.parse.quote_plus(os.environ.get('MONGO_PASS'))

uri = "mongodb://{}:{}@localhost:27017".format(user, password, os.environ.get('MONGO_HOST'), os.environ.get('MONGO_PORT'))
client = MongoClient(uri)
db = client['bookstore']

load_dotenv()
mongo = PyMongo(bookstore, uri=uri)

# Establish a connection to MongoDB
try:
    client = MongoClient(uri)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB connection successful!")

except ConnectionFailure as e:
    print("MongoDB connection failed:", e)

# Home Page
@bookstore.route('/')
def index():
    return render_template('index.html')

collection = db['books']
books = collection.find()

# Display all books

@bookstore.route('/books')
def books():
    books = collection.find()
    return render_template('books.html', books=books)

# Book detail page
@bookstore.route('/book/<id>')
def book_detail(id):
    _id = ObjectId(id)
    book = collection.find_one({'_id': _id})
    if book is None:
        return "Book not found", 404
    return render_template('book_detail.html', book=book)

# Add a new book (Admin only)
@bookstore.route('/add_book', methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        db.books.insert_one({
            'title': title,
            'author': author,
            'description': description,
            'price': price,
            'stock': stock         
        })
        flash('Book added successfully!')
        return redirect(url_for('books'))

    return render_template('add_book.html')

# Update a book (Admin only)
@bookstore.route('/update_book/<id>', methods=['GET', 'POST'])
def update_book(id):
    book = db.books.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        db.books.update_one({'_id': ObjectId(id)}, {'$set': {
            'title': title,
            'author': author,
            'description': description,
            'price': price,
            'stock': stock
        }})
        flash('Book updated successfully!')
        return redirect(url_for('books'))

    return render_template('update_book.html', book=book)


# Delete a book (Admin only)
@bookstore.route('/book/<id>', methods=['POST'])
def delete_book(id):
    db.books.find_one_and_delete({'_id': ObjectId(id)})
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

if __name__ == '__main__':
    bookstore.run(debug=True, port=9000)
