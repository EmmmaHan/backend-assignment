from typing import List
from app.errors import ObjectNotFoundError
from app.orm import *
from app.db import User, UserAccount, UserCard

def create_user(first_name, last_name, email, password) -> int:
    return create_object(User(first_name, last_name, email, password))

def register_cards(cards: List[UserCard]):
    try: 
        create_objects(cards)
    except IntegrityError:
        print("Bulk insert for cards failed due to invalid entry values.")

def activate_card(card_id):
    try:
        card = get_object_by_id(card_id, UserCard)
        update_card_status(card,'active')
    except NoResultFound:
        ObjectNotFoundError(f"UserCard cannot be found with card_id: {card_id}")

def deactivate_card(card_id):
    try:
        card = get_object_by_id(card_id, UserCard)
        update_card_status(card, 'deactive')
    except NoResultFound:
        ObjectNotFoundError(f"UserCard cannot be found with card_id: {card_id}")

def check_balance(user_account_id) -> int:
    try:
        account = get_object_by_id(user_account_id, UserAccount)
        return account.balance
    except NoResultFound:
        raise ObjectNotFoundError(f"UserAccount cannot be found by user_account_id: {user_account_id}")

def create_account(user_id, amount=0) -> int:
    return create_object(UserAccount(user_id, amount))
    
def withdraw_cash(user_account_id, amount):
    account = get_object_by_id(user_account_id, UserAccount)
    if amount <= 0:
        raise ValueError("Withdraw amount should be greater than 0.")
    if account.balance - amount < 0:
        raise ValueError("You cannot withdraw below 0 balance.")
    
    update_account_balance(user_account_id, amount)

def deposit_cash(user_account_id, amount):
    if amount <= 0:
        raise ValueError("Deposit amount should be greater than 0.")
    
    account = get_object_by_id(user_account_id, UserAccount)
    update_account_balance(user_account_id, account.balance + amount)
