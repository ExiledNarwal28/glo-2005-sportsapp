# SportsApp

![Build](https://github.com/ExiledNarwal28/glo-2005-sportsapp/workflows/Build/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/ExiledNarwal28/glo-2005-sportsapp/branch/master/graph/badge.svg?token=R9AKC1L5PE)](https://codecov.io/gh/ExiledNarwal28/glo-2005-sportsapp)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5716b95dcc114147ac758590d14c22bc)](https://www.codacy.com/manual/ExiledNarwal28/glo-2005-sportsapp?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ExiledNarwal28/glo-2005-sportsapp&amp;utm_campaign=Badge_Grade)
[![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/)

**This is a school project that was submitted with a report explaining the project and how to use it. Said report was migrated into our [wiki](https://github.com/ExiledNarwal28/glo-2005-sportsapp/wiki) for educational purposes.**

This is our project for course GLO-2005 at Laval University. We are team 8.

This project is about listing sports, practice centers, shops and equipments.

Our app also features a list of shops that display announces for equipment. It is built using Flask and Python.

## Installation

First, you will need [Python](https://www.python.org/downloads/).

Then, you will need to create a MySQL database. This database must fit the information displayed in [instance/flask.cfg](instance/flask.cfg).

## Prepare database

First, check that the MySQL service is well running on `localhost:3306`.

### Access MySQL CLI
On windows, using MySQL Shell :

```shell script
\connect --mysql root@localhost:3306
# Enter root password
```

On UNIX, using `mysql` CLI : 

```shell script
mysql -u root -p
# Enter root password
```

### Create database
Now, on Windows or UNIX (Windows needs to add `\sql` before each query)

```mysql
CREATE USER 'sportsapp'@'localhost' IDENTIFIED BY 'sportsapp';
GRANT ALL PRIVILEGES ON *. * TO 'sportsapp'@'localhost';
CREATE DATABASE 'sportsapp';
CREATE DATABASE 'sportsapp_test';
SET GLOBAL log_bin_trust_function_creators=1;
```

## Install requirements

```shell script
pip install -q -r requirements.txt
```

## Run app

Choose one option for running the app : 

```shell script
python ./run.py
python ./run.py -c  # or --db-create : create database tables
python ./run.py -p  # or --db-populate : populate database with mock data
python ./run.py -cp # usually what you want
```

By default, web API is hosted on port `5000` : [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Run tests

```shell script
nose2 -v --with-coverage tests
```

## Lint app and tests

```shell script
pylint --output-format=text app
pylint --output-format=text tests
```
