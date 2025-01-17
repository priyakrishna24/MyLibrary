from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Initialize the Flask application
app = Flask(__name__)

# CREATE DATABASE
# Define a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Configure the application to use a SQLite database called 'books.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"

# Create an instance of the SQLAlchemy class, passing the base class for model definitions
db = SQLAlchemy(model_class=Base)

# Initialize the app with the SQLAlchemy extension
db.init_app(app)

# CREATE TABLE
# Define a Book model class that will map to a table in the database
class Book(db.Model):
    # Define columns for the Book table
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)  # Title of the book
    author: Mapped[str] = mapped_column(String(250), nullable=False)  # Author of the book
    rating: Mapped[float] = mapped_column(Float, nullable=False)  # Rating of the book

# Create the table in the database if it doesn't exist yet
with app.app_context():
    db.create_all()

# Route to the homepage
@app.route('/')
def home():
    # READ ALL RECORDS
    # Create a query to select all books from the database, ordered by title
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Use .scalars() to extract individual book objects from the result
    all_books = result.scalars().all()
    # Render the home page with the list of all books
    return render_template("index.html", books=all_books)

# Route to add a new book
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD: When the form is submitted
        # Create a new Book object with the data from the form
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        # Add the new book to the session and commit to save it to the database
        db.session.add(new_book)
        db.session.commit()
        # After adding the book, redirect to the home page
        return redirect(url_for('home'))
    # If the method is GET, render the form for adding a new book
    return render_template("add.html")

# Route to edit the rating of an existing book
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD: When the form is submitted with updated information
        book_id = request.form["id"]
        # Use db.get_or_404 to fetch the book by ID, or return a 404 error if not found
        book_to_update = db.get_or_404(Book, book_id)
        # Update the rating of the book
        book_to_update.rating = request.form["rating"]
        # Commit the changes to the database
        db.session.commit()
        # After updating, redirect to the home page
        return redirect(url_for('home'))
    # If the method is GET, render the edit page for the specific book
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit_rating.html", book=book_selected)

# Route to delete an existing book by ID
@app.route("/delete")
def delete():
    # Fetch the book ID from the query parameters
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    # Use db.get_or_404 to find the book by ID, or return a 404 if not found
    book_to_delete = db.get_or_404(Book, book_id)
    # Alternative way to select the book for deletion (commented out)
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # Delete the book from the session
    db.session.delete(book_to_delete)
    # Commit the changes to the database to remove the book
    db.session.commit()
    # After deleting the book, redirect to the home page
    return redirect(url_for('home'))

# Run the app when this script is executed
if __name__ == "__main__":
    app.run(debug=True,port=5001)
