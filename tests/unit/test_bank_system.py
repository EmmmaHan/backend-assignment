import pytest
from app.db import User, UserAccount, UserCard
from app.services import *
from app.errors import *
from app.utils import generate_random_string

# Run 'poetry run python app/db.py test for db initialization

def user_factory() -> int:
    """
    Helper function to create user
    """
    user = User(first_name="Emma", last_name="Han", email=generate_random_string(10)+"gmail.com", password="emmahan")
    return create_object(user)

def account_factory(user_id, balance) -> int:
    """
    Helper function to create account
    """
    user_account = UserAccount(user_id=user_id, balance=balance)
    account_id = create_object(user_account)
    return account_id

def card_factory(user_id, user_account_id):
    """
    Helper function to register card to a user
    """

    card = UserCard(user_id=user_id, user_account_id=user_account_id)
    card_id = create_object(card)
    return card_id


@pytest.mark.asyncio
async def test_create_account_service():
    """
    Test Account Creating Logic
    """

    #GIVEN
    _user_id = user_factory()
    _balance = 0
    #WHEN
    user_account_id = account_factory(_user_id, _balance)
    user_account = get_object_by_id(user_account_id, UserAccount)
    #THEN
    assert user_account.user_id == _user_id
    assert user_account.balance == _balance #default

@pytest.mark.asyncio
async def test_register_cards_service():
    #GIVEN
    user_id1 = user_factory()
    user1 = get_object_by_id(user_id1, User)
    user_account_id1 = account_factory(user_id1, 10)
    card1 = UserCard(user_id=user_id1, user_account_id=user_account_id1)
    assert len(user1.cards) == 0

    user_id2 = user_factory()
    user_account_id2 = account_factory(user_id2, 10)
    card2 = UserCard(user_id=user_id2, user_account_id=user_account_id2)
    assert len(user1.cards) == 0

    #WHEN
    register_cards([card1, card2])
    #THEN
    user1 = get_object_by_id(user_id1, User)
    assert len(user1.cards) == 1
    user2 = get_object_by_id(user_id2, User)
    assert len(user2.cards) == 1


@pytest.mark.asyncio
async def test_disable_card():
    #GIVEN
    user_id1 = user_factory()
    user_account_id1 = account_factory(user_id1, 10)
    card1_id = card_factory(user_id1, user_account_id1)
    card1 = get_object_by_id(card1_id, UserCard)
    assert card1.status == 'deactive'
    #WHEN
    activate_card(card1_id)
    #THEN
    card1 = get_object_by_id(card1_id, UserCard)
    assert card1.status == 'active'

@pytest.mark.asyncio
async def test_enable_card():
    #GIVEN
    user_id1 = user_factory()
    user_account_id1 = account_factory(user_id1, 10)
    card1_id = card_factory(user_id1, user_account_id1)
    card1 = get_object_by_id(card1_id, UserCard)
    assert card1.status == 'deactive'
    #WHEN
    activate_card(card1_id)
    deactivate_card(card1_id)
    #THEN
    card1 = get_object_by_id(card1_id, UserCard)
    assert card1.status == 'deactive'



@pytest.mark.asyncio
async def test_deposit_cash():
    #GIVEN
    _user_id = user_factory()
    _balance = 0
    _user_account_id = account_factory(_user_id, _balance)
    #WHEN
    deposit_cash(_user_account_id, 100)
    #THEN
    account = get_object_by_id(_user_account_id, UserAccount)
    assert account.balance == 100

@pytest.mark.asyncio
async def test_withdraw_cash():
    #GIVEN
    _user_id = user_factory()
    _balance = 100
    _user_account_id = account_factory(_user_id, _balance)
    #WHEN
    withdraw_cash(_user_account_id, 50)
    #THEN
    account = get_object_by_id(_user_account_id, UserAccount)
    assert account.balance == 50


@pytest.mark.asyncio
async def test_check_account_balance():
    #GIVEN
    _user_id = user_factory()
    _balance = 100
    #WHEN   
    _user_account_id = create_account(_user_id, _balance)
    #THEN
    assert check_balance(_user_account_id) == _balance

### Custom cases

@pytest.mark.asyncio
async def test_depost_invalid_amount():
    #GIVEN
    _user_id = user_factory()
    _balance = 0
    _user_account_id = account_factory(_user_id, _balance)
    #WHEN
    with pytest.raises(ValueError):
        deposit_cash(_user_account_id, -1)


@pytest.mark.asyncio
async def test_withdraw_below_balance():
    #GIVEN
    _user_id = user_factory()
    _balance = 100
    _user_account_id = account_factory(_user_id, _balance)
    #WHEN
    with pytest.raises(ValueError):
        withdraw_cash(_user_account_id, 200)
