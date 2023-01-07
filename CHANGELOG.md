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
- [`6be7f84`](https://github.com/jaedsonpys/cookiedb/commit/6be7f84): Renaming `CookieDB.get_item` method to `get`.

# 2.0.1

- [CookieDB 2.0.1 in PyPi](https://pypi.org/project/cookiedb/2.0.1/)
- [CookieDB 2.0.1 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v2.0.1)

## Fix

- [`1efebcf`](https://github.com/jaedsonpys/cookiedb/commit/1efebcf): Fixing database persistence error when committing new data.

# 3.0.0

- [CookieDB 3.0.0 in PyPi](https://pypi.org/project/cookiedb/3.0.0/)
- [CookieDB 3.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v3.0.0)

## Improvements

- [`57c6019`](https://github.com/jaedsonpys/cookiedb/commit/57c6019): Adding `CookieDB._get_database_items` method;
- [`0c10824`](https://github.com/jaedsonpys/cookiedb/commit/0c10824): Removing commit option for user.

# 3.0.1

- [CookieDB 3.0.1 in PyPi](https://pypi.org/project/cookiedb/3.0.1/)
- [CookieDB 3.0.1 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v3.0.1)

## Improvements

- [`fc2eefe`](https://github.com/jaedsonpys/cookiedb/commit/fc2eefe): Update `CookieDB.add` method docstring;
- [`9540c14`](https://github.com/jaedsonpys/cookiedb/commit/9540c14): Adding method to filter item path;
- [`a491c86`](https://github.com/jaedsonpys/cookiedb/commit/a491c86): Filter empty string in `CookieDB.get` method.

# 3.0.2

- [CookieDB 3.0.2 in PyPi](https://pypi.org/project/cookiedb/3.0.2/)
- [CookieDB 3.0.2 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v3.0.2)

## Fix

- [`df37f99`](https://github.com/jaedsonpys/cookiedb/commit/df37f99): Removing `autocommit` from README.md.

# 3.0.3

- [CookieDB 3.0.3 in PyPi](https://pypi.org/project/cookiedb/3.0.3/)
- [CookieDB 3.0.3 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v3.0.3)

## Fix

- [`8cbc837`](https://github.com/jaedsonpys/cookiedb/commit/8cbc837): Avoiding exception by deleting the item only if it exists;
- [`e1fc339`](https://github.com/jaedsonpys/cookiedb/commit/e1fc339): Adding docstring to `CookieDB.delete` method.

# 4.0.0

- [CookieDB 4.0.0 in PyPi](https://pypi.org/project/cookiedb/4.0.0/)
- [CookieDB 4.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.0.0)

## Fix

- [`f3804c1`](https://github.com/jaedsonpys/cookiedb/commit/f3804c1): Creating `InvalidDatabaseKeyError` exception;
- [`1aa48c2`](https://github.com/jaedsonpys/cookiedb/commit/1aa48c2): Checking database encrypt key in `open` method.

# 4.1.0

- [CookieDB 4.1.0 in PyPi](https://pypi.org/project/cookiedb/4.1.0/)
- [CookieDB 4.1.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.1.0)

## Aditions

- [`0f3f795`](https://github.com/jaedsonpys/cookiedb/commit/0f3f795): Creating `ItemNotExistsError` exception;
- [`8dad755`](https://github.com/jaedsonpys/cookiedb/commit/8dad755): Adding `CookieDB.update` method to update existent items.

# 4.2.0

- [CookieDB 4.2.0 in PyPi](https://pypi.org/project/cookiedb/4.2.0/)
- [CookieDB 4.2.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.0)

## Aditions

- [`06cf483`](https://github.com/jaedsonpys/cookiedb/commit/06cf483): Adding method to close a open database.

# 4.2.1

- [CookieDB 4.2.1 in PyPi](https://pypi.org/project/cookiedb/4.2.1/)
- [CookieDB 4.2.1 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.1)

## Fix

- [`5439611`](https://github.com/jaedsonpys/cookiedb/commit/5439611): Changing condition to True if path getting is not None.

# 4.2.2

- [CookieDB 4.2.2 in PyPi](https://pypi.org/project/cookiedb/4.2.2/)
- [CookieDB 4.2.2 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.2)

## Improvements

- [`3859228`](https://github.com/jaedsonpys/cookiedb/commit/3859228): Removing CookieDB files from `database/` directory;
- [`31258a3`](https://github.com/jaedsonpys/cookiedb/commit/31258a3): Changing `cryptography` import in cookiedb.py.

# 4.2.3

- [CookieDB 4.2.3 in PyPi](https://pypi.org/project/cookiedb/4.2.3/)
- [CookieDB 4.2.3 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.3)

## Improvements

- [`443bea6`](https://github.com/jaedsonpys/cookiedb/commit/443bea6): Updating project requirements;
- [`72da046`](https://github.com/jaedsonpys/cookiedb/commit/72da046): Import `fernet` from `_document.py` file.

# 4.2.4

- [CookieDB 4.2.4 in PyPi](https://pypi.org/project/cookiedb/4.2.4/)
- [CookieDB 4.2.4 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.4)

## Improvements

- [`9f8eb8e`](https://github.com/jaedsonpys/cookiedb/commit/9f8eb8e): Removing `python_requires` from setup script.

# 4.2.5

- [CookieDB 4.2.5 in PyPi](https://pypi.org/project/cookiedb/4.2.5/)
- [CookieDB 4.2.5 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.5)

## Fix

- [`46ae46c`](https://github.com/jaedsonpys/cookiedb/commit/46ae46c): Adding version manually in setup script.

# 4.2.6

- [CookieDB 4.2.6 in PyPi](https://pypi.org/project/cookiedb/4.2.6/)
- [CookieDB 4.2.6 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.6)

## Fix

- [`9f4e7de`](https://github.com/jaedsonpys/cookiedb/commit/9f4e7de): Updating and adding docstring to `checkout()` method.

# 4.2.7

- [CookieDB 4.2.7 in PyPi](https://pypi.org/project/cookiedb/4.2.7/)
- [CookieDB 4.2.7 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v4.2.7)

## Fix

- [`f3dab3b`](https://github.com/jaedsonpys/cookiedb/commit/f3dab3b): Updating `cryptography` version in requirements;
- [`5933f5e`](https://github.com/jaedsonpys/cookiedb/commit/5933f5e): Updating `cryptography` version in setup script.

# 5.0.0

- [CookieDB 5.0.0 in PyPi](https://pypi.org/project/cookiedb/5.0.0/)
- [CookieDB 5.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v5.0.0)

## Fixs

- [`9a55821`](https://github.com/jaedsonpys/cookiedb/commit/9a55821): Removing `Fernet` key support;
- [`3579138`](https://github.com/jaedsonpys/cookiedb/commit/3579138): Change `generate_fernet_key` function to private.

# 6.0.0

- [CookieDB 6.0.0 in PyPi](https://pypi.org/project/cookiedb/6.0.0/)
- [CookieDB 6.0.0 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v6.0.0)

## Improves

- [`4136012`](https://github.com/jaedsonpys/cookiedb/commit/4136012): Create `InvalidKeyError` exception;
- [`b7e57f2`](https://github.com/jaedsonpys/cookiedb/commit/b7e57f2): Remove default key from `__init__()` method;
- [`4a9c283`](https://github.com/jaedsonpys/cookiedb/commit/4a9c283): Remove key decode from base64;
- [`a237527`](https://github.com/jaedsonpys/cookiedb/commit/a237527): Rename "key" argument in `JSONHandler.__init__()`;
- [`6165e18`](https://github.com/jaedsonpys/cookiedb/commit/6165e18): Rename `JSONHandler` class to Document;
- [`daa70c1`](https://github.com/jaedsonpys/cookiedb/commit/daa70c1): SecPickle library pre-implementation;
- [`715d0af`](https://github.com/jaedsonpys/cookiedb/commit/715d0af): Fix variable name in `create_document()` method;
- [`c2deb00`](https://github.com/jaedsonpys/cookiedb/commit/c2deb00): Rename encrypt and decrypt methods;
- [`da28691`](https://github.com/jaedsonpys/cookiedb/commit/da28691): Rename `_document.py` module import;
- [`c915a28`](https://github.com/jaedsonpys/cookiedb/commit/c915a28): Thrown `DatabaseNotFoundError` exception if document is not found;
- [`d270260`](https://github.com/jaedsonpys/cookiedb/commit/d270260): Implement faster method for writing and reading database files;
- [`c1b918e`](https://github.com/jaedsonpys/cookiedb/commit/c1b918e): Use `picke` module instead of `secpickle`;
- [`3bcf91d`](https://github.com/jaedsonpys/cookiedb/commit/3bcf91d): Improve condition in `create_database()` method;
- [`833a8d2`](https://github.com/jaedsonpys/cookiedb/commit/833a8d2): Change `_get_path_list()` method for more perfomance;
- [`fdd4a76`](https://github.com/jaedsonpys/cookiedb/commit/fdd4a76): Use `strftime` to format time.

# 6.0.1

- [CookieDB 6.0.1 in PyPi](https://pypi.org/project/cookiedb/6.0.1/)
- [CookieDB 6.0.1 in GitHub Release](https://github.com/jaedsonpys/cookiedb/releases/tag/v6.0.1)

## Improves

- [`577ef81`](https://github.com/jaedsonpys/cookiedb/commit/577ef81): Store length of list instead of calculating every iteration;
- [`3b861ed`](https://github.com/jaedsonpys/cookiedb/commit/3b861ed): Update `cryptography` library version.