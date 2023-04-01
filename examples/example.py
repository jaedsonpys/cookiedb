from cookiedb import CookieDB

database = CookieDB('MyDatabase', key='secret')

database.add('languages', {
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

# get items
languages = database.get('languages')
print(f'All languages: {languages}')

python_lang = database.get('languages/python')
print(f'Python language: {python_lang}')

javascript_ext = database.get('languages/javascript/ext')
print(f'JavaScript file extension: {javascript_ext}')
