[![Code Issues](http://www.quantifiedcode.com/api/v1/project/0094577cbd774ac9a1f3d0f220bf6a49/badge.svg)](http://www.quantifiedcode.com/app/project/0094577cbd774ac9a1f3d0f220bf6a49) Code Issues detected by Quantified Code - check them if you're looking for something to fix

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hanleybrand/rooibos?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) Chat/ask questions/etc - don't be shy!


# Madison Digial Image Database (MDID)

The [Madison Digital Image Database](http://mdid.org/) is a free, open source media repo aimed at education spaces.
It was created at [James Madison University](http://www.jmu.edu).

## Django 1.8.x upgrade - clone to a new directory

**Status:** Currently in a "for developers only/get it running" state - will work on an existing mdid3 installation's database, although obvs don't run it against a production database.

**This branch has the potential to mess up the organization of a django 1.2.7 based branch, so `git clone` to separate directory for testing**

I'm currently running it on OS X but I tried to make any settings changes as generic as possible (I made most if not all directories set relative to PROJECT_ROOT)

### setting up

I'd recommend making a fresh virtual env with python 2.7.x so everything has that 'oh-so-fresh' feeling!

I've been developing/testing this fork with an export of a production database and I haven't hit a snag, so right on!


### big change notes

- Switched static files to the staticfiles app, so a good start for running against an already existing database after setting up your virtualenv is:
``` shell 
pip install -f requirements.txt
./manage.py collectstatic
./manage.py migrate --fake-initial
./manage.py runserver
``` 

- Note that as of Django 1.7 migrations are a requirement, so you **must** run the `./manage.py migrate' command before starting or... bad things, I guess. The repo includes an untested, pre-generated migrations file so installation should not have to involve If you are working with a pre-existing database **copy** (please please do not run this against your production data!) you should use this command:
``` shell 
./manage.py migrate --fake-initial
``` 

- Following the newer django convention, moved the main app files to a 'project' directory, and followed [Jeff Knupp's advice](http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/) that this is really a 'config' directory, so settings file plus the main urls & wsgi files are in the PROJECT_ROOT/config directory, collected staticfiles are in PROJECT_ROOT/static, and local templates are in PROJECT_ROOT/templates.

- A goal is to get anything in rooibos.contrib out of that dir and to use the requirements.txt file to install libraries in the standard way (or remove them if no longer needed e.g. django-logging). 
    - [x] BeautifulSoup.py   
    - [ ] backends          
    - [ ] cloudfiles        
    - [x] compressor        
    - [x] django_extensions 
    - [x] djangologging     
    - [ ] google_analytics * (note this library may need a replacement found)
    - [ ] impersonate       
    - [ ] ipaddr.py         
    - [ ] pagination        
    - [ ] pyPdf             
    - [x] south             
    - [ ] sql_server        
    - [x] tagging           

