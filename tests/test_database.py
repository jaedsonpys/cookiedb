import os

from pyseqtest import SeqTest
from cookiedb import CookieDB


class TestDatabase(SeqTest):
    def __init__(self):
        super().__init__()
        self.cookiedb: CookieDB

    def setup(self):
        if not os.path.isdir('./databases'):
            os.mkdir('./databases')

        self.programming_languages = {
            'python': {
                'extension': '.py',
                'name': 'Python'
            },
            'javascript': {
                'extension': '.js',
                'name': 'JavaScript'
            },
            'cpp': {
                'extension': '.cpp',
                'name': 'C++'
            },
            'typescript': {
                'extension': '.ts',
                'name': 'TypeScript'
            },
            'csharp': {
                'extension': '.cs',
                'name': 'C#'
            }
        }

        self.markup_languages = {
            'html': {
                'extension': '.html',
                'name': 'HTML'
            },
            'xhtml': {
                'extension': '.xhtml',
                'name': 'XHTML'
            },
            'xml': {
                'extension': '.xml',
                'name': 'XML'
            }
        }

        self.cookiedb = CookieDB(database_local='./databases', autocommit=True)

    def test_create_database(self):
        self.cookiedb.create_database('MyDatabase', if_not_exists=True)
        self.cookiedb.create_database('PySGIDatabase', if_not_exists=True)

        self.is_true(os.path.isfile('./databases/MyDatabase'), msg_error='"MyDatabase" not created')
        self.is_true(os.path.isfile('./databases/PySGIDatabase'), msg_error='"PySGIDatabase" not created')

    def test_create_items_1(self):
        self.cookiedb.create_item('languages/programming', self.programming_languages)
        self.cookiedb.create_item('languages/markup', self.markup_languages)


if __name__ == '__main__':
    TestDatabase().run()
