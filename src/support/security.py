from typing import Union
from datetime import datetime, timedelta
from jose import jwt
import hashlib

from db.db_api import check_user_credentials

from fastapi import HTTPException, status, Response


# -----------------------------
# GET_TOKEN
# Function to get new token upon user log-in.
# It checks that username and password hash match on database.
# If credentials match, generates an access token and returns it.
# If no match, returns "None"
# -----------------------------
def get_token(
        engine,
        secret_key,
        access_token_expire_minutes,
        username,
        password
    ) -> Union[str , None]:

    pwd_hash = hash_password(password)

    if check_user_credentials(engine, username, pwd_hash):
        expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
        data={"username": username, "exp": expire}
        return jwt.encode(data, secret_key, algorithm="HS256")
    else:
        return False



# -----------------------------
# HASH_PASSWORD
# Input is password string. Returns hashed password
# -----------------------------
def hash_password(password) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# -----------------------------
# CHECK ACCESS
# Logic to review JWT token. Return True if valid token and has not yet expired.
# -----------------------------
def check_access(secret_key, request, log):
    try:
        token = request.cookies['token'] if 'token' in request.cookies else ""
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        expiry = datetime.utcfromtimestamp(payload.get("exp"))
        log.info("Validating token for " + str(payload.get("username"))+ ", expires " + str(expiry))
        access_granted =  True if expiry > datetime.utcnow() else False
    except:
        log.error("Unable to authenticate user.")
        access_granted = False
    return access_granted


# -----------------------------
# TOKEN VALIDATOR
# Use at every webpage end point to be behind log-in wall
# Raises HTTP exceptions if not valid token
# -----------------------------
def token_validator(secret_key, request, log):

    access_granted = check_access(secret_key, request, log)
    if not access_granted:
        log.info("User granted access.")
        raise HTTPException(
            status_code=307,
            detail="Token expired. Please log-in again.",
            headers={"Location": "/login"},
        )