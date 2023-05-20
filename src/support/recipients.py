# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures and methods for aid recipients
#
# =========================================================================
from pydantic import BaseModel
from typing import List

NO_KNOWN_ADDRESS = "NO_KNOWN_ADDRESS"
NO_LAST_NAME = "NO_LAST_NAME"

class PersonID(BaseModel):
    """
    A base person data unit consisting of the unique identifier

    Args:
        id (str): Unique record key in the database or other unique identifier.
    """
    person_id: int = None


class Person(PersonID):
    """
    A data structure representing basic information about a person

    Args:
        first_name (str): Person's first name.
        last_name (str): Person's last name. Defaults to "NO_LAST_NAME"
        age (float): Age in years.
        nationality: Person's nationality
        id_no: Personal ID
        id_expiry: Expiry date of personal ID
        document_id: FK link to sensitive_img table which stores up to three img files
    """
    first_name: str
    last_name: str = NO_LAST_NAME
    age: int
    nationality: str = None
    id_no: str = None
    id_expiry: str = None
    document_id: str = None # Can FK be None?

class AidRecipient(Person):
    """
    A data structure representing basic recipient information.
    It can be used for both `request` and `response`.

    Args:
        address (str): Recipient's last known address.
            Defaults to NO_KNOWN_ADDRESS.
        common_law_partner (Person): Recipient's partner.
        dependents (List of Person): Recipient's dependents (eg. kids).
    """
    address: str = NO_KNOWN_ADDRESS
    n_family: int = None
    common_law_partner: str = None
    dependents: str = None
