# 🍪 CookieDB database

**CookieDB** is a noSQL document database developed in Python. Using `JSON` as the document where all data is stored.

See a little about:

- Store information in various types of data;
- Encrypted database;
- Easy access to data;
- Data search by path.

To install **CookieDB**, use the `pip` package manager:

```
pip install cookiedb
```

## Documentation

All **CookieDB** documentation is in the directory [DOCS/](https://github.com/jaedsonpys/cookiedb/tree/master/DOCS) on GitHub, there you go find database documentation and other functionality.

## Demonstration of use

**Simple usage demo**, see full example in [examples/example.py](https://github.com/jaedsonpys/cookiedb/blob/master/examples/example.py):

```python
from cookiedb import CookieDB

database = CookieDB()

database.create_database('MyDatabase')
database.open('MyDatabase')

database.add('languages', {
    'python': {
        'name': 'Python',
        'ext': '.py'
    },
    'cpp': {
        'name': 'C++',
        'ext': '.cpp'
    }
})

languages = database.get('languages')
print(f'All languages: {languages}')
```

## License

```
Apache License
Copyright 2023 Jaedson Silva
```

This project is licensed under Apache License (see [LICENSE](https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE) for details)