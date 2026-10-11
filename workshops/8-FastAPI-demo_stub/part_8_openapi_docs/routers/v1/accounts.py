from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Account, AccountUpdate
from crud import add_account_to_user, get_account_by_number_username, get_active_accounts, get_inactive_accounts, get_total_balance, get_accounts_by_username, delete_account, update_account

router = APIRouter(
    prefix = "/api/v1/users/{username}/accounts",
    tags = ["Accounts"]
)

# Endpoint to get all accounts for a user by username
@router.get("/", response_model=list[Account])
def get_accounts_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    accounts = get_accounts_by_username(db, username)
    if accounts:
        return accounts
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to add a new account for a user by username
@router.post("/", response_model=Account)
def add_account_endpoint(username: str, account: Account, db: Session = Depends(get_db)):
    try:
        db_account = add_account_to_user(db, username, account)
        if db_account is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Error adding account: " + str(e))

# Endpoint to get the active accounts for a user by username
@router.get("/active", response_model=list[Account])
def get_active_accounts_route(username: str, db: Session = Depends(get_db)):
    accounts = get_active_accounts(db, username)
    if accounts is None:
        raise HTTPException(status_code=404, detail="User not found")
    return accounts

# Endpoint to get the inactive accounts for a user by username
@router.get("/inactive", response_model=list[Account])
def get_inactive_accounts_route(username: str, db: Session = Depends(get_db)):
    accounts = get_inactive_accounts(db, username)
    if accounts is None:
        raise HTTPException(status_code=404, detail="User not found")
    return accounts

# Endpoint to get the total balance of all accounts for a user by username
@router.get("/total_balance", response_model=dict)
def get_total_balance_route(username: str, db: Session = Depends(get_db)):
    total_balance = get_total_balance(db, username)
    if total_balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"total_balance": total_balance}

# Endpoint to get a specific account for a user by username and account number
@router.get("/{account_number}", response_model=Account)
def get_account_by_number_route(username: str, account_number: str, db: Session = Depends(get_db)):
    account = get_account_by_number_username(db, username, account_number)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Endpoint to update a specific account for a user by username and account number
@router.put("/{account_number}", response_model=Account)
def update_account_route(username: str, account_number: str, account_update: AccountUpdate, db: Session = Depends(get_db)):
    updated_account = update_account(db, username, account_number, account_update)
    if updated_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account

# Endpoint to delete a specific account for a user by username and account number
@router.delete("/{account_number}", response_model=Account)
def delete_account_route(username: str, account_number: str, db: Session = Depends(get_db)):
    deleted_account = delete_account(db, username, account_number)
    if deleted_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return deleted_account


