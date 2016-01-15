# About stockanalyzer

# Setup Development Environment

## Create a virtual environments

[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is a tool that keep the depencies of the python
project in a seperate place. To create a virtualenv you need to install this package first:

```
$sudo pip install virtualenv
```

Then you need to create a virtualenv, python2.7-venv is the name of the directory that save the copied python environment
and the dependencies of the virtual environment:

```
$cd ~/
$virtualenv python2.7-venv
```

Then you need to activate the environment.

```
$source python2.7-venv/bin/activate
```

After that you can install packages to this virtual environment, these packages are isolated from the global environment.

```
$pip install pandas
$pip install matplotlib
$pip install pandas_datareader
$pip install ta-lib
```

**Notes**: [Ta-lib](https://github.com/mrjbq7/ta-lib) is hard to install, you should install the dependent lib first: `brew install ta-lib`.

To deactivate the environment:

```
$deactivate
```

## Intellij setup

Open "Project Structure", you can add a new SDK by selecting the `python` file under the `bin` directory of the virtual
environment directory. The project will use this virtual environment to execute the python scripts.

