<h1 align="center">CookieDB</h1>
<p align="center">A safe, fast and simple database.</p>

<p align="center" style="margin-bottom: 15px">
    <a href="https://github.com/jaedsonpys/cookiedb/releases">
        <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/jaedsonpys/cookiedb?include_prereleases">
    </a>
    <a href="https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE" style="margin-right: 5px; margin-left: 5px">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/cookiedb">
    </a>
    <a href="https://pypi.org/project/cookiedb">
        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/cookiedb">
    </a>
</p>

CookieDB is a noSQL database that uses the `document` model with all data encrypted using AES-256, take advantage of *performance and security* to create your projects that need **fast storage** and simple to use, where you have full control over the data. Read the [full CookieDB documentation](https://jaedsonpys.github.io/cookiedb) to understand the methods available to create, read, update, and delete data in the database.

## Getting started

First, let's start by performing a quick installation of CookieDB using the PIP package manager:

```
pip install cookiedb
```

Take a look at this **simple example of using** the database, where we create and get some data (the complete example can be found in [examples/example.py](https://github.com/jaedsonpys/cookiedb/blob/master/examples/example.py))

```python
from cookiedb import CookieDB

database = CookieDB('MyDatabase', key='secret')
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
