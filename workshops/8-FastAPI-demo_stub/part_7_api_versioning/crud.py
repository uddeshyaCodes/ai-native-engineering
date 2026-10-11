from sqlalchemy import select
from sqlalchemy.orm import Session
from models import AccountDB, UserDB
from schemas import User, UserUpdate, Account, AccountUpdate

# USER CRUD OPERATIONS

# Function to create a new user in the database
def create_user(db: Session, user: User):
    db_user = UserDB(username=user.username, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to retrieve user by username from the database
def get_user_by_username(db: Session, username: str):
    return db.scalar(select(UserDB).where(UserDB.username == username))

# Function to retrieve all users from the database
def get_all_users(db: Session):
    return db.scalars(select(UserDB)).all()

# Function to update user details in the database
def update_user(db: Session, username: str, user_update: UserUpdate):
    user = get_user_by_username(db, username)

    if not user:
        return None

    data = user_update.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

# Function to delete a user from the database
def delete_user(db: Session, username: str):
    user = get_user_by_username(db, username)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user

# ACCOUNT CRUD OPERATIONS

# Function to add an account to a user in the database
def add_account_to_user(db: Session, username: str, account: Account):
    user = get_user_by_username(db, username)

    if not user:
        return None

    if len(user.accounts) > 5:
        raise ValueError("User can have a maximum of 5 accounts")

    db_account = AccountDB(account_number=account.account_number, account_type=account.account_type, balance=account.balance, user_id=user.id, is_active=account.is_active)

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account

# Function to retrieve account using account number from the database
def get_account_by_number_username(db: Session, username: str, account_number: str):
    user = get_user_by_username(db, username)

    if not user:
        return None

    return db.scalar(select(AccountDB).where(AccountDB.account_number == account_number, AccountDB.user_id == user.id))

# Get active accounts for a user
def get_active_accounts(db: Session, username: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    
    return [account for account in user.accounts if account.is_active]

# Get inactive accounts for a user
def get_inactive_accounts(db: Session, username: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    
    return [account for account in user.accounts if not account.is_active]

# Get total balance of all accounts for a user
def get_total_balance(db: Session, username: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    
    return sum(account.balance for account in user.accounts)

# Get the accounts for a particular user by username
def get_accounts_by_username(db: Session, username: str):
    user = get_user_by_username(db, username)

    if not user:
        return None
    
    return user.accounts

# Function to delete an account from a user in the database
def delete_account(db: Session, username: str, account_number: str):
    account = get_account_by_number_username(db, username, account_number)

    if not account:
        return None

    db.delete(account)
    db.commit()

    return account

# Function to update account details in the database
def update_account(db: Session, username: str, account_number: str, account_update: AccountUpdate):
    account = get_account_by_number_username(db, username, account_number)

    if not account:
        return None

    data = account_update.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)

    return account