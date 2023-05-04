# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Database APIs, for accessing the database and adding / changing the data.
#
# =========================================================================

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from db.db_builder import User
from db.db_builder import Aid_Recipient_DB, Person
from support.responses import DatabaseActionResponse
from sqlalchemy import update

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

    from db.db_builder import User
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(User)
        user = query.filter(User.username == username).first()
        if user is not None and user.password_hash == pwd_hash:
            return True
        else:
            return False

# =======================
# ADD AID RECIPIENT
# Creates new aid recipient in the database
# =======================
def add_aid_recipient(
        engine: Engine,
        aidrecipient: Aid_Recipient_DB
    ):
    response = DatabaseActionResponse()
    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(aidrecipient)
            session.commit()
            response.id = aidrecipient.person_id
    except Exception as e:
        response.error = e

    return response
# =======================
# UPDATE AID RECIPIENT
# Finds and updates an aid recipient's details
# =======================
def update_aid_recipient(
        engine: Engine,
        aidrecipient: Aid_Recipient_DB,
        person: Person
    ):
    temp_person = {
        "person_id":person.person_id,
        "first_name" :person.first_name,
        "age":person.age,
        "last_name":person.last_name
    }

    temp_ar = {
        "person_id":aidrecipient.person_id,
        'address': aidrecipient.address,
        'common_law_partner' : aidrecipient.common_law_partner,
        'dependents' : aidrecipient.dependents
    }

    response = DatabaseActionResponse(id=aidrecipient.person_id)
    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.query(Aid_Recipient_DB).filter(Aid_Recipient_DB.person_id ==
                                    aidrecipient.person_id).update(temp_ar)
            session.query(Person).filter(Person.person_id ==
                                    person.person_id).update(temp_person)
            session.commit()
    except Exception as e:
        response.error = e

    return response
# =======================
# DELETE AID RECIPIENT
# Finds and deletes an aid recipient from the database
# =======================
def delete_aid_recipient(
        engine: Engine,
        aidrecipient: Aid_Recipient_DB
    ):
    response = DatabaseActionResponse(id=aidrecipient.person_id)
    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            query = session.query(Aid_Recipient_DB)
            user_to_del = query.filter(Aid_Recipient_DB.person_id ==
                                    aidrecipient.person_id).one()
            session.delete(user_to_del)
            session.commit()
    except Exception as e:
        response.error = e
    
    return response