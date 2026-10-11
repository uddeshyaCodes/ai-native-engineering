from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Account, AccountUpdate
from crud import add_account_to_user, get_account_by_number_username, get_active_accounts, get_inactive_accounts, get_total_balance, get_accounts_by_username, delete_account, update_account

router = APIRouter(
    prefix = "/users/{username}/accounts",
    tags = ["Accounts"]
)

# Endpoint to get all accounts for a user by username
@router.get("/")
def get_accounts_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    # TODO: Implement the logic to retrieve all accounts for a user by username from the database and return them as a list of Account models
    user = get_user_by_username(db, username)
    if not user:
        return None

    if len(user.accounts) > 5:
        raise ValueError("User cannot have more than 5 accounts")

    db_account = AccountDB(account_number=account.account_number, account_type=account.account_type, balance=account.balance, is_active=account.is_active)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Endpoint to add a new account for a user by username
@router.post("/")
def add_account_endpoint(account: Account, db: Session = Depends(get_db)):
    # TODO: Implement the logic to add a new account for a user by username in the database using the Account model for validation and serialization
    user = get_user_by_username(db, username)
    if not user:
        return None

    if len(user.accounts) >= 5:
        raise ValueError("User cannot have more than 5 accounts")

# Endpoint to get the active accounts for a user by username
@router.get("/active")
def get_active_accounts_route():
    # TODO: Implement the logic to retrieve all active accounts for a user by username from the database and return them as a list of Account models
    ...

# Endpoint to get the inactive accounts for a user by username
@router.get("/inactive")
def get_inactive_accounts_route():
    # TODO: Implement the logic to retrieve all inactive accounts for a user by username from the database and return them as a list of Account models
    ...

# Endpoint to get the total balance of all accounts for a user by username
@router.get("/total_balance")
def get_total_balance_route():
    # TODO: Implement the logic to calculate the total balance of all accounts for a user by username from the database and return it as a numeric value
    ...

# Endpoint to get a specific account for a user by username and account number
@router.get("/{account_number}")
def get_account_by_number_route():
    # TODO: Implement the logic to retrieve a specific account for a user by username and account number from the database and return it as an Account model
    ...

# Endpoint to update a specific account for a user by username and account number
@router.put("/{account_number}")
def update_account_route():
    # TODO: Implement the logic to update a specific account for a user by username and account number in the database using the AccountUpdate model for validation and serialization
    ...

# Endpoint to delete a specific account for a user by username and account number
@router.delete("/{account_number}")
def delete_account_route():
    # TODO: Implement the logic to delete a specific account for a user by username and account number from the database
    ...


