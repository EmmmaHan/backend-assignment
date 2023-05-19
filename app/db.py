import os
import sqlalchemy as db
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy_utils import PasswordType
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship
# from errors import InvalidStateTransitonError
from state_model import UserCardDeactive, UserCardActive, UserCardState
from config import get_db_uri
import utils
import sys

engine = db.create_engine(get_db_uri())
connection = engine.connect()
metadata = MetaData()
Base = declarative_base()

class ExtendedBase:
    """Base class for repeating columns"""

    id = Column(Integer, primary_key = True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class User(ExtendedBase, Base):
    """User class"""

    __tablename__ = 'users'

    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    email = Column(String(length=100), unique=True, index=True, nullable=False)
    password = Column(PasswordType(schemes=[
                    'pbkdf2_sha512',
                    'md5_crypt'
                ],
                deprecated=['md5_crypt']),
                nullable=False)
    user_accounts = relationship('UserAccount', back_populates="user")

    def __init__(self, first_name, last_name, email, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"<User(id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}, email:{self.email}, updated_at:{self.updated_at}, created_at:{self.created_at})>"

class UserAccount(ExtendedBase, Base):
    """User account class"""

    __tablename__ = 'user_accounts'
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_number = Column(String(30), nullable=False)
    balance = Column(Integer, default=0, nullable=False) # Integer for KRW
    user = relationship('User', back_populates="user_accounts")

    def __init__(self, user_id, balance=0) -> None:
        self.user_id =user_id
        self.account_number = utils.generate_random_string(20)
        self.balance = balance

    def __repr__(self) -> str:
       return f"<UserAccount(id:{self.id}, user_id:{self.user_id}, account_number:{self.account_number}, balance:{self.balance}, updated_at:{self.updated_at}, created_at:{self.created_at})>"
    
class UserCard(ExtendedBase, Base):
    """Card class related to user and user_account"""

    __tablename__ = 'user_cards'
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_account_id = mapped_column(Integer, ForeignKey("user_accounts.id"), nullable=False, index=True)
    card_number = Column(String(12), nullable=False)
    cvc = Column(String(3), nullable=False)
    status = Column(String(20), nullable=False)
    activated_at = Column(DateTime(timezone=True), nullable=True)
    deactivated_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, user_id, user_account_id) -> None:
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.card_number = utils.generate_random_numbers(12)
        self.cvc = utils.generate_random_numbers(3)
        self.status = repr(UserCardDeactive(self))
    
    def transition_to(self, state: UserCardState):
        print(f'{self}')
        self.status = repr(state(self))

    def get_state(self):
        """ Temporary fix for trying saving status as string in db"""

        state = ''
        match self.status:
            case 'active':
                state =  UserCardActive
            case 'deactive':
                state = UserCardDeactive
            case '':
                raise InvalidStateTransitonError("invalid state")
        return state
            
        
    def __repr__(self) -> str:
        return f"<UserCard(id:{self.id}, user_id:{self.user_id}, user_account_id:{self.user_account_id}, card_number:{self.card_number}, status:{self.status}, activated_at:{self.activated_at}, deactivated_at:{self.deactivated_at}, created_at:{self.created_at}, updated_at:{self.updated_at})>"

def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()


def InvalidStateTransitonError(Exception):
    pass