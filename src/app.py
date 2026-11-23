import io
import flask
from config import app
from db_helper import (
    add,
    add_article,
    add_conference_article,
    db,
    delete,
    get_all,
    get_by_id,
    update,
    search_books,
)
from sqlalchemy.exc import IntegrityError
import bibtex


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


def validate_article_data(form):
    """Return cleaned article data and an error message, if invalid."""
    fields = (
        "cite_key",
        "author",
        "title",
        "year",
        "journal",
        "volume",
        "number",
        "pages",
    )
    article = {field: form.get(field, "").strip() for field in fields}

    required_fields = {
        "cite_key": "Viiteavain",
        "author": "Tekijä",
        "title": "Nimi",
        "year": "Julkaisuvuosi",
        "journal": "Julkaisu",
    }
    missing = [
        label for field, label in required_fields.items()
        if not article[field]
    ]
    if missing:
        return None, f"Täytä pakolliset kentät: {', '.join(missing)}."

    try:
        article["year"] = int(article["year"])
    except ValueError:
        return None, "Julkaisuvuoden pitää olla kokonaisluku."

    if article["year"] <= 0:
        return None, "Julkaisuvuoden pitää olla positiivinen kokonaisluku."

    return article, None


def validate_conference_article_data(form):
    """Return cleaned conference article data and an error message."""
    fields = ("cite_key", "author", "title", "year", "booktitle")
    conference_article = {
        field: form.get(field, "").strip() for field in fields
    }

    required_fields = {
        "cite_key": "Viiteavain",
        "author": "Tekijä",
        "title": "Nimi",
        "year": "Julkaisuvuosi",
        "booktitle": "Kirja tai konferenssinimi",
    }
    missing = [
        label for field, label in required_fields.items()
        if not conference_article[field]
    ]
    if missing:
        return None, f"Täytä pakolliset kentät: {', '.join(missing)}."

    try:
        conference_article["year"] = int(conference_article["year"])
    except ValueError:
        return None, "Julkaisuvuoden pitää olla kokonaisluku."

    if conference_article["year"] <= 0:
        return None, "Julkaisuvuoden pitää olla positiivinen kokonaisluku."

    return conference_article, None


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
    reference_type = (
        flask.request.form.get("reference_type")
        or flask.request.form.get("type")
        or "book"
    )
    aliases = {
        "conference": "conference_article",
        "inproceedings": "conference_article",
        "konferenssiartikkeli": "conference_article",
        "artikkeli": "article",
        "kirja": "book",
    }
    reference_type = aliases.get(reference_type, reference_type)

    validators = {
        "book": validate_book_data,
        "article": validate_article_data,
        "conference_article": validate_conference_article_data,
    }
    validator = validators.get(reference_type)
    if validator is None:
        return flask.render_template(
            "add_book.html",
            error="Tuntematon viitteen tyyppi.",
            form=flask.request.form,
        ), 400

    reference, error = validator(flask.request.form)
    if error:
        return flask.render_template(
            "add_book.html", error=error, form=flask.request.form
        ), 400

    try:
        if reference_type == "article":
            add_article(**reference)
        elif reference_type == "conference_article":
            add_conference_article(**reference)
        else:
            add(**reference)
    except IntegrityError:
        db.session.rollback()
        return flask.render_template(
            "add_book.html",
            error="Viiteavain on jo käytössä.",
            form=flask.request.form,
        ), 400

    flask.flash("Viite lisättiin onnistuneesti.")
    return flask.redirect("/")

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book and redirect to the front page."""
    delete(book_id)
    return flask.redirect("/")


@app.route("/books/<int:book_id>/edit")
def edit_book(book_id):
    """Render the form for editing an existing book."""
    book = get_by_id(book_id)
    if book is None:
        flask.abort(404)
    return flask.render_template("edit_book.html", book=book)


@app.route("/books/<int:book_id>/edit", methods=["POST"])
@app.route("/books/<int:book_id>/update", methods=["POST"])
def update_book(book_id):
    """Update an existing book and redirect to the front page."""
    book = get_by_id(book_id)
    if book is None:
        flask.abort(404)

    updated_book, error = validate_book_data(flask.request.form)
    if error:
        return flask.render_template(
            "edit_book.html",
            error=error,
            book=flask.request.form,
        ), 400

    try:
        update(book_id, **updated_book)
    except IntegrityError:
        db.session.rollback()
        return flask.render_template(
            "edit_book.html",
            error="Viiteavain on jo käytössä.",
            book=flask.request.form,
        ), 400

    flask.flash("Kirjan tiedot päivitettiin onnistuneesti.")
    return flask.redirect("/")


@app.route("/bibtex")
def generate_bibtex():
    return flask.send_file(
        io.BytesIO(bibtex.generate(get_all()).encode()),
        download_name="viitteet.bib",
        mimetype="application/x-bibtex"
    )
