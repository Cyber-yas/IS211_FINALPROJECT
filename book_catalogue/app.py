from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Manually create the database and tables when the app starts
with app.app_context():
    db.create_all()

# Home route to display all books
@app.route('/')
def home():
    books = Book.query.all()  # Retrieve all books from the database
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    
    new_book = Book(title=title, author=author, year=year)
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('home'))  # Redirect to the home page after adding a book

# Route to delete a book
@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)  # Find the book by ID or show a 404 if not found
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home'))  # Redirect to the home page after deleting the book

if __name__ == '__main__':
    app.run(debug=True)





