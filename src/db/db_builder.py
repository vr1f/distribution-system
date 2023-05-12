# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Database Builder, on SQLAlchemy (using postgres). Build and design the database in this file.
#
# =========================================================================


from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Date, Float
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

class Size(enum.Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    XLarge = 'XL'

class Status(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

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
    value = Column(Integer, primary_key=True, default=3)

# =======================
# LOckOUT_PERIOD
# Database table to store single item = lockout period
# =======================
class Lockout_Period(Base):
    __tablename__ = 'lockout_period'
    value = Column(Float, primary_key=True, default=24.0)

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

# =======================
# AID_RECIPIENT_DB
# Inherits person and collects additional details
# PK is a person_id from the Person table
# =======================
class Aid_Recipient_DB(Person):
    __tablename__ = 'aid_recipients'
    person_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    address = Column(String)
    common_law_partner = Column(String)
    dependents = Column(String)
    __mapper_args__ = {'inherit_condition': person_id == Person.person_id}
    # person = relationship('Person', backref='aid_recipients', passive_deletes=True)

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
class Item(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True, autoincrement=True, onupdate="CASCADE")
    item_name = Column(String)
    item_quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.category_id", ondelete="CASCADE", onupdate="CASCADE"))
    __mapper_args__ = {'inherit_condition': category_id == Categories.category_id}

# =======================
# FOOD_ITEM
# Inherits Item class. Further includes food details
# PK is item_id from item table
# =======================
class Food_Item(Item):
    __tablename__ = 'food_item'
    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    expiry_date = Column(Date)
    ingredients = Column(String)
    allergen_info = Column(String)
    brand = Column(String)
    __mapper_args__ = {'inherit_condition': item_id == Item.item_id}

# =======================
# CLOTHING_ITEM
# Inherits Item class. Further clothing details
# PK is item_id from item table
# =======================
class Clothing_Item(Item):
    __tablename__ = 'clothing_item'
    item_id = Column(Integer, ForeignKey("item.item_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    size = Column(Enum(Size))
    brand = Column(String)
    __mapper_args__ = {'inherit_condition': item_id == Item.item_id}

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