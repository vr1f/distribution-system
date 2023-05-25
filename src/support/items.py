# =========================================================================
#
# VR1FAMILY CHARITY DISTRIBUTION IT SYSTEM
#
# Data structures for items, categories and kits
#
# =========================================================================

from pydantic import BaseModel
from datetime import date
import enum

class StatusEnum(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

#! Not used, causes problems for an optional field
class Size(str, enum.Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    XLarge = 'XL'

#! Not used, removed gender from item column
class Gender(str, enum.Enum):
    FEMALE = 'female'
    MALE = 'male'
    UNISEX = 'unisex'
    OTHER = 'other'

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
    item_brand: str
    expiry_date: str
    ingredients : str
    allergen_info: str
    size: str
    category_id: int
    from_donor: int = None

class FoodItem(Item):
    """
    Class specifically for food items - inherits Item class

    Args:
        expiry_date: date - date of food expiration
        ingredients : str - main ingredients
        allergen_info: str - allergey information
    """
    expiry_date: date
    ingredients : str
    allergen_info: str

class ClothingItem(Item):
    """
    Class specifically for clothing items - inherits Item

    Args:
        Size (Size) -  size of the clothing item
    """
    gender: Gender
    size: Size

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


class AidKit(BaseModel):
    """
    Defines an aid kit
    """
    aid_kit_id: int = None
    aidkit_name: str
    aidkit_description: str


class AidKitItem(BaseModel):
    """
    Defines an item belonging to a kit
    """
    id: int = None
    aid_kit_id: int
    item_id: int
    quantity: int
