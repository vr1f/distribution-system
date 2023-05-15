# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures for items, categories and kits
#
# =========================================================================

from pydantic import BaseModel
import enum

class StatusEnum(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class Item(BaseModel):
    """
    A base item data unit representing any item

    Args:
        item_id (int): id of the item
        item_name (str) : name of the item
        item_quantity (int): current stock level of the item

    """
    item_id: int = None
    item_name: str
    item_quantity: int

class Category(BaseModel):
    """
    A category data unit that defines a category

    Args:
        category_id (int): category id for DB
        category_name (str): name of the category
        status (enum): it's current stock level status

    """
    category_id: int = None
    category_name: str
    status: StatusEnum