# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Database Builder, on SQLAlchemy (using postgres). Build and design the database in this file.
# 
# =========================================================================


from sqlalchemy import Column,  String, Integer, Enum, ForeignKey
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


# =======================
# USERS
# Database class for system users (ie. anyone with a login / access)
# =======================
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password_hash = Column(String)
    access_level = Column(Enum(Privileges))

class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    children = relationship(
        "aid_recipients",
        back_populates="Person",
        cascade="all, delete",
    )
class Aid_Recipient_DB(Person):
    __tablename__ = 'aid_recipients'
    person_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE"), primary_key=True)
    address = Column(String)
    common_law_partner = Column(ForeignKey("person.person_id"))
    dependents = Column(String)
    
    __mapper_args__ = {
        'inherit_condition': person_id == Person.person_id
    }


def build_db(engine):

    Base.metadata.create_all(engine)