# immunizationSJ

The current implementation uses [Flask](http://flask.pocoo.org/) as a basic web framework for displaying the results from the database. The database is populated from data originating in an Excel file which has been converted to CSV format which has then been input into `csv_to_sql.py` and `db_utils.py`.

## Preparing the Excel file for export to CSV

The provided Excel spreadsheets contain headers which span multiple columns. They also contain Unicode characters which do not readily transfer over to JSON or HTML without additional work or configuration.

The column headers should be changed and title information leading up to the actual rows of data should be removed, in addition to the symbol legend which is at the very bottom of the data set. The current column header titles can be seen in the `2014-15 CA Kindergarten Data.csv` file, and are:

    SCHOOL CODE,COUNTY,PUBLIC  PRIVATE,PUBLIC SCHOOL DISTRICT,CITY,SCHOOL NAME,ENROLLMENT,# UP-TO-DATE,% UP-TO-DATE,# CONDITIONAL,% CONDITIONAL,# PME,% PME,# PBE,% PBE,# PRE-JAN PBE,% PRE-JAN PBE,# HEALTH CARE PRACTITIONER COUNSELED PBE,% HEALTH CARE PRACTITIONER COUNSELED PBE,# RELIGIOUS PBE,% RELIGIOUS PBE,# DTP,% DTP,# POLIO,% POLIO,# MMR,% MMR,# HEPB,% HEPB,# VARI,% VARI,REPORTED

The file can then be saved or exported as a CSV that is ready for the next step.

##Using virtualenv (optional)

Install virtualenv via pip:

    $ pip install virtualenv

 Create virtualenv for this project:

     $ cd immunizationSJ
     $ virtualenv venv

 virtualenv venv will create a folder in immunizationSJ directory which will contain the Python executable files, and a copy of the pip library which you can use to install other packages. 

To begin using the virtual environment, it needs to be activated:

    . venv/bin/activate

The name immunizationSJ will now appear on the left of the prompt (e.g. (venv)Your-Computer:immunizationSJ UserName$) to let you know that it’s active. From now on, any package that you install using pip will be placed in the venv folder, isolated from the global Python installation.

Now install flask:
    pip install flask    

## Create the database
Run the provided `db_utils.py` utility program with the `create` option:

    python db_utils.py create

## Populate the database with the CSV data
Run the provided `csv_to_sql.py` utility program, giving arguments for the appropriate input file (-i), year (-y), and grade (-g):

    python csv_to_sql.py -i data/2014-15\ CA\ Kindergarten\ Data.csv -y 2014 -g K

## Run the app

Start the Flask application by running `app.py`:

    python app.py

With this running, open a web browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Screenshots

##### Example school record:
![example_school_record](https://github.com/codeforsanjose/ImmunizationSJ/blob/master/screenshots/example_school_record.png "Example School Record")
