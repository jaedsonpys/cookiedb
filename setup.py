from setuptools import setup

with open(f'README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='cookiedb',
    description='CookieDB is a noSQL document database.',
    version='7.0.0',
    long_description_content_type='text/markdown',
    long_description=readme,
    license='Apache License',
    install_requires=['pycryptodome==3.17'],
    packages=['cookiedb'],
    url='https://github.com/jaedsonpys/cookiedb',
    project_urls={
        'License': 'https://github.com/jaedsonpys/cookiedb/blob/master/LICENSE',
        'Documentation': 'https://github.com/jaedsonpys/cookiedb/tree/master/DOCS'
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database :: Database Engines/Servers'
    ],
    keywords=['database', 'noSQL', 'document', 'JSON', 'sql']
)
