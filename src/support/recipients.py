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
    id: str = None


class Person(PersonID):
    """
    A data structure representing basic information about a person

    Args:
        first_name (str): Person's first name.
        last_name (str): Person's last name. Defaults to "NO_LAST_NAME"
        age (float): Age in years.
    """
    first_name: str
    last_name: str = NO_LAST_NAME
    age: float


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
    address: str = None #NO_KNOWN_ADDRESS
    common_law_partner: str = None
    dependents: str = None
