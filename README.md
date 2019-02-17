[![Build Status](https://travis-ci.com/luqee/politico-api.svg?branch=develop)](https://travis-ci.com/luqee/politico-api)
[![Coverage Status](https://coveralls.io/repos/github/luqee/politico-api/badge.svg?branch=develop)](https://coveralls.io/github/luqee/politico-api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/3a787cadf8c622507598/maintainability)](https://codeclimate.com/github/luqee/politico-api/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/68b518b918fd44d7a161ee78c3922932)](https://www.codacy.com/app/luqee/politico-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=luqee/politico-api&amp;utm_campaign=Badge_Grade)
## POLITICO-API
Politico API is the back end to the Politico platform that enables citizens to give their mandate to politicians running for different government offices while building trust in the process through transparency.

## API Endpoints Included in this Branch 

| Http method  | EndPoint | Description |
| ------------- | ------------- |---------|
| POST  | /api/v1/auth/user/register  | Register a User |
| POST  | /api/v1/auth/user/login  | Login a User |
| POST  | api/v1/parties  | Create a political Party |
| GET | api/v1/parties/<int:party-id> | Get a single party |
| GET | api/v1/parties | Get all Parties |
| PATCH | api/v1/parties/<int:party-id> | Patch a party by Id |
| DELETE | api/v1/parties/<int:party-id> | Delete a party by Id |
| POST  | api/v1/offices  | Create a political Office |
| GET | api/v1/offices/<int:office-id> | Get a single Party |
| GET  | api/v1/offices  | Get all political Offices |
| PATCH | api/v1/offices/<int:office-id> | Update an Office by Id |
| DELETE | api/v1/offices/<int:office-id> | Delete an Office by Id |

## Installation Instructions
- Download or clone the contents of this repository.
  - `git clone https://github.com/luqee/politico-api`
- Set up and activate a virtual environment
  - `pip install virtualenv`
  - `virtualenv venv`
  - `source venv/bin/activate`
- Install required packages.
  - `pip install -r requriemnts.txt`
- Add the following environment variables
  - `export FLASK_APP=run.py`
  - `export SECRET=yoursecretkey`
- Run the application.
  - `flask run`

## Unit Testing
To Test the endpoint, ensure the following tools are available:
- pytest
- Postman/Insomnia
# Commands
 To run the tests and view coverage report use:
 - `coverage run --source=app -m py.test && coverage report`

## Deployment
[Click here](https://politico-api-heroku.herokuapp.com/) to access the app hosted on heroku.
After it opens, append the specific endpoint. i.e &lt;url&gt;/api/v1/auth/register

## Built with
- Python.
- Flask framework

## Author
Luke Nzang'u