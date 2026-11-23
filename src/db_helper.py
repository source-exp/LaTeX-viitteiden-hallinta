from config import db, app
from sqlalchemy import text
import os


def reset_db():
    print("Clearing contents from reference tables")
    sql = text("DELETE FROM conference_articles")
    db.session.execute(sql)
    sql = text("DELETE FROM articles")
    db.session.execute(sql)
    sql = text("DELETE FROM books")
    db.session.execute(sql)
    db.session.commit()


def tables():
    """Returns all table names from the database"""
    sql = text(
      "SELECT name FROM sqlite_master "
      "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def setup_db():
    """
        Creating the database
        If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read().strip()

    for statement in schema_sql.split(";"):
        statement = statement.strip()
        if statement:
            db.session.execute(text(statement))
    db.session.commit()


def add(cite_key, author, title, year, publisher):
    """Add a book reference to the database and return its id."""
    sql = text(
        """
        INSERT INTO books (cite_key, author, title, year, publisher)
        VALUES (:cite_key, :author, :title, :year, :publisher)
        """
    )
    result = db.session.execute(sql, {
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
    })
    db.session.commit()
    return result.lastrowid


def update(book_id, cite_key, author, title, year, publisher):
    """Update a book reference by id."""
    sql = text(
        """
        UPDATE books
        SET cite_key = :cite_key,
            author = :author,
            title = :title,
            year = :year,
            publisher = :publisher
        WHERE id = :id
        """
    )
    result = db.session.execute(sql, {
        "id": book_id,
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
    })
    db.session.commit()
    return result.rowcount


def get_all():
    """Return all book references, newest first."""
    sql = text(
        "SELECT id, cite_key, author, title, year, publisher "
        "FROM books ORDER BY id DESC"
    )
    return db.session.execute(sql).mappings().all()


def get_by_id(book_id):
    """Return a book reference by id, or None if it does not exist."""
    sql = text(
        "SELECT id, cite_key, author, title, year, publisher "
        "FROM books WHERE id = :id"
    )
    return db.session.execute(
        sql, {"id": book_id}
    ).mappings().first()


def delete(book_id):
    """Delete a book reference by id."""
    sql = text("DELETE FROM books WHERE id = :id")
    db.session.execute(sql, {"id": book_id})
    db.session.commit()


def add_article(cite_key, author, title, journal, year,
                volume=None, number=None, pages=None):
    """Add an article reference to the database and return its id."""
    sql = text(
        """
        INSERT INTO articles
            (cite_key, author, title, journal, year, volume, number, pages)
        VALUES
            (:cite_key, :author, :title, :journal, :year,
             :volume, :number, :pages)
        """
    )
    result = db.session.execute(sql, {
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": number,
        "pages": pages,
    })
    db.session.commit()
    return result.lastrowid


def update_article(article_id, cite_key, author, title, journal, year,
                   volume=None, number=None, pages=None):
    """Update an article reference by id."""
    sql = text(
        """
        UPDATE articles
        SET cite_key = :cite_key,
            author = :author,
            title = :title,
            journal = :journal,
            year = :year,
            volume = :volume,
            number = :number,
            pages = :pages
        WHERE id = :id
        """
    )
    result = db.session.execute(sql, {
        "id": article_id,
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": number,
        "pages": pages,
    })
    db.session.commit()
    return result.rowcount


def get_all_articles():
    """Return all article references, newest first."""
    sql = text(
        "SELECT id, cite_key, author, title, journal, year, "
        "volume, number, pages FROM articles ORDER BY id DESC"
    )
    return db.session.execute(sql).mappings().all()


def get_article_by_id(article_id):
    """Return an article reference by id, or None if it does not exist."""
    sql = text(
        "SELECT id, cite_key, author, title, journal, year, "
        "volume, number, pages FROM articles WHERE id = :id"
    )
    return db.session.execute(
        sql, {"id": article_id}
    ).mappings().first()


def delete_article(article_id):
    """Delete an article reference by id."""
    sql = text("DELETE FROM articles WHERE id = :id")
    db.session.execute(sql, {"id": article_id})
    db.session.commit()


def add_conference_article(cite_key, author, title, year, booktitle):
    """Add a conference article reference and return its id."""
    sql = text(
        """
        INSERT INTO conference_articles
            (cite_key, author, title, year, booktitle)
        VALUES
            (:cite_key, :author, :title, :year, :booktitle)
        """
    )
    result = db.session.execute(sql, {
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "year": year,
        "booktitle": booktitle,
    })
    db.session.commit()
    return result.lastrowid


def update_conference_article(conference_article_id, cite_key,
                              author, title, year, booktitle):
    """Update a conference article reference by id."""
    sql = text(
        """
        UPDATE conference_articles
        SET cite_key = :cite_key,
            author = :author,
            title = :title,
            year = :year,
            booktitle = :booktitle
        WHERE id = :id
        """
    )
    result = db.session.execute(sql, {
        "id": conference_article_id,
        "cite_key": cite_key,
        "author": author,
        "title": title,
        "year": year,
        "booktitle": booktitle,
    })
    db.session.commit()
    return result.rowcount


def get_all_conference_articles():
    """Return all conference article references, newest first."""
    sql = text(
        "SELECT id, cite_key, author, title, year, booktitle "
        "FROM conference_articles ORDER BY id DESC"
    )
    return db.session.execute(sql).mappings().all()


def get_conference_article_by_id(conference_article_id):
    """Return a conference article by id, or None if it does not exist."""
    sql = text(
        "SELECT id, cite_key, author, title, year, booktitle "
        "FROM conference_articles WHERE id = :id"
    )
    return db.session.execute(
        sql, {"id": conference_article_id}
    ).mappings().first()


def delete_conference_article(conference_article_id):
    """Delete a conference article reference by id."""
    sql = text(
        "DELETE FROM conference_articles WHERE id = :id"
    )
    db.session.execute(sql, {"id": conference_article_id})
    db.session.commit()

def search_books(author=None, title=None, year=None):
    """Search books by author, title and year. All filters are combined."""
    conditions = []
    params = {}

    if author and author.strip():
        conditions.append("LOWER(author) LIKE LOWER(:author)")
        params["author"] = f"%{author.strip()}%"

    if title and title.strip():
        conditions.append("LOWER(title) LIKE LOWER(:title)")
        params["title"] = f"%{title.strip()}%"

    if year:
        try:
            year = int(year)
            conditions.append("year = :year")
            params["year"] = year
        except (TypeError, ValueError):
            pass

    sql = (
        "SELECT id, cite_key, author, title, year, publisher "
        "FROM books"
    )

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY id DESC"

    return db.session.execute(text(sql), params).mappings().all()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
