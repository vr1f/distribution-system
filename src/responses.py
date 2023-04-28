# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures and methods for API responses
#
# =========================================================================
from pydantic import BaseModel

class DatabaseActionResponse(BaseModel):
    """
    A data structure representing a standard response for a database
    type request.

    Args:
        id (str): The id key of the database item being added/updated.
        error (str): An error message if relevant.
    """
    id: str = None
    error: str = None