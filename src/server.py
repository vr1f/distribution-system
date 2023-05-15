# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Main entry point for application
#
# =========================================================================



# Imports
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
import uvicorn
from sqlalchemy.exc import OperationalError, IntegrityError
from support.recipients import PersonID, AidRecipient
from support.items import Category
from support.donor import AidDonor
from support.responses import DatabaseActionResponse
from support.security import token_validator, check_access, check_admin


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

# Add default user and admin profiles (for dev purposes)
from db.db_api import add_default_user_admin, add_default_admin_settings
try:
    add_default_user_admin(engine)
    log.info("Added default user and admin profiles to db.")
except IntegrityError:
    log.info("Default admin and user profiles already exist.")

# Check / add default admin settings:
try:
    add_default_admin_settings(engine)
    log.info("Checked default admin settings.")
except:
    log.error("Error checking default admin settings.")

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
    app=StaticFiles(directory="js"),
    name="javascript"
)


# =====================
#  PAGE: Log-in Page:
# =====================
@app.get("/login")
def login(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/' called from: " + str(request.client))
    if check_access(secret_key, request, log):
        log.info("User " + str(request.client) + " already logged in. Redirecting to homepage.")
        return Response(status_code=307, headers={"Location": "/home"})
    return templates.TemplateResponse("login.html", {"request": request, "base_href": base_href})


# =====================
#  PAGE: Home Page:
# =====================
@app.get("/")
@app.get("/home")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/home' called from: " + str(request.client))
    token_validator(secret_key, request, log)
    return templates.TemplateResponse("home.html", {"request": request, "base_href": base_href})

# =====================
#  PAGE: Admin Page:
# =====================
@app.get("/admin")
def admin(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/admin' called from: " + str(request.client))
    token_validator(secret_key, request, log)
    is_admin = check_admin(secret_key, request, log)
    return templates.TemplateResponse("admin.html", {"request": request, "base_href": base_href, "is_admin": is_admin})


# =====================
#  PAGE: View Search Page
# =====================
@app.get("/search")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/search' called from: " + str(request.client))
    token_validator(secret_key, request, log)

    html = templates \
        .TemplateResponse(
            "search.html", {"request": request, "base_href": base_href}
        )

    return html
# =====================
#  PAGE: View Aid recipients
# =====================
@app.get("/aid_recipient")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/aid_recipient' called from: " + str(request.client))
    token_validator(secret_key, request, log)

    html = templates \
        .TemplateResponse(
            "recipients.html", {"request": request, "base_href": base_href}
        )

    return html

# =====================
#  PAGE: View Inventory
# =====================
@app.get("/inventory")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/inventory' called from: " + str(request.client))
    token_validator(secret_key, request, log)

    html = templates \
        .TemplateResponse(
            "inventory.html", {"request": request, "base_href": base_href}
        )

    return html

# =====================
#  PAGE: View Aid donors
# =====================
@app.get("/aid_donor")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/aid_donor' called from: " + str(request.client))
    token_validator(secret_key, request, log)

    html = templates \
        .TemplateResponse(
            "donors.html", {"request": request, "base_href": base_href}
        )

    return html

# =====================
#  PAGE: View User Registration
# =====================
@app.get("/add_new_user")
def home(
        request: Request
    ) -> _TemplateResponse:

    log.info("'/add_new_user' called from: " + str(request.client))
    token_validator(secret_key, request, log)

    html = templates \
        .TemplateResponse(
            "user.html", {"request": request, "base_href": base_href}
        )

    return html

# =====================
# API ENDPOINT: ADD NEW USER
# Add new system user
# Parameters = dictionary containing fields: {'username':..., 'password':...}
# =====================
@app.post("/add_new_user", status_code=201)
def add_new_user(
        request: Request,
        user: dict
    ) -> dict:

    log.info("'/add_new_user' called from: " + str(request.client))
    from db.db_builder import User, Privileges
    from db.db_api import add_new_user
    from support.security import hash_password

    new_user = User(
        username= user['username'],
        password_hash = hash_password(user['password']),
        access_level = "ADMIN" if user['privilege'] == "1" else "USER"
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
    token = get_token(engine, secret_key, access_token_expire_minutes, details['username'], details['password'], log)
    log.info("Successful log in from " + str(request.client))
    return {"token": token}


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
        recipient: AidRecipient,
    ) -> dict:

    from db.db_builder import Aid_Recipient_DB
    from db.db_api import add_aid_recipient as add_a_r
    log.info("'/add_new_aid_recipient/' called from: " + str(request.client))

    new_recipient = Aid_Recipient_DB(
            first_name=recipient.first_name,
            last_name=recipient.last_name,
            age=recipient.age,
            address=recipient.address,
            common_law_partner=recipient.common_law_partner,
            dependents=recipient.dependents,
            nationality=recipient.nationality,
            id_no = recipient.id_no,
            id_expiry = recipient.id_expiry
        )

    response = add_a_r(engine, new_recipient)

    if response.error == None:
        log.info("New recipient added " + str(recipient))
    else:
        log.info("Unable to add recipient: " + str(response.error))
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
        request: Request,
        recipient: AidRecipient,
    ) -> dict:

    from db.db_builder import Aid_Recipient_DB, Person
    from db.db_api import update_aid_recipient as update_a_r
    log.info("'/update_aid_recipient/' called from: " + str(request.client))

    update_recipient = Aid_Recipient_DB(
                person_id=recipient.person_id,
                address=recipient.address,
                common_law_partner=recipient.common_law_partner,
                dependents=recipient.dependents
            )

    update_person = Person(
        person_id=recipient.person_id,
        first_name=recipient.first_name,
        last_name=recipient.last_name,
        age=recipient.age
    )

    response = update_a_r(engine, update_recipient, update_person)
    if response.error == None:
        log.info("Recipient updated: " + str(recipient.person_id))
    else:
        log.info("Unable to update recipeint: " + str(response.error))
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
        recipient: PersonID,
    ) -> dict:

    from db.db_builder import Aid_Recipient_DB
    from db.db_api import delete_aid_recipient as delete_a_r
    log.info("'/delete_aid_recipient/' called from: " + str(request.client))

    remove_recipient = Aid_Recipient_DB(
        person_id=recipient.person_id
    )

    response = delete_a_r(engine, remove_recipient)

    if response.error == None:
        log.info("Recipient deleted: " + str(recipient))
    else:
        log.info("Unable to delete recipeint: " + str(response.error))

    return response

