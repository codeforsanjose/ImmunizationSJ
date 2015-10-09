# immunizationSJ
The current implementation uses [Django](https://www.djangoproject.com/) as a web framework for displaying the results from the database. The database is populated from data originating from [data.ca.gov](https://cdph.data.ca.gov/).

## Using virtualenv (optional)
Install virtualenv via pip:

    $ pip install virtualenv

 Create virtualenv for this project:

     $ cd immunizationSJ
     $ virtualenv venv

 virtualenv venv will create a folder in immunizationSJ directory which will contain the Python executable files, and a copy of the pip library which you can use to install other packages. 

To begin using the virtual environment, it needs to be activated:

    . venv/bin/activate

## Setup development environment
The name immunizationSJ will now appear on the left of the prompt (e.g. (venv)Your-Computer:immunizationSJ UserName$) to let you know that it’s active. From now on, any package that you install using pip will be placed in the venv folder, isolated from the global Python installation.

Now install django and all the required packages:
    pip install -r requirements.txt

## Create the database
Run the Django commands for making the database:
    $ python manage.py syncdb
    $ python manage.py makemigrations
    $ python manage.py migrate

Once that's done, create a superuser for yourself, the following is fine, as this is just for your own use:
    username : admin
    password : password

## Populate the database
(more information to come here)

## Start the development server
Start the Django application by using the `runserver` option in manage.py:

    $ python manage.py runserver

With this running, open a web browser to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should be greeted with the main page, and you should be able to get to the admin console at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), and login with the superuser account you created earlier.

## Populate the database
First, find a dataset you want to look at, like the [Kindergarten 2014-2015 Immunizations dataset](https://cdph.data.ca.gov/Healthcare/School-Immunizations-In-Kindergarten-2014-2015/4y8p-xn54) and find the SODA API endpoint under `export`>`SODA API`. The endpoint will look like this:
    https://cdph.data.ca.gov/resource/4y8p-xn54.json
The UID we need is the part before `.json`, in this case, it's `4y8p-xn54`. In the Django administration console, create a new dataset, using that UID and fill in all the fields that are available for that dataset, as they correspond to the fields shown in the SODA API tab below where the endpoint was located. Not all of the fields will be present, like `Hib`. Once you have this filled in and saved, stop the development webserver.

Now go into the Django shell and run the update_db function:
    $ python manage.py shell
    >>> from data.tasks import update_db; update_db();

## Screenshots

##### Example school record:
![example_school_record](https://github.com/codeforsanjose/ImmunizationSJ/blob/master/screenshots/example_school_record.png "Example School Record")
