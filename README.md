
# **Bookstore E-commerce Web App** 📚

A basic e-commerce web application for managing and selling books, built with **Flask** and **MongoDB**. The app allows users to browse available books, view detailed information, and (as an admin) add or delete books.

---

## **Table of Contents**

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Installation and Setup](#installation-and-setup)  
4. [Project Structure](#project-structure)  
5. [Usage](#usage)  
6. [Future Improvements](#future-improvements)  
7. [Contributing](#contributing)  
8. [License](#license)  
9. [Contact](#contact)  
10. [Screenshots](#screenshots)  

---

## **Features**

- 📖 **View Books**: Browse all available books with title, author, and price.  
- 🛒 **Book Details**: View detailed information about each book, including description and stock.  
- ➕ **Add Book**: Admin users can add new books to the collection.  
- ❌ **Delete Book**: Admin users can remove books from the collection.  
- 🌐 **Dynamic Content**: Data is retrieved in real-time from a MongoDB database.

---

## **Technologies Used**

- **Backend**: Flask (Python)  
- **Database**: MongoDB  
- **Frontend**: HTML, CSS  
- **Dependencies**: Flask-PyMongo, pymongo  

---

## **Installation and Setup**

### **Prerequisites**

- **Python 3.x** installed  
- **MongoDB** server running locally or on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### **Step-by-Step Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/samirhimi/bookstore-app.git
   cd bookstore-app
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Start the MongoDB Server:**

   For a local MongoDB server, ensure it's running on mongodb://localhost:27017.
   For MongoDB Atlas, update the connection string in app.py

   ```bash

