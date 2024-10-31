import os, urllib
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_session import Session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:root@localhost:27017/bookstore"
app.secret_key = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
mongo = PyMongo(app)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Display all books
@app.route('/books')
def books():
    books = mongo.db.books.find()
    return render_template('books.html', books=books)

# Book detail page
@app.route('/book/<book_id>')
def book_detail(book_id):
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('book_detail.html', book=book)

# Add a new book (Admin only)
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        mongo.db.books.insert_one({
            'title': title,
            'author': author,
            'price': price,
            'description': description,
            'stock': stock
        })
        flash('Book added successfully!')
        return redirect(url_for('books'))
    
    return render_template('add_book.html')

# Delete a book (Admin only)
@app.route('/delete/<book_id>')
def delete_book(book_id):
    mongo.db.books.delete_one({'_id': ObjectId(book_id)})
    flash('Book deleted successfully!')
    return redirect(url_for('books'))

if __name__ == '__main__':
    app.run(debug=True)
