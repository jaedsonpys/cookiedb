<h1 align="center">CookieDB database</h1>

<div style="display: flex; justify-content: center; margin-bottom: 15px">
    <div align="center">
        <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/jaedsonpys/cookiedb?include_prereleases">
    </div>
    <div align="center" style="margin-right: 5px; margin-left: 5px">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/cookiedb">
    </div>
    <div align="center">
        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/cookiedb">
    </div>
</div>

CookieDB is a noSQL database that uses the `document` model with all data encrypted, take advantage of the *performance and security* to create your projects that need a **quick storage** and are simple to use. Read the [CookieDB full documentation](https://jaedsonpys.github.io/cookiedb) to understand the methods available for creating, reading, updating and deleting data in the database.

## Getting started

First, let's start by performing a quick installation of CookieDB using the PIP package manager:

```
pip install cookiedb
```

Take a look at this **simple example of using** the database, where we create and get some data (the complete example can be found in [examples/example.py](https://github.com/jaedsonpys/cookiedb/blob/master/examples/example.py))

```python
from cookiedb import CookieDB

database = CookieDB(key='secret')
database.open('MyDatabase')

database.add('languages/python', {'name': 'Python', 'ext': '.py'})
python_ext = database.get('languages/python/ext')

print(f'Python extension: {python_ext}')
```

You can find more usage examples in the [examples/ directory](https://github.com/jaedsonpys/cookiedb/tree/master/examples)

# License

```
Apache License
Copyright 2023 Jaedson Silva
```

This project uses the *Apache License*, anyone can use this project as long as the license conditions allow. [See more about the license](https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE).