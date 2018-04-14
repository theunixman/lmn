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

```
python manage.py test lmn.tests
```

Or just some of the tests,

```
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in
```


### Functional Tests with Selenium

Install (upgrade to the latest version if you already have it) Firefox browser. It works best for automated functional testing with Selenium.

Make sure you have the latest version of Firefox, and the most recent geckodriver, and latest Selenium.

geckodriver needs to be in path or you need to tell Selenium where it is. Pick an approach: http://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path

If your DB is at GCP, your tests might time out, and you might need to use longer waits http://selenium-python.readthedocs.io/waits.html

Start your server with `python manage.py runserver` and then

```
python manage.py test lmn.tests.functional_tests
```

Or select tests, for example,
```
python manage.py test lmn.tests.functional_tests.HomePageTest
python manage.py test lmn.tests.functional_tests.BrowseArtists.test_searching_artists
```


### Test coverage

From directory with manage.py in it,

```
coverage run --source='.' manage.py test lmn.tests

coverage report
```


### Optional, if wanting to install and use with local postgresql

A local PostgreSQL server will be faster than a GCP one.
https://github.com/DjangoGirls/tutorial-extensions/tree/master/en/optional_postgresql_installation

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

TROUBLESHOOTING:

'pip' not being recognized as internal or external command, if you use pycharm you probably need to restarting pycharm.
If you don't use pycharm or that doesn't work, make sure you are in your virtual environment.

CSS not updating: try using an incognito window so CSS isn't stored while you work on it.

If you installed requirements, but your console can't find them, make sure you are in your virtual environment. You
should see a (venv) at the beginning of your terminal prompt. This will be the name of your virtual environment so if
you named yours 'myvenv', it should display (myvenv).

requirements issues: make sure requirements in requirements.txt are all spelled correctly such as 'Pillow' vs 'pillo'
and if a version can't be found, look up the latest valid version to make sure you have a valid version listed.

If attributes or columns can't be found or 'already exist': you probably made changes to your database that overwrite
current database so drop/delete your database and recreate it. Dont forget to remake your SUPERUSER FROM YOUR TERMINAL.
This does not mean the user that owns your database.

If your terminal can't recognize a requirement, clean-install it, meaning UNINSTALL before reinstalling. This can be
necessary for requirements that have been working for months.

If you can't run this program with these instructions, try changing your selenium version in requirements.txt to 3.11.0
and try using 'ALTER DATABASE lmnop OWNER TO lmnop;' instead of the line in the instructions.

If python, pip, psql, git, or anything else isn't recognized in your terminal, find the path they were installed in and
ADD THEM TO YOUR COMPUTER PATH VARIABLE this means do NOT replace your current path variable, just append.

If you change your code and you're not seeing the changes apply to your page and restarting your server isn't doing it,
restart your IDLE or code-editor.

If teammate's code works on their computer, but not on yours be aware of your URL. If you refresh because you were just
on your own version of the project, you might be in the middle of a process that their version does not know how to
handle or that their program hasn't been updated to your version yet.

If you use an unsupported version of MAC, you might need XCODE from the appstore. Last I heard, a lot of versions are
free. I don't know EXACTLY what it does, but I know it has helped people be able to run code in python, java and C
languages while using old MACS.

If 'django' isnt recognized, you just opened a repo of a program on your computer or python is not recognized on a
recently created copy of a repo, you may need to delete your virtual environment and recreate your virtual environment.
Make sure to activate it afterwards, then install requirements.

If you are running different versions of your program or you are looking at a friend's repo, I do this every time I
change between those repos: follow the next paragraph of instructions:

If you are trying to view/run changes to your program or view someone else's version, or nothing else works: delete/drop
your database, recreate a new one, make sure you're in virtual environment, update pip (if it fails, that's usualy okay,
but look into it if this STILL doesn't work), install requirements.txt using command line (don't do it through pycharm),
delete everything in your 'migrations' folder except for '__init__', create migrations, migrate, create superuser,
runserver, open incognito browser, start from default port and good luck.
