# =========================================================================
# 
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
# 
# Database Builder, on SQLAlchemy (using postgres). Build and design the database in this file.
# 
# =========================================================================


from sqlalchemy import Column,  String, Integer
from sqlalchemy.orm import relationship, declarative_base

Base  = declarative_base()

# Example class = Aid Recipients:
class Recipient(Base):
    __tablename__ = 'recipients'
    recipient_id  = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    previous_address = Column(String)
    total_fam_mem = Column(Integer)
    partner_name = Column(String)
    partner_age = Column(String)
    events = relationship('Event', backref='job')

def build_db(engine):

    Base.metadata.create_all(engine)