# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Database APIs, for accessing the database and adding / changing the data.
# 
# =========================================================================

from sqlalchemy.engine import Engine
from db_builder import Recipient


# Create new aid recipient
def db_create_new_recipient(
        engine: Engine, 
        recipient: Recipient
    ):

    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(recipient)
        session.commit()


# =======================
# CHECK USER CREDENTIALS
# This function is used by the security.py module to check if the username and password are valid
# Parameters are username (string) and pwd_hash (string)
# It checks database to see if that user exists AND if that password hash matches
# If match, return True. Else return False.
# =======================
def check_user_credentials(
        username, 
        pwd_hash
    ) -> bool:

    # TODO

    return True