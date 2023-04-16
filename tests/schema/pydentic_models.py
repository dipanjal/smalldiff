from pydantic import BaseModel, PositiveInt


class AddressModel(BaseModel):
    street: str
    dist: str
    zip: PositiveInt


class PersonModel(BaseModel):
    name: str
    age: PositiveInt
    address: AddressModel
