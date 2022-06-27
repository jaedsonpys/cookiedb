from setuptools import setup
from cookiedb import __version__

doc_version = __version__.replace('.', '-')

with open(f'DOCS/database/{doc_version}.md', 'r') as reader:
    full_doc = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='cookiedb',
    description='CookieDB is a noSQL document database.',
    long_description_content_type='text/markdown',
    long_description=full_doc,
    version=__version__,
    license='MIT License',
    packages=['cookiedb', 'cookiedb/database'],
    install_requires=['cryptography'],
    project_urls={
        'Source code': 'https://github.com/jaedsonpys/cookiedb',
        'License': 'https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE',
        'Documentation': 'https://github.com/jaedsonpys/cookiedb/tree/master/DOCS'
    }
)
