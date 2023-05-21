# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Database APIs, for accessing the database and adding / changing the data.
#
# =========================================================================

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from db.db_builder import User, Privileges, Login_Attempts, Lockout_Period, \
    Aid_Recipient_DB, Person, Categories, Lockout_List, Failed_Login, \
    Aid_Donor, Sensitive_Img, Item_DB
from support.responses import DatabaseActionResponse
from sqlalchemy import update
from datetime import datetime, timedelta

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
# ADD DEFAULT USER & ADMIN
# For dev purposes - called on start-up
# =======================
def add_default_user_admin(
        engine: Engine
    ):

    from support.security import hash_password

    default_user = User(
        username= "user",
        password_hash = hash_password("password"),
        access_level = "USER"
    )

    default_admin = User(
        username= "admin",
        password_hash = hash_password("password"),
        access_level = "ADMIN"
    )

    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(default_user)
        session.add(default_admin)
        session.commit()

# =======================
# ADD DEFAULT ADMIN SETTINGS
# eg default log-in attempts, lock out time, if hasn't been set yet. Called on start-up
# Checks if value already in DB. If not, adds default value.
# =======================
def add_default_admin_settings(
        engine: Engine
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        if session.query(Login_Attempts).count() == 0:
            session.add(Login_Attempts())
            session.commit()
        if session.query(Lockout_Period).count() == 0:
            session.add(Lockout_Period())
            session.commit()

# =======================
# UPDATE LOGIN ATTEMPTS
# Used by admin to update the number of login attempts
# Login attempts as Integer (number of attempts, default = 3)
# =======================
def update_login_attempts(
        engine: Engine,
        no_attempts: int
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        login_attempts = session.query(Login_Attempts).one()
        login_attempts.value = no_attempts
        session.commit()

# =======================
# GET LOGIN ATTEMPTS
# Get current login attempts setting
# Returns integer number of attempts before users are locked out
# =======================
def get_login_attempts(
        engine: Engine
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        login_attempts = session.query(Login_Attempts).one()
        return login_attempts.value

# =======================
# UPDATE LOCKOUT PERIOD
# Used by admin to update the lockout period when have more than x failed login attempts
# Lockout period in HOURS (as float, default 24)
# =======================
def update_lockout_period(
        engine: Engine,
        new_lockout_period: float
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        lockout_period = session.query(Lockout_Period).first()
        lockout_period.value = new_lockout_period
        session.commit()

# =======================
# GET LOCKOUT PERIOD
# Get current lockout period, following which user will be barred from login
# Returns float, being the number of hours locked out
# =======================
def get_lockout_period(
        engine: Engine
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        lockout_period = session.query(Lockout_Period).one()
        return lockout_period.value

# =======================
# GET LOCKOUT EXPIRY
# Check lockout_list for user and, if present and not expired, returns expiry time
# =======================
def get_user_lockout_expiry(
        engine: Engine,
        username: str
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(Lockout_List)
        user = query.filter(Lockout_List.username == username).first()
        if user is not None and user.lockout_expiry > datetime.now():
            return user.lockout_expiry
        else:
            return None

# =======================
# ADD / UPDATE LOCKOUT EXPIRY
# Check lockout_list for user and, if present and not expired, returns expiry time
# =======================
def update_or_add_user_lockout_expiry(
        engine: Engine,
        username: str,
        lockout_expiry: datetime
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(Lockout_List)
        user = query.filter(Lockout_List.username == username).first()
        if user is not None:
            user.lockout_expiry = lockout_expiry
        else:
            new_user_to_lockout = Lockout_List(username=username, lockout_expiry=lockout_expiry)
            session.add(new_user_to_lockout)
        session.commit()

# =======================
# ADD FAILED LOGIN
# Add the user-time of a failed login attempt
# =======================
def add_failed_login(
        engine: Engine,
        username: str
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        failed_login = Failed_Login(username=username, when=datetime.now())
        session.add(failed_login)
        session.commit()

# =======================
# GET REMAINING LOGINS
# Get the number of remaining logins
# =======================
def get_remaining_logins(
        engine: Engine,
        username: str,
        login_attempts_allowed: int
    ):

    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)

    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(Failed_Login)
        count = query.filter(
            Failed_Login.username == username,
            Failed_Login.when >= thirty_minutes_ago
        ).count()

    if login_attempts_allowed - count <= 0:
        return 0
    else:
        return login_attempts_allowed - count

# =======================
# ADD USER TO LOCKOUT LIST
# Add user to lockout list (called when remaining logins = 0)
# =======================
def add_user_to_lockout_list(
        engine: Engine,
        username: str,
        lockout_period: float
    ):

    Session = sessionmaker(bind=engine)
    with Session() as session:
        expiry = datetime.now() + timedelta(hours=lockout_period)
        lockout_list = Lockout_List(username=username, lockout_expiry=expiry)
        session.add(lockout_list)
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
# CHECK USER IS ADMIN
# =======================
def check_user_is_admin(
        engine,
        username
    ) -> bool:

    from db.db_builder import User
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(User)
        user = query.filter(User.username == username).first()
        if user.access_level == Privileges.ADMIN:
            return True
        else:
            return False

# =======================
# RETRIEVES ALL DATA WITHIN A TABLE
# Returns all data rows within the target table
# =======================
def get_table_rows(
        engine: Engine,
        table: str = ""
    ):
    Session = sessionmaker(bind=engine)

    if table == "aid_recipients":
        with Session() as session:
            rows = session.query(Aid_Recipient_DB).all()
            return rows

    if table == "aid_donors":
        with Session() as session:
            rows = session.query(Aid_Donor).all()
            return rows

    if table == "item":
        with Session() as session:
            rows = session.query(Item_DB).all()
            return rows

    return []

# =======================
# ADD SENSITIVE ID DOCUMENT
# Creates new record for storing ID documents
# =======================
def add_id_img_record(
        engine: Engine,
        new_images: Sensitive_Img
    ):
    response = DatabaseActionResponse()
    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(new_images)
            session.commit()
            response.id = new_images.document_id
    except Exception as e:
        response.error = e

    return response

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

# =======================
# ADD AID CATEGORY
# Adds an aid category to the database
# =======================
def add_aid_category(
        engine: Engine,
        category: Categories
    ):
    response = DatabaseActionResponse()

    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(category)
            session.commit()
            response.id = category.category_id
    except Exception as e:
        response.error = e

    return response

# =======================
# ADD AID ITEM
# Adds an aid category to the database
# =======================
def add_aid_item(
        engine: Engine,
        item: Item_DB
    ):
    response = DatabaseActionResponse()

    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(item)
            session.commit()
            response.id = item.item_id
    except Exception as e:
        response.error = e

    return response

# =======================
# ADD AID DONOR
# Adds an aid donor to the database
# =======================
def add_aid_donor(
        engine: Engine,
        donor: Aid_Donor
    ):
    response = DatabaseActionResponse()

    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(donor)
            session.commit()
            response.id = donor.donor_id
    except Exception as e:
        response.error = e

    return response
