# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Main entry point for application
#
# =========================================================================

# from pathlib import Path
# import os
# import sys
# print(Path.cwd())
# print(os.getcwd())

# ROOT_DIR = Path.cwd()
# sys.path.append("..")

# Imports
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
import uvicorn
from sqlalchemy.exc import OperationalError
from support.recipients import PersonID, AidRecipient
from support.responses import DatabaseActionResponse

# Initialise log:
import support.logger as logger
log = logger.get_logger()


# Get configurations
from support.config import get_config
config = get_config(log)
frontend_host = config.FRONTEND_HOST
frontend_port = config.FRONTEND_PORT
templates_dir = config.TEMPLATES_DIR
base_href = config.BASE_HREF
db_drivername = config.DB_DRIVERNAME
db_username = config.DB_USERNAME
db_host = config.DB_HOST
db_port = config.DB_PORT
db_database = config.DB_DATABASE
db_password = config.DB_PASSWORD
secret_key = config.SECRET_KEY
algorithm = config.ALGORITHM
access_token_expire_minutes = config.ACCESS_TOKEN_EXPIRE_MINUTES


# Connect to DB
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from db.db_builder import build_db
url = URL.create(
    drivername=db_drivername,
    username=db_username,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_database
)
try:
    engine = create_engine(url)
    build_db(engine)
    log.info("Successfully connected to DB")
except OperationalError:
    log.critical("Failed to connect to database.", exc_info=1)


# Start FastAPI app:
app = FastAPI()
templates = Jinja2Templates(directory=templates_dir)


# Cross-origin resource sharing configuration:
origin_url = "vr1family_example"
origins = [
    "https://" + origin_url + ".com",
    "https://www" + origin_url + ".com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serving static files for javascript
app.mount(
    path="/js",
    app=StaticFiles(directory="./src/js"),
    name="javascript"
)


# =====================
#  Landing Page:
# =====================
@app.get("/")
def home(
        request: Request
    ) -> _TemplateResponse:

    #TODO: Check token validity

    log.info("'/' called from: " + str(request.client))
    return templates.TemplateResponse("index.html", {"request": request, "base_href": base_href})


# =====================
# API ENDPOINT: ADD NEW USER
# Add new system user
# Parameters = dictionary containing fields: {'username':..., 'password':...}
# =====================
@app.post("/add_new_user/", status_code=201)
def add_new_user(
        request: Request,
        user: dict
    ) -> dict:

    log.info("'/add_new_user/' called from: " + str(request.client))
    from db.db_builder import User, Privileges
    from db.db_api import add_new_user
    from support.security import hash_password

    new_user = User(
        username= user['username'],
        password_hash = hash_password(user['password']),
        access_level = Privileges.USER  # Default privilege level is 'user'
    )
    try:
        add_new_user(engine, new_user)
        log.info("New user added: " + user['username'])
    except:
        log.error("Unable to add new user.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to add new user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {'username':user['username']}


# =====================
# API ENDPOINT: CHECK LOG-IN DETAILS & PROVIDE TOKEN
# It checks user credentials and, if valid, returns a JWT access token
# Return object = dictionary {token: string} (or 401 Error if invalid credentials)
# =====================
@app.post("/check_login", status_code=200)
async def login_for_access_token(
        request: Request,
        details: dict # dictionary containing fields: {'username':..., 'password':...}
    ) -> dict:

    log.info("'/check_login' called from: " + str(request.client))
    from support.security import get_token
    token = False
    try:
        token = get_token(engine, secret_key, access_token_expire_minutes, details['username'], details['password'])
    except:
        log.error("Unable to check token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify details",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"token": token}


# =====================
#  Page to view aid recipients
# =====================
@app.get("/aid_recipient")
def home(
        request: Request
    ) -> _TemplateResponse:

    #TODO: Check token validity

    log.info("'/aid_recipient' called from: " + str(request.client))

    html = templates \
        .TemplateResponse(
            "recipients.html", {"request": request, "base_href": base_href}
        )

    return html


# =====================
# API ENDPOINT: Create aid recipients in the system
# Check JWT access token
# Take request body as JSON
# Create entry in the DB
# Return object = dictionary {error: str|None, id: str|None}
# =====================
@app.post("/aid_recipient")
async def add_aid_recipient(
        request: Request,
        recipient: dict,
    ) -> dict:

    from db_builder import Aid_Recipient_DB
    from db_api import add_aid_recipient as add_a_r
    log.info("'/add_new_aid_recipient/' called from: " + str(request.client))

    new_recipient = Aid_Recipient_DB(
        first_name=recipient.get('first_name'),
        last_name=recipient.get('last_name'),
        age=recipient.get('age'),
        address=recipient.get('address'),
        common_law_partner=recipient.get('common_law_partner'),
        dependents=recipient.get('dependents')
    )
    try:
        add_a_r(engine, new_recipient)
        log.info("New recipient added: " + str(recipient))
    except:
        log.error("Unable to add aid recipient.")
    
    response = DatabaseActionResponse(
        id="123456",
        error=None
    )

    return response


# =====================
# API ENDPOINT: Create or overwrite aid recipients in the system
# Check JWT access token
# Take request body as JSON
# Create or overwrite entry in the DB
# Return object = dictionary {error: str|None, id: str|None}
# =====================
@app.put("/aid_recipient")
async def update_aid_recipient(
        recipient: AidRecipient,
    ) -> dict:

    # TODO
    # print(recipient)

    response = DatabaseActionResponse(
        id="123456",
        error=None
    )

    return response


# =====================
# API ENDPOINT: Delete aid recipients in the system
# Check JWT access token
# Take request body as JSON
# Delete entry in the DB
# Return object = dictionary {error: str|None, id: str|None}
# =====================
@app.delete("/aid_recipient")
async def delete_aid_recipient(
        request: Request,
        recipient: dict,
    ) -> dict:

    from db_builder import Aid_Recipient_DB
    from db_api import delete_aid_recipient as delete_a_r
    log.info("'/delete_aid_recipient/' called from: " + str(request.client))

    remove_recipient = Aid_Recipient_DB(
        person_id=recipient.get('id')
    )
    try:
        delete_a_r(engine, remove_recipient)
        log.info("Recipient deleted: " + str(recipient))
    except:
        log.error("Unable to delete recipient")

    response = DatabaseActionResponse(
        id="123456",
        error=None
    )

    return response


# =====================
#  Run server:
# =====================
if __name__ == '__main__':
    uvicorn.run(app, host=frontend_host,port=frontend_port)