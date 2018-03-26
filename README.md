#LMNOP

## Live Music Notes, Opinions, Photographs


### To install

1. Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory.

2. pip install -r requirements.txt

3. python manage.py makemigrations lmn

4. python manage.py migrate

5. python manage.py runserver

Site at

127.0.0.1:8000

### Create superuser


`python manage.py createsuperuser`

enter username and password

will be able to use these to log into admin console at

127.0.0.1:8000/admin


### Run tests

To run tests  (some currently fail - see Issues)

python manage.py test lmn.tests

Or just some of the tests,
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in


### Functional Tests with Selenium

Install (upgrade to the latest version if you already have it) Firefox browser. It works best for automated functional testing with Selenium.

geckodriver needs to be in path or you need to tell Selenim where it is. Pick an approach: http://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path

python manage.py runserver

```
python manage.py test lmn.tests.functional_tests
```

### Test coverage

From directory with manage.py in it,

coverage run --source='.' manage.py test lmn.tests

coverage report


### Optional, if wanting to install and use with local postgresql

https://github.com/DjangoGirls/tutorial-extensions/blob/master/optional_postgresql_installation/README.md

Set admin password, remember it.

Start postgres running

`su postgres ` if on a mac/linux
`pg_ctl start`  enter username and password

start postgres shell with `psql`

And create a user called lmnop

```
create user lmnop with password 'password_here';
```

create a database lmnop

```
create database owner lmnop;
```

Various postgres shell commands
connect to lmnop database

```
\c lmnop
```

`\dt`    shows tables

`\d table_name`   shows info (and constraints) for a table
other sql as expected

postgres shell command cheatsheet - https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546

set environment variable called
POSTGRES_LMNOP_USER_PASSWORD
with a value of the lmnop user's password


Mac users may need to run these commands; these one time

```
sudo ln -s /Library/PosgreSQL/9.5/lib/libssl.1.0.0.dylib /usr/local/lib
sudo ln -s /Library/PosgreSQL/9.5/lib/libcrypto.1.0.0.dylib /usr/local/lib`
```

And this when you start a new shell; or set it permanently in .bash_profile
`export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.5/lib:$DYLD_LIBRARY_PATH`
