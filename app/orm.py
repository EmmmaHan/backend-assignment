from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db import engine, UserCard, UserAccount
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import List

def create_object(object: object) -> int:
    try:
        with Session(engine) as session:
            session.add(object)
            session.commit()
            session.refresh(object)
            return object.id
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
    except NoResultFound as e:
        raise e
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e

def update_card_status(card: UserCard) -> None:
    try:
        with Session(engine) as session:
            card
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


