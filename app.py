import os, urllib
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId 


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

user = urllib.parse.quote_plus(os.environ.get('MONGO_USER'))
password = urllib.parse.quote_plus(os.environ.get('MONGO_PASS'))

uri = "mongodb://{}:{}@localhost:27017".format(user, password, os.environ.get('MONGO_HOST'), os.environ.get('MONGO_PORT'))
client = MongoClient(uri)
db = client['bookstore']

load_dotenv()
mongo = PyMongo(app, uri=uri)

# Establish a connection to MongoDB
try:
    client = MongoClient(uri)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB connection successful!")

except ConnectionFailure as e:
    print("MongoDB connection failed:", e)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

collection = db['books']
books = collection.find()

# Display all books

@app.route('/books')
def books():
    books = collection.find()
    return render_template('books.html', books=books)

# Book detail page
@app.route('/book/<id>')
def book_detail(id):
    _id = ObjectId(id)
    book = collection.find_one({'_id': _id})
    if book is None:
        return "Book not found", 404
    return render_template('book_detail.html', book=book)

# Add a new book (Admin only)
@app.route('/add_book', methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        stock = int(request.form['stock'])
        db.books.insert_one({
            'title': title,
            'author': author,
            'description': description,
            'stock': stock         
        })
        flash('Book added successfully!')
        return redirect(url_for('books'))

    return render_template('add_book.html')


# Delete a book (Admin only)
@app.route('/book/<id>', methods=['POST'])
def delete_book(id):
    db.books.find_one_and_delete({'_id': ObjectId(id)})
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

if __name__ == '__main__':
    app.run(debug=True, port=9000)
