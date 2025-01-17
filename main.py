# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)

# all_books = []


# @app.route('/')
# def home():
#     return render_template("index.html",books=all_books)


# @app.route("/add",methods=["GET", "POST"])
# def add():
#     if request.method=="POST":
#         new_book={
#             "title":request.form["title"],
#             "author":request.form["author"],
#             "rating":request.form["rating"]
#         }
#         all_books.append(new_book)
#     return render_template("add.html")


# # if __name__ == "__main__":
# #     app.run(debug=True)
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5001)



from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()



# @app.route('/')
# def home():
#     return render_template("index.html")
@app.route('/')
def home():
    # Fetch all books from the database
    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/add",methods=["GET", "POST"])
def add():
    if request.method=="POST":
        new_book=Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5001)


