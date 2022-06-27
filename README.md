# 🍪 CookieDB database

**CookieDB** is a noSQL document database developed in Python.
Using `JSON` as the document where all data is stored.

See a little about:

- Store information in various types of data;
- Encrypted database;
- `autocommit` options and encryption key definition;
- Easy access to data;
- Data search by path.

## Documentation

All **CookieDB** documentation is in the directory
[DOCS/](https://github.com/jaedsonpys/cookiedb/tree/master/DOCS) on GitHub,
there you go find database documentation and other functionality.

## Installation

To install **CookieDB**, use the `pip` package manager:

```
pip install cookiedb
```

## Demonstration of use

**Simple usage demo**, see full example in
[examples/example.py](https://github.com/jaedsonpys/cookiedb/blob/master/examples/example.py):

```python
from cookiedb import CookieDB

database = CookieDB()

database.create_database('MyDatabase')
database.open('MyDatabase')

database.create_item('languages', {
    'python': {
        'name': 'Python',
        'ext': '.py'
    },
    'cpp': {
        'name': 'C++',
        'ext': '.cpp'
    }
})

database.commit()

languages = database.get_item('languages')
print(f'All languages: {languages}')
```

## License

```
MIT License © 2022 by Jaedson Silva
```

This code is licensed under MIT license (see [LICENSE.txt](https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE)
for details)