# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures and methods for air donors
#
# =========================================================================
from pydantic import BaseModel

NO_KNOWN_ADDRESS = "NO_KNOWN_ADDRESS"
NO_LAST_NAME = "NO_LAST_NAME"


class AidDonor(BaseModel):

    """
    A data item representing an aid donor

    Args:
        donor_id (int): id for the database
        first_name (str): first name of the donor
        last_name (str): last name of the donor. Optional field
        mail_address (str): physical mailing address
        phone_number (str): mobile or landline
        email_address (str): email address
        preferred_comm (str): select either email or phone as the preferred mode of communication
    """
    donor_id: int
    first_name: str
    last_name: str = NO_LAST_NAME
    mail_address: str = NO_KNOWN_ADDRESS
    phone_number: str
    email_address: str
    preferred_comm: str

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
