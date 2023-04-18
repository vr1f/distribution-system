# SWEN90016 Project
## Semester 1, 2023




# VR1 Family Charity Distribution IT System


# Installation

1. Create a new pip virtual environment locally. Use **Python 3.10.9**: `python -m venv /path/to/new/virtual/environment`

2. Activate the virtual environment: `Scripts\activate`

3. Install requirements using pip: `pip install requirements.txt`

# Local run

To run locally with a local database, you need to install Postgres (https://www.postgresql.org/download/). You will need to select a username and password when installing Postgres. These details will be needed to access the database locally. See the config.py file to see how this is handled. 

Currently, the username is hard coded in to config.py and the password needs to be manually entered (so that your personal password is not in the repo). You will also need to create a new database within postgres with the name 'vr1_db1'. Using pgAdmin4 desktop tool makes all this much easier.

# AWS Deployment

When the code is deployed on Docker & AWS, the DockerConfig settings should be activated instead of the local settings. This config retrieves 'environment variables' which need to be particularised in the AWS build software (and again, are not hard coded into the repo for security reasons). 

Take the deployment database, for example. It will be on a separate AWS instance. It is currently set up so that the details of this instance will be kept in AWS Secrets Manager, and retrieved by AWS Elastic Beanstalk and inserted as environment variables during deployment.

# Front-end Bootstrap

See https://getbootstrap.com/docs/5.3/getting-started/introduction/ for the html code templates. These can be copied and pasted into the html templates, and amended as required. Note the `% block content %` decorators which are used to stitch the 'index' html pages together within the 'base' html page.

Note the version we are using is 5.3, but it is easy to accidentally access the documentation from earlier versions.

# Calling REST APIs

BOTH the 'frontend' (ie. that return html pages) and the 'backend' (ie. that interact with the database and perform other logic) APIs will be accessible from `server.py`. 

The 'front-end' APIs are called just by going to the http address in the decorator (whilst the server is running). Local environments should be accessible at localhost:8000 in your browser.

The 'back-end' APIs will be called via javascript embedded in the html templates. These are activated when, for example, a button is clicked by the user. They typically use the javascript 'fetch' method to send a json / dictionary object to the API endpoint.
