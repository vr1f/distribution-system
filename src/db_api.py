# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Database APIs, for accessing the database and adding / changing the data.
# 
# =========================================================================

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from db_builder import User
from db_builder import Aid_Recipient


# =======================
# ADD NEW USER
# Creates new user in database
# =======================
def add_new_user(
        engine: Engine, 
        user: User
    ):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(user)
        session.commit()

# =======================
# CHECK USER CREDENTIALS
# This function is used by the security.py module to check if the username and password are valid
# Parameters are username (string) and pwd_hash (string)
# It checks database to see if that user exists AND if that password hash matches
# If match, return True. Else return False.
# =======================
def check_user_credentials(
        engine,
        username, 
        pwd_hash
    ) -> bool:

    from db_builder import User
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(User)
        user = query.filter(User.username == username).first()
        if user.password_hash == pwd_hash:
            return True
        else:
            return False

def add_aid_recipient(
        engine: Engine,
        aid_recipient: Aid_Recipient
    ):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(aid_recipient)
        session.commit()

    # ensure right table 
