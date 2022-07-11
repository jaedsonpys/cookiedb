# Change log of CookieDB versions

# 0.1.0

- [CookieDB 0.1.0 in PyPi](https://pypi.org/project/cookiedb/0.1.0/)
- [CookieDB 0.1.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v0.1.0)

## Aditions

- `CookieDB.create_database`: method to creating a database;
- `CookieDB.open`: method to open a database;
- `CookieDB.commit`: method to commit database changes;
- `CookieDB.create_item`: method to create item in database;
- `CookieDB.get_item`: method to get item from database.

# 1.0.0

- [CookieDB 1.0.0 in PyPi](https://pypi.org/project/cookiedb/1.0.0/)
- [CookieDB 1.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v1.0.0)

## Aditions

- [`d8d4b95`](https://github.com/jaedsonpys/cookiedb/commit/d8d4b95dca40ab1dac096e85a19878ffaa11c7ac): Adding ".cookiedb" extension to CookieDB files;
- [`a009f6a`](https://github.com/jaedsonpys/cookiedb/commit/a009f6a2aa000eb00bdf776088389f2d3aa84b13): Creating unit test using PySeqTest.

## Fixs

- [`f2ff9dc`](https://github.com/jaedsonpys/cookiedb/commit/f2ff9dcdd203acf8b973c74e45197e79fbecdec8): Adding empty character filter from "path_list".

# 1.1.0

- [CookieDB 1.1.0 in PyPi](https://pypi.org/project/cookiedb/1.1.0/)
- [CookieDB 1.1.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v1.1.0)

## Aditions

- [`938a0e3`](https://github.com/jaedsonpys/cookiedb/commit/938a0e3ff0617fe86a8e052b72e5bdb65dbfe8e9): Creating `NoOpenDatabaseError` class in exceptions.py;
- [`4ad55de`](https://github.com/jaedsonpys/cookiedb/commit/4ad55def9d49c9ab7651b34934499a116ce6e114): Creating decorator to check if there is an open database.

# 1.2.0

- [CookieDB 1.2.0 in PyPi](https://pypi.org/project/cookiedb/1.2.0/)
- [CookieDB 1.2.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v1.2.0)

## Aditions

- [`3b51b74`](https://github.com/jaedsonpys/cookiedb/commit/3b51b7411bebcc1b5fd10431542f47ac4eda958f): Adding method to delete items from database;
- [`0fbb070`](https://github.com/jaedsonpys/cookiedb/commit/0fbb0706a67bfaca50a1961c9f321d400368fd12): Adding license notice to files.

# 2.0.0

- [CookieDB 2.0.0 in PyPi](https://pypi.org/project/cookiedb/2.0.0/)
- [CookieDB 2.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v2.0.0)

## Improvements

- [`b832f56`](https://github.com/jaedsonpys/cookiedb/commit/b832f56): Renaming "wrapper" function to "decorator";
- [`60d27d5`](https://github.com/jaedsonpys/cookiedb/commit/60d27d5): Renaming `CookieDB.get_opened_database` method to `checkout`;
- [`cdac90f`](https://github.com/jaedsonpys/cookiedb/commit/cdac90f): Removing `Union[str, int]` from writing and reading methods;
- [`6ec1aff`](https://github.com/jaedsonpys/cookiedb/commit/6ec1aff): Renaming `CookieDB.create_item` method to `add`;
- [`6be7f84`](https://github.com/jaedsonpys/cookiedb/commit/6be7f84): Renaming `CookieDB.get_item` method to `get`;
- [`6be7f84`](https://github.com/jaedsonpys/cookiedb/commit/6be7f84): Renaming `CookieDB.get_item` method to `get`.

# 2.0.1

- [CookieDB 2.0.1 in PyPi](https://pypi.org/project/cookiedb/2.0.1/)
- [CookieDB 2.0.1 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v2.0.1)

## Fix

- [`1efebcf`](https://github.com/jaedsonpys/cookiedb/commit/1efebcf): Fixing database persistence error when committing new data;