# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures and methods for air donors
#
# =========================================================================
from pydantic import BaseModel
from support.recipients import Person
import enum

NO_KNOWN_ADDRESS = "NO_KNOWN_ADDRESS"
NO_LAST_NAME = "NO_LAST_NAME"

class Communication(str, enum.Enum):
    EMAIL = 'email'
    PHONE = 'phone'

class AidDonor(Person):

    """
    A data item representing an aid donor

    Args:
        donor_id (int): id for the database
        mail_address (str): physical mailing address
        phone_number (str): mobile or landline
        email_address (str): email address
        preferred_comm (str): select either email or phone as the preferred mode of communication
        org_name (str): name of organisation if applicable
        org_abn (str): abn of organisation if applicable
    """
    donor_id: int = None
    mail_address: str = NO_KNOWN_ADDRESS
    phone_number: str
    email_address: str
    preferred_comm: Communication
    org_name: str
    org_abn: str

class DonorOrganisation(BaseModel):
    """
    A data item representing an aid donor

    Args:
        donor_org_id (int): organisation id for the database
        org_name (str): name of the organisation
        contact_person (str): name of the contact person
        contact_email (str): how to contact the main contact
        address (str): physical mailing address

    """
    donor_org_id: int
    org_name: str
    contact_person: str
    contact_email: str
    address: str = None
