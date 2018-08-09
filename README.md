# This is a demo project to learn python

## Assumptions
- A 'drop' is a negative priceMove of more than 10% in less than 10 hours. All klines are negative (should probably allow for small contra move)
- A 'raise' is a positive priceMove of more than 10% in less than 10 hours. All klines are positive
- A 'base' is a drop + a raise with less than 4 hours appart



### Challenges to resolve
- How to deploy python application on droplet with all the dependencies 
    - Using pipenv
     ` cd <projectname> `
     `pipenv --python 3.6` sets up the project to be a virtual environment with dependecies managed by pipenv.
     `pipenv shell` activates the virtual environment (must be done in terminal first thing every time)
     `pipenv install <packagename>` installs the python package into the virtual environment and writes it to the pipfile
     `pipenv uninstall --all-dev <package name>` removes package both from env and from pipfile
     `pipenv lock` creates a file: pipfile.lock to ensure deterministic builds (that all dependencies are exactly the right versions)
    - Using MySql with python
    `pipenv install mysql-connector-python-rf`
    - Configure visual code to use pipenv (to be able to debug and run code directly in terminal (without doing the `pipenv shell`))
        - https://olav.it/2017/03/04/pipenv-visual-studio-code/
    
    
- Modules in python
    - Create a subdirectory named lib.
    - Create an empty file named lib\__init__.py.
`from lib import <filename> as <alias>`
- Unit testing
    - `pipenv install pytest`
    - create a new file with name: test_<some name> 
    - inside create a function named: test_<some name>
    - inside it use assert expected == result
    - run it from terminal like: `python -m pytest` or `py.test` or `py.test -v` (v for verbose: see all details about the test runs when they fail) or `py.test -s` (-s will print all to console)
        - pytest will inspect all files and find those named 'test_* with functions named test_*