# 🍪 CookieDB database

CookieDB is an *extremely optimized* noSQL database using the **key-value** model, with encrypted databases, you can enjoy the performance, security and ease of using CookieDB. To install **CookieDB**, use the `pip` package manager:

```
pip install cookiedb
```

- [Documentation](https://jaedsonpys.github.io/cookiedb)
- [PyPI Project](https://pypi.org/project/cookiedb)

## Demonstration of use

**Simple usage demo**, see full example in [examples/example.py](https://github.com/jaedsonpys/cookiedb/blob/master/examples/example.py):

```python
from cookiedb import CookieDB

database = CookieDB(key='secret')
database.open('MyDatabase')

database.add('languages/python', {'name': 'Python', 'ext': '.py'})
python_ext = database.get('languages/python/ext')

print(f'Python extension: {python_ext}')
```

## License

```
Apache License
Copyright 2023 Jaedson Silva
```

This project is licensed under Apache License (see [LICENSE](https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE) for details)
