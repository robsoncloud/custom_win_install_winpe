from sqlalchemy.orm import Session
from .import models, schemas

def get_computers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Computer).offset(skip).limit(limit).all()

def create_computer(db: Session, computer: schemas.ComputerCreate):
    db_computer = models.Computer(**computer.model_dump())
    db.add(db_computer)
    db.commit()
    db.refresh(db_computer)
    return db_computer

def get_users(db: Session, skip: int=0, limit=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_locks(db: Session, skip: int=0, limit=100):
    return db.query(models.Lock).offset(skip).limit(limit).all()

def create_lock(db: Session, lock: schemas.LockCreate):
    db_lock = models.Lock(**lock.model_dump())
    db.add(db_lock)
    db.commit()
    db.refresh(db_lock)
    return db_lock

# def add_computer_to_user(db: Session, computer: schemas.ComputerCreate, user_id: str):
#     db_computer = models.Computer(**computer.model_dump(), user_id=user_id)
#     db.add(db_computer)
#     db.commit()
#     db.refresh(db_computer)
#     return db_computer

def add_computer_to_user(db: Session, computer_id: str, user_id: str):
# Verifique se o computador existe
    db_computer = db.query(models.Computer).filter(models.Computer.id == computer_id).first()
    if db_computer is None:
        raise Exception("Computer not found")
    
    # Verifique se o computador já tem um usuário associado
    if db_computer.user_id is not None:
        raise Exception("Computer already assigned to a user")
    
    # Verifique se o usuário existe
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise Exception("User not found")
    
    # Associe o usuário ao computador
    db_computer.user_id = user_id
    db.commit()
    db.refresh(db_computer)
    
    return db_computer