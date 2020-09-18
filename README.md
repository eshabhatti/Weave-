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
3. run `python3 app.py`.

To disable the virtual environment after running, run `deactivate`.

## Language Installation

Download Python 3.5.8 from `https://www.python.org/downloads/`

Download Node.JS (npm) from `https://nodejs.org/en/`