# =====================
# API ENDPOINT: Add aid category
# Use Category data structure in support.items to get fields
# Convert it to a database object and call the relevant method from db_api.py
# =====================

@app.post("/aid_category")
async def add_aid_category(
        request : Request,
        category : Category,
    ) -> dict:

    from db.db_builder import Categories
    from db.db_api import add_aid_category as add_a_c
    log.info("'/aid_category/' called from: " + str(request.client))

    add_category = Categories(
        category_name=category.category_name,
        status=category.status
    )

    response = add_a_c(engine, add_category)

    if response.error == None:
        log.info("Category added: " + str(response.id))
    else:
        log.info("Unable to add category " + str(response.error))

    return response

# =====================
# API ENDPOINT: Add aid donor
# Receive an AidDonor data structure from input fields
# Convert it to a DB object and add it to the database
# =====================

@app.post("/aid_donor")
async def add_aid_category(
        request : Request,
        donor : AidDonor,
    ) -> dict:

    print(donor)

    from db.db_builder import Aid_Donor
    from db.db_api import add_aid_donor as add_a_d
    log.info("'/aid_donor/' called from: " + str(request.client))

    add_donor = Aid_Donor(
        first_name=donor.first_name,
        last_name=donor.last_name,
        age=donor.age,
        mail_address=donor.mail_address,
        phone_number=donor.phone_number,
        email_address=donor.email_address,
        preferred_comm=donor.preferred_comm
    )

    print(donor.preferred_comm)

    response = add_a_d(engine, add_donor)

    if response.error == None:
        log.info("Aid donor added: " + str(response.id))
    else:
        log.info("Unable to add donor " + str(response.error))

    return response

# =====================
# API ENDPOINT: GET CURRENT ADMIN SETTINGS
# Get configurable admin settings (to display on admin dashboard)
# Returns dictionary
# =====================
@app.get("/get_admin_settings", status_code=200)
async def get_admin_settings(
        request: Request
    ) -> dict:

    log.info("'/get_admin_settings' called from: " + str(request.client))
    token_validator(secret_key, request, log)
    if not check_admin(secret_key, request, log):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorised access.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from db.db_api import get_lockout_period, get_login_attempts
    try:
        lockout_period = get_lockout_period(engine)
        login_attempts = get_login_attempts(engine)
    except:
        log.error("Unable to get admin settings.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to get admin settings.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    log.info("Successfully obtained admin settings.")
    return templates.TemplateResponse("security.html", {"request": request, "base_href": base_href, "lockout_period": lockout_period, "login_attempts":login_attempts})

# =====================
# API ENDPOINT: UPDATE CURRENT ADMIN SETTINGS
# Update configurable admin settings (to display on admin dashboard)
# =====================
@app.post("/update_admin_settings")
async def get_admin_settings(
        request: Request,
        details: dict # dictionary containing fields: {'lockout_period': (as a float, in hours)..., 'login_attempts':...}
    ) -> dict:

    log.info("'/update_admin_settings' called from: " + str(request.client))
    token_validator(secret_key, request, log)
    if not check_admin(secret_key, request, log):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorised access.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from db.db_api import update_lockout_period, update_login_attempts
    try:
        update_lockout_period(engine, float(details['lockout_period']))
        update_login_attempts(engine, int(details['login_attempts']))
    except:
        log.error("Unable to update admin settings.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to update admin settings.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    log.info("Successfully updated admin settings.")
    return {"message":"successfully updated."}

# =====================
#  Run server:
# =====================
if __name__ == '__main__':
    uvicorn.run(app, host=frontend_host,port=frontend_port)