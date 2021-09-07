# create virtual environment
pipenv --three
# or
pipenv --python 3.8

# spawn a subshell and activate/create virtual environment
pipenv shell 

# install a module (like pip)
pipenv install flask

# install from github repo
pipenv install git+(repo_url)@(branch_or_tag_or_version)#(package_name)

# install in dev mode (not for production)
pipenv install flask --dev

# create pipfile.lock for deterministic dependency resolution
pipenv lock

# install from lock , not from basic pipfile
# if it fails, it will generate a new lock that works
pipenv install --ignore-pipfile

# install in production
# --deploy installs specified versions from lock
# --system installs in system path, not virtual environment
pipenv install --system --deploy

# install dev version
pipenv install --dev

# print graph of dependencies
pipenv graph (--reverse) # reverse may be easier to resolve dependencies

# open installed package in editor
pipenv open flask

# run command in virtual environment without shell
pipenv run (command)

# check for security vulnerabilities
pipenv check

# uninstall package (--all for everything) 
pipenv uninstall (package) (--all)

# print where virtual environment and project home are located
pipenv --venv
pipenv --where

# install from requirement files
pipenv install -r (dev-)requirements.txt (--dev)

# generate requirements.txt from a pipfile
pipenv lock -r > requirements.txt
pipenv lock -r -d > dev-requirements.txt





