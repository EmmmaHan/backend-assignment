import sqlalchemy as db
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy_utils import PasswordType
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column
from config import get_db_uri
import utils

engine = db.create_engine(get_db_uri())
connection = engine.connect()
metadata = MetaData()
Base = declarative_base()

class ExtendedBase:
    id = Column(Integer, primary_key = True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class User(ExtendedBase, Base):
    """User Account"""

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
    
    def __repr__(self) -> str:
        return f"<User(id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}, email:{self.email}, updated_at:{self.updated_at}, created_at:{self.created_at})>"

class UserAccount(ExtendedBase, Base):
    """Accounts owned by user"""

    __tablename__ = 'user_accounts'
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_number = Column(String(30), nullable=False, default=utils.generate_random_string(20))
    amount = Column(Integer, default=0, nullable=False) # Integer for KRW

    def __repr__(self) -> str:
       return f"<UserAccount(id:{self.id}, user_id:{self.user_id}, account_number:{self.account_number}, amount:{self.amount}, updated_at:{self.updated_at}, created_at:{self.created_at})>"
    
class UserCard(ExtendedBase, Base):
    """Cards"""

    __tablename__ = 'user_cards'
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_account_id = mapped_column(Integer, ForeignKey("user_accounts.id"), nullable=False, index=True)
    card_number = Column(String(12), nullable=False, default=utils.generate_random_numbers(12))
    cvc = Column(String(3), nullable=False, default=utils.generate_random_numbers(3))
    status = Column(String(20), nullable=False)
    activated_at = Column(DateTime(timezone=True), nullable=True)
    deactivated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<UserCard(id:{self.id}, user_id:{self.user_id}, user_account_id:{self.user_account_id}, card_number:{self.card_number}, status:{self.status}, expire_at:{self.expire_at}, activated_at:{self.activated_at}, deactivated_at:{self.deactivated_at}, created_at:{self.created_at}, updated_at:{self.updated_at})>"

def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()