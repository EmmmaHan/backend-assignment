import pytest
from app.db import User, UserAccount, UserCard
from app.services import *

# Run 'poetry run python app/db.py test for db initialization

def user_factory() -> int:
    """
    Helper function to create user
    """
    user = User(first_name="Emma", last_name="Han", email="emma@gmail.com", password="emmahan")
    return create_user(user)

def account_factory(user_id, balance) -> int:
    """
    Helper function to create account
    """
    user_account = UserAccount(user_id=user_id, balance=balance)
    return user_account

def card_factory(user_id, user_account_id):
    """
    Helper function to register card to a user
    """
    


@pytest.mark.asyncio
async def test_create_account():
    """
    Test Account Creating Logic
    """

    #GIVEN
        
    #WHEN
    _user_id = user_factory()
    _balance = 0
    user_account_id = create_object(account_factory(_balance))
    user_account = get_object_by_id(user_account_id, UserAccount)
    #THEN

    assert user_account.user_id == _user_id
    assert user_account.balance == _balance #default

@pytest.mark.asyncio
async def test_register_cards():

    #GIVEN
    _account = account_factory()

    #WHEN
        # Card Registration Logic
    #THEN
        # Assertion


@pytest.mark.asyncio
async def test_disable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Disabling Logic
    #THEN
        #Assertion

@pytest.mark.asyncio
async def test_enable_card():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Card Enabling Logic
            
    #THEN
        #Assertion
            


@pytest.mark.asyncio
async def test_deposit_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Saving Logic

    #THEN

@pytest.mark.asyncio
async def test_withdraw_cash():
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Money Withdrawing Logic

    #THEN



@pytest.mark.asyncio
async def test_check_account_balance():
    ...
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Balace checking Logic
            
    #THEN
        #Assertion

### Custom cases

@pytest.mark.asyncio
async def test_depost_invalid_amount():
    # amount <= 0
    ...
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Balace checking Logic
            
    #THEN
        #Assertion

@pytest.mark.asyncio
async def test_withdraw_below_balance():
    ...
    #GIVEN
    _account = account_factory()
    _card = card_factory(account_id=...)

    #WHEN
        # Balace checking Logic
            
    #THEN
        #Assertion