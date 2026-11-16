import flask
from config import app
from db_helper import add, get_all, delete


@app.route('/')
def index():
    books = get_all()
    return flask.render_template('index.html', books = books)

@app.route("/books/new")
def new_book():
    """Render the form for adding a new book."""
    return flask.render_template("add_book.html")


@app.route("/books", methods=["POST"])
def create_book():
    """Store a submitted book and redirect to the front page."""
    add(
        cite_key=flask.request.form["cite_key"],
        author=flask.request.form["author"],
        title=flask.request.form["title"],
        year=int(flask.request.form["year"]),
        publisher=flask.request.form["publisher"],
    )

    return flask.redirect("/")

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book and redirect to the front page."""
    delete(book_id)
    return flask.redirect("/")