# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Main entry point for application
# 
# =========================================================================



# Imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
import uvicorn
from sqlalchemy.exc import OperationalError


# Initialise log:
import logger
log = logger.get_logger()


# Get configurations
from config import get_config
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


# Connect to DB
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from db_builder import build_db
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


# =====================
#  Landing Page:
# =====================
@app.get("/")
def home(
        request: Request
    ) -> _TemplateResponse:
    log.info("'/' called from: " + str(request.client))
    return templates.TemplateResponse("index.html", {"request": request, "base_href": base_href})


# **Example API call**
# =====================
#  Add Aid recipients API:
# =====================
@app.get("/add_aid_recipient/")
def add_recipient(
        request: Request,
        new_recipient: dict
    ) -> dict:

    log.info("'/add_aid_recipient/' called from: " + str(request.client))
    from db_builder import Recipient
    from db_api import db_create_new_recipient
    new_recipient = Recipient(**new_recipient.dict())
    success = False
    try:
        db_create_new_recipient(new_recipient)
        success = True
    except:
        log.error("Unable to access database")
    return {'success':success}


# =====================
#  Run server:
# =====================
if __name__ == '__main__': 
    uvicorn.run(app, host=frontend_host,port=frontend_port)