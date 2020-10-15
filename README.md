# Weave

## Dependency Installation

If python3 or npm/node is not installed on your machine, see the `Language Installation` section before installing dependencies.

### Python (backend)
cd to the `api/` folder to begin.

1. Run `python3 -m venv venv` to initialize the python virtual environment.
2. Run `source venv/bin/activate` to enter the environment on MacOS/Linux.
   (Run `venv\Scripts\activate` to do so on Windows.)
3. Run `pip install -r requirements.txt` to install all relevant dependencies.

To disable the virtual environment after installing, run `deactivate`.


### Node (frontend)
cd to the `frontend/` folder to begin.

1. Run `npm install` to install all modules.

## Running Project

### frontend
cd to the `frontend/` directory and run `npm start.`

### backend
1. cd to `api/`
2. Run `source venv/bin/activate` to initialize the virtual environment on MacOS/Linux.
   (To do so on Windows, run `venv\Scripts\activate`.)
3. run `python3 api.py`.

To disable the virtual environment after running, run `deactivate`.

## Language Installation

Download Python 3.5.8 from `https://www.python.org/downloads/`

Download Node.JS (npm) from `https://nodejs.org/en/`

## Database Installation and Initialization

1. Download MySQL Community Workbench and Server from `https://dev.mysql.com/downloads/installer/`
2. Once your community server is initialized locally, add a file `\api\credentials\dbcredentials.txt` with your database username on the first line and your database password on the second.
3. Run the file `db/init/createtables.sql` in MySQL workbench to create all the tables needed to run Weave. 
4. If the database needs to be updated (that is, if the creation file has been changed), run the file `db/init/droptables.sql` in MySQL workbench and then re-run `db/init/createtables.sql`.
