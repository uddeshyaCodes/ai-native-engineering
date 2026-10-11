from pydantic import BaseModel, EmailStr, Field, field_validator

class Account(BaseModel):
    # TODO: Define the fields for the Account model
    account_number: str = Field(..., min_length=10, max_length=12, description="Account number must be between 10 and 12 characters")
    account_type: str = Field(..., pattern=r"^(savings|current)$", description="Account type must be either savings or current")
    balance: float = Field(..., description="Balance must be a positive number", ge=0.0)
    # Use default=False OR ..., not both (... means "required")
    is_active: bool = Field(default=False, description="Account must be active")
    

class User(BaseModel):
    # TODO: Define the fields for the User model, including a list of Account objects
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(..., format="email")
    age: int = Field(..., description="Age must be between 0 and 100")
    accounts: list[Account] = Field(default_factory=list, description="User must have at least one account")
    @field_validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Age must be between 0 and 100")
        return v

class UserInput(BaseModel):
    # TODO: Define the fields for the UserInput model, which will be used for user creation input
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(..., format="email")
    age: int = Field(..., description="Age must be between 0 and 100")
