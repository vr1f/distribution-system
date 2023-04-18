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
