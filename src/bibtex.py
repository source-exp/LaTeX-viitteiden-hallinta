from collections.abc import Mapping


def _value(reference, field):
    if isinstance(reference, Mapping):
        return reference[field]
    return getattr(reference, field)


def _entry(book) -> str:
    return f"""@book{{{_value(book, "cite_key")},
    author    = "{_value(book, "author")}",
    title     = "{_value(book, "title")}",
    publisher = "{_value(book, "publisher")}",
    year      = {_value(book, "year")}
}}
"""


def _article_entry(article) -> str:
    optional_fields = ""
    for field in ("volume", "number", "pages"):
        value = _value(article, field)
        if value:
            optional_fields += f',\n    {field:<9} = "{value}"'

    return f"""@article{{{_value(article, "cite_key")},
    author    = "{_value(article, "author")}",
    title     = "{_value(article, "title")}",
    journal   = "{_value(article, "journal")}",
    year      = {_value(article, "year")}{optional_fields}
}}
"""


def _conference_article_entry(article) -> str:
    return f"""@inproceedings{{{_value(article, "cite_key")},
    author    = "{_value(article, "author")}",
    title     = "{_value(article, "title")}",
    booktitle = "{_value(article, "booktitle")}",
    year      = {_value(article, "year")}
}}
"""


def generate(books, articles=(), conference_articles=()) -> str:
    """Create BibTeX entries for books, articles, and conference articles."""
    entries = list(map(_entry, books))
    entries.extend(map(_article_entry, articles))
    entries.extend(map(_conference_article_entry, conference_articles))
    return "\n".join(entries)
