from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)

class Base(DeclarativeBase):

  pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

db = SQLAlchemy(model_class=Base)

db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

# CREATE RECORD
# with app.app_context():
#     new_book = Book(title="Tetor", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":

        with app.app_context():
            new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "GET":
        with app.app_context():
            book = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
        return render_template('edit.html', book=book)
    elif request.method == "POST":
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
            book_to_update.rating = request.form["rating"]
            db.session.commit()

        return redirect(url_for('home'))

@app.route('/delete')
def delete():
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

