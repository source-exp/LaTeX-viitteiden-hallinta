import unittest
from bibtex import generate
from dataclasses import dataclass

@dataclass
class Book:
    cite_key: str
    author: str
    title: str
    publisher: str
    year: int

class TestVarasto(unittest.TestCase):
    def test_bibtex(self):
        book = Book('key1', 'author1', 'title1', 'publisher1', 1)
        output = "".join(generate([book]).split()) # Remove all whitespace characters
        self.assertEqual(output, '@book{key1,author="author1",title="title1",publisher="publisher1",year=1}')

    def test_bibtex_with_articles_and_conference_articles(self):
        article = {
            "cite_key": "article-key",
            "author": "article author",
            "title": "article title",
            "journal": "journal name",
            "year": 2024,
            "volume": "5",
            "number": "2",
            "pages": "10-20",
        }
        conference_article = {
            "cite_key": "conference-key",
            "author": "conference author",
            "title": "conference title",
            "booktitle": "proceedings",
            "year": 2023,
        }

        output = generate([], [article], [conference_article])

        self.assertIn("@article{article-key,", output)
        self.assertIn('author    = "article author"', output)
        self.assertIn('journal   = "journal name"', output)
        self.assertIn('volume    = "5"', output)
        self.assertIn('number    = "2"', output)
        self.assertIn('pages     = "10-20"', output)
        self.assertIn("@inproceedings{conference-key,", output)
        self.assertIn('booktitle = "proceedings"', output)

