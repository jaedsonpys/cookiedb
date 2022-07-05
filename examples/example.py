from cookiedb import CookieDB

database = CookieDB(database_local='./')
database.create_database('MyDatabase', if_not_exists=True)
database.open('MyDatabase')

database.create_item('languages', {
    'python': {
        'name': 'Python',
        'ext': '.py'
    },
    'javascript': {
        'name': 'JavaScript',
        'ext': '.js'
    },
    'cpp': {
        'name': 'C++',
        'ext': '.cpp'
    }
})

# commit database changes
database.commit()

# get items
languages = database.get_item('languages')
print(f'All languages: {languages}')

python_lang = database.get_item('languages/python')
print(f'Python language: {python_lang}')

javascript_ext = database.get_item('languages/javascript/ext')
print(f'JavaScript file extension: {javascript_ext}')
