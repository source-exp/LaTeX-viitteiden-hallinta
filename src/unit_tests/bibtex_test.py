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

