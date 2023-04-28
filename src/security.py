from typing import Union
from datetime import datetime, timedelta
from jose import jwt
import hashlib
from db_api import check_user_credentials



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
# TOKEN VALIDATOR
# Validates if a given token is valid by checking the expiry time.
# If token is valid (ie. if expiry time not yet lapsed), returns True, else returns False.
# -----------------------------
def token_valid(
        secret_key, token
    ) -> bool:

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        expiry = datetime.utcfromtimestamp(payload.get("exp"))
        print("Validating token for %s, expires %s." % (payload.get("username"), expiry))
        if expiry > datetime.utcnow():
            return True
    except:
        pass
    return False

