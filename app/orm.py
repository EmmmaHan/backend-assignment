from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db import engine, UserCard, UserAccount
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import List

def create_object(object: object) -> None:
    try:
        with Session(engine) as session:
            session.add(object)
            session.commit()
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e
    
def create_objects(objects: List[object]) -> None:
    try:
        with Session(engine) as session:
            session.bulk_save_objects(objects)
            session.commit()
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e


def get_object_by_id(id: int, klass: object) -> object:
    try:
        with Session(engine) as session:
            q=session.query(klass).filter(klass.id==id)
            obj = q.one()
            return obj
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e

def update_card_status(card_id: int, status: str) -> None:
    try:
        with Session(engine) as session:
            q = session.query(UserCard).filter(UserCard.id==card_id)
            card = q.one()
            card.status = status
            session.commit()
    except NoResultFound as e:
        raise e
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e
    
    
def update_account_balance(account_id: int, balance: int):
        try:
            with Session(engine) as session:
                q = session.query(UserAccount).filter(UserAccount.id == account_id)
                user_account = q.one()
                user_account.balance = balance
                session.commit()
        except NoResultFound as e:
            raise e
        except IntegrityError as e:
            raise e
        except SQLAlchemyError as e:
            raise e
        

        
# def check_user_password(user_id, password):
#     try:    
#         with Session(engine) as session:
#             q = session.query(User).filter(User.id==user_id)
#             user = q.one()
#             if not user.verify_password(password):
#                 raise NoResultFound
#             return True
#     except IntegrityError as e:
#         raise IndentationError
#     except SQLAlchemyError as e:
#         raise e


