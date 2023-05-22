# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Database Builder, on SQLAlchemy (using postgres). Build and design the database in this file.
#
# =========================================================================


from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Date, Float, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
import enum

Base  = declarative_base()


# =======================
# PRIVILEGES
# Helper class for enum user by 'USERS'
# =======================
class Privileges(enum.Enum):
    ADMIN = 1
    USER = 2

class Communication(str, enum.Enum):
    PHONE = 'phone'
    EMAIL = 'email'

class Size(str, enum.Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    XLarge = 'XL'

class Status(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Gender(str, enum.Enum):
    FEMALE = 'female'
    MALE = 'male'
    UNISEX = 'unisex'
    OTHER = 'other'

# =======================
# USERS
# Database class for system users (ie. anyone with a login / access)
# =======================
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password_hash = Column(String)
    access_level = Column(Enum(Privileges))

# =======================
# LOGIN_ATTEMPTS
# Database table to store single item = log in attempts
# =======================
class Login_Attempts(Base):
    __tablename__ = 'login_attempts'
    value = Column(Integer, primary_key=True, default=5)

# =======================
# LOCKOUT_PERIOD
# Database table to store single item = lockout period
# =======================
class Lockout_Period(Base):
    __tablename__ = 'lockout_period'
    value = Column(Float, primary_key=True, default=24.0)

# =======================
# LOCKOUT_LIST
# Database table to store list of usernames which are locked out
# =======================
class Lockout_List(Base):
    __tablename__ = 'lockout_list'
    username = Column(String, primary_key=True)
    lockout_expiry = Column(DateTime)

# =======================
# FAILED_LOGIN
# Database table to store all failed log-in attempts
# =======================
class Failed_Login(Base):
    __tablename__ = 'failed_login'
    login_attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    when = Column(DateTime)

# =======================
# PERSON
# Database class for persons. Used by Aid Recipient and Aid Donor child classes
# =======================
class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    nationality = Column(String)
    id_no = Column(String)
    id_expiry = Column(String)
    aid_recipient_db = relationship('Aid_Recipient_DB', backref='person', passive_deletes=True)
    document_id = Column(Integer, ForeignKey("sensitive_img.document_id", ondelete="CASCADE", onupdate="CASCADE"))



# =======================
# AID_RECIPIENT_DB
# Inherits person and collects additional details
# PK is a person_id from the Person table
# =======================
class Aid_Recipient_DB(Person):
    __tablename__ = 'aid_recipients'
    person_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    address = Column(String)
    n_family = Column(Integer)
    common_law_partner = Column(String)
    dependents = Column(String)
    __mapper_args__ = {'inherit_condition': person_id == Person.person_id}


# =======================
# AID_DONOR
# Inherits person and collects additional details of aid donors
# PK is a person_id from the Person table
# =======================
class Aid_Donor(Person):
    __tablename__ = 'aid_donors'
    donor_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    mail_address = Column(String)
    phone_number = Column(String)
    email_address = Column(String)
    preferred_comm = Column(Enum(Communication))
    org_name = Column(String)
    org_abn = Column(String)
    __mapper_args__ = {'inherit_condition': donor_id == Person.person_id}

# =======================
# Sensitive image table
# Store sensitive img files for both aid donor and aid recipient
# PK is a person_id from the Person table
# =======================
class Sensitive_Img(Base):
    __tablename__ = 'sensitive_img'
    document_id = Column(Integer, primary_key=True)
    img_1 = Column(LargeBinary, default=None)
    img_2 = Column(LargeBinary, default=None)
    img_3 = Column(LargeBinary, default=None)


# =======================
# CATEGORIES
# Defines a list of categories
# Each aid item belongs to a category
# =======================
class Categories(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    category_name = Column(String)
    status = Column(Enum(Status))

# =======================
# ITEM
# Base class to represent items
# Each aid item has a name, quantity and category
# =======================
class Item_DB(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    item_name = Column(String)
    item_quantity = Column(Integer)
    item_brand = Column(String)
    expiry_date = Column(Date)
    ingredients = Column(String)
    allergen_info = Column(String)
    size = Column(Enum(Size))
    category_id = Column(Integer, ForeignKey("category.category_id", ondelete="CASCADE", onupdate="CASCADE"))
    __mapper_args__ = {'inherit_condition': category_id == Categories.category_id}

# =======================
# AID_KIT
# Aid kits that include a combination of items
# Each aid kit has a name and description
# =======================
class Aid_Kit(Base):
    __tablename__ = 'aid_kit'
    aid_kit_id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    aidkit_name = Column(String)
    description = Column(String)

# =======================
# AID_KIT_ITEM
# Many-to-many relationship requires junction table
# Row is an item that belongs to a specific aid kit and
# includes quantity of the items in the kit
# =======================
class Aid_Kit_Item(Base):
    __tablename__ = 'aid_kit_item'
    id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    aid_kit_id = Column(Integer, ForeignKey("aid_kit.aid_kit_id", ondelete="CASCADE", onupdate="CASCADE"))
    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity = Column(Integer)

def build_db(engine):

    Base.metadata.create_all(engine)