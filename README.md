#LMNOP

## Live Music Notes, Opinions, Photographs

###Install postgresql

https://github.com/DjangoGirls/tutorial-extensions/blob/master/optional_postgresql_installation/README.md

Set admin password, remember it.

start postgres shell

- Create a user called lmnop

create user lmnop;

- set lmnop user password

alter user lmnop with password 'password_here';

- create a database lmnop

create database owner lmnop;

- connect to lmnop

\c lmnop

\dt    shows tables
\d table_name   shows info (and constraints) for a table
other sql as expected

set environment variable called
POSTGRES_LMNOP_USER_PASSWORD
with a value of the lmnop user's password


postgres shell command cheatsheet - https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546

(Mac users:

  sudo ln -s /Library/PosgreSQL/9.5/lib/libssl.1.0.0.dylib /usr/local/lib
  sudo ln -s /Library/PosgreSQL/9.5/lib/libcrypto.1.0.0.dylib /usr/local/lib

  export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_LIBRARY_PATH

)

###To install

1. Create and activate a virtual environment. Use Python3 as the interpreter.

2. pip install -r requirements.txt

3. cd LMNOP/LMNOPSite

4. python manage.py makemigrations lmn

5. python manage.py migrate

6. python manage.py runserver

Site at

127.0.0.1:8000

###Create superuser

from LMNOP/LMNOPSite

python manage.py createsuperuser

enter username and password

will be able to use these to log into admin console at

127.0.0.1:8000/admin

To run tests  (some currently fail - see Issues)

python manage.py test lmn.tests

### Install selenium
