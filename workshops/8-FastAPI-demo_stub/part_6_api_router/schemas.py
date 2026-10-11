from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Account(BaseModel):
    # Mandatory fields for the Account model with validation constraints
    account_number: str = Field(..., min_length=10, max_length=12, description="The account number of the user")
    account_type: str = Field(..., pattern=r"^(savings|current)$", description="The type of the account, either 'savings' or 'current'")
    balance: float = Field(..., description="The balance of the account", ge=0.0)
    is_active: bool = Field(description="Indicates whether the account is active or not", default=False)

class AccountUpdate(BaseModel):
    # TODO: Define the fields for the AccountUpdate model, which will be used for account update input
    ...

class User(BaseModel):
    # Mandatory fields for the User model with validation constraints
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    email: str = Field(..., pattern=r"^\S+@\S+\.\S+$", description="The email address of the user")
    age: int = Field(..., description="The age of the user", ge=0, le=120)
    # Addition of accounts field to the User model, which is a list of Account objects
    accounts: list[Account] = Field(default_factory=list, description="List of accounts associated with the user")
    # Validator to ensure that the age is at least 13 for user registration
    @field_validator("age")
    @classmethod
    def validate_age(cls, age):
        if age is not None and age < 13:
            raise ValueError("User must be at least 13 years old")
        return age

class UserInput(BaseModel):
    # Mandatory fields for the User model with validation constraints
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    email: str = Field(..., pattern=r"^\S+@\S+\.\S+$", description="The email address of the user")
    age: int = Field(..., description="The age of the user", ge=0, le=120)

class UserUpdate(BaseModel):
    email: Optional[str] = Field(default=None, pattern=r"^\S+@\S+\.\S+$", description="The email address of the user")
    age: Optional[int] = None
    @field_validator("age")
    @classmethod
    def validate_age(cls, age):
        if age is not None and age < 13:
            raise ValueError("User must be at least 13 years old")
        return age
