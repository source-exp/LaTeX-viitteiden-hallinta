def _entry(book) -> str:
    return f"""@book{{{book.cite_key},
    author    = "{book.author}",
    title     = "{book.title}",
    publisher = "{book.publisher}",
    year      = {book.year}
}}
"""

def generate(books) -> str:
    return "\n".join(map(_entry, books))
