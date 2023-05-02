from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class Gender(str, Enum):
    M = "Male"
    F = "Female"


class AddressModel(BaseModel):
    street: str
    dist: str
    zip: PositiveInt


class LocationModel(BaseModel):
    long: float
    lat: float


class PersonModel(BaseModel):
    name: str
    age: PositiveInt
    address: AddressModel
    gender: Gender
    locations: Optional[List[LocationModel]] = None
    mobile_numbers: Optional[List[str]] = None
