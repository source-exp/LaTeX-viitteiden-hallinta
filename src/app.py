import flask
from config import app
from db_helper import add, db, delete, get_all, search_books
from sqlalchemy.exc import IntegrityError


def validate_book_data(form):
    """Return a cleaned book and an error message, if the data is invalid."""
    fields = ("cite_key", "author", "title", "year", "publisher")
    book = {field: form.get(field, "").strip() for field in fields}

    required_fields = {
        "cite_key": "Viiteavain",
        "author": "Tekijä",
        "title": "Nimi",
        "year": "Julkaisuvuosi",
        "publisher": "Kustantaja",
    }
    missing = [
        label for field, label in required_fields.items() if not book[field]
    ]
    if missing:
        return None, f"Täytä pakolliset kentät: {', '.join(missing)}."

    try:
        book["year"] = int(book["year"])
    except ValueError:
        return None, "Julkaisuvuoden pitää olla kokonaisluku."

    if book["year"] <= 0:
        return None, "Julkaisuvuoden pitää olla positiivinen kokonaisluku."

    return book, None


@app.route('/')
def index():
    query = flask.request.args.get("q", "").strip()
    author = flask.request.args.get("author", "").strip()
    title = flask.request.args.get("title", "").strip()
    year = flask.request.args.get("year", "").strip()

    if query:
        found = {}
        searches = [search_books(author=query), search_books(title=query)]
        try:
            int(query)
            searches.append(search_books(year=query))
        except ValueError:
            pass

        for books in searches:
            for book in books:
                found[book["id"]] = book
        books = sorted(found.values(), key=lambda book: book["id"], reverse=True)
    elif author or title or year:
        books = search_books(author=author, title=title, year=year)
    else:
        books = get_all()

    return flask.render_template(
        "index.html",
        books=books,
        query=query,
    )

@app.route("/books/new")
def new_book():
    """Render the form for adding a new book."""
    return flask.render_template("add_book.html")


@app.route("/books", methods=["POST"])
def create_book():
    """Store a submitted book and redirect to the front page."""
    book, error = validate_book_data(flask.request.form)
    if error:
        return flask.render_template(
            "add_book.html", error=error, form=flask.request.form
        ), 400

    try:
        add(**book)
    except IntegrityError:
        db.session.rollback()
        return flask.render_template(
            "add_book.html",
            error="Viiteavain on jo käytössä.",
            form=flask.request.form,
        ), 400

    flask.flash("Kirja lisättiin onnistuneesti.")
    return flask.redirect("/")

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book and redirect to the front page."""
    delete(book_id)
    return flask.redirect("/")