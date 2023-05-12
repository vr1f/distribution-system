from typing import Union
from datetime import datetime, timedelta
from jose import jwt
import hashlib

from db.db_api import (check_user_credentials,
                       check_user_is_admin,
                       get_user_lockout_expiry,
                       add_failed_login,
                       get_login_attempts,
                       get_remaining_logins,
                       add_user_to_lockout_list,
                       get_lockout_period)
from db.db_builder import Privileges
from fastapi import HTTPException, status, Response


# -----------------------------
# GET_TOKEN
# Function to get new token upon user log-in.
# Checks if user is locked_out, checks is username-password match (if not adds to failed log in log)
# If all valid, returns token. If not, raises exception with details in HTTPException 'details' field.
# -----------------------------
def get_token(
        engine,
        secret_key,
        access_token_expire_minutes,
        username,
        password,
        log
    ) -> Union[str , None]:

    try:

        # Check if user is currently locked out (bc too many log-in attempts):
        lock_out_time = get_user_lockout_expiry(engine,username)
        if lock_out_time != None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You have been locked out of the system until " + str(lock_out_time.strftime('%Y-%m-%d %H:%M')),
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            log.info("Checked lock out list. User " + username + " is authorised.")

        # Check username-password:
        pwd_hash = hash_password(password)
        if check_user_credentials(engine, username, pwd_hash):
            expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
            access_level = Privileges.ADMIN.value if check_user_is_admin(engine, username) else Privileges.USER.value
            data={"username": username, "exp": expire, "access_level": access_level}
            token = jwt.encode(data, secret_key, algorithm="HS256")
            return token
        else:
            log.info("User " + username + " password does not match.")
            add_failed_login(engine,username)
            login_attempts_allowed = get_login_attempts(engine)
            remaining_logins = get_remaining_logins(engine, username, login_attempts_allowed)
            if remaining_logins <= 0:
                lockout_period = get_lockout_period(engine)
                add_user_to_lockout_list(engine, username=username, lockout_period=lockout_period)
                log.info(username + " has exceeded valid login attempts. Locked out for " + str(lockout_period) + " hours.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You have exceeded your login attempts and are now locked out for " + str(lockout_period) + " hours.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                log.info(username + " has " + str(remaining_logins) + " remaining logins.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Your username and/or password did not match. You have " + str(remaining_logins) + " attempts remaining.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

    except HTTPException as e:

        raise(e)

    except:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify details",
            headers={"WWW-Authenticate": "Bearer"},
        )




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
        log.info("Token is valid.")
        raise HTTPException(
            status_code=307,
            detail="Token expired. Please log-in again.",
            headers={"Location": "/login"},
        )

# -----------------------------
# CHECK ADMIN
# Check if token is admin level access. If admin, return True.
# -----------------------------
def check_admin(secret_key, request, log):
    try:
        token = request.cookies['token'] if 'token' in request.cookies else ""
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        if payload.get("access_level") == Privileges.ADMIN.value:
            admin = True
            log.info("Valid admin user.")
        else:
            admin = False
    except:
        log.error("Unable to authenticate admin.")
        admin = False
    return admin
