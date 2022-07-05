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
    version=__version__,
    long_description_content_type='text/markdown',
    long_description=full_doc,
    python_requires='>=3.6',
    license='GPL',
    packages=['cookiedb', 'cookiedb/database'],
    install_requires=['cryptography'],
    project_urls={
        'Source code': 'https://github.com/jaedsonpys/cookiedb',
        'License': 'https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE',
        'Documentation': 'https://github.com/jaedsonpys/cookiedb/tree/master/DOCS'
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers'
    ],
    keywords=['database', 'noSQL', 'document', 'JSON', 'cookiedb']
)
