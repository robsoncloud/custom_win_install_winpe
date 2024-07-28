from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError

from mdt import crud
from mdt.schemas import Computer, ComputerCreate, User, UserCreate, LockCreate
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from .models import Base

app = FastAPI(
    title="Deployment Manager Enginee"
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_root():
    return {"message": "Hello World"}


@app.get("/api/computers", tags=["Computers"], response_model=list[Computer])
async def get_computers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_computers(db, skip=skip, limit=limit)


@app.post("/api/computers", tags=["Computers"], response_model=Computer)
async def create_computer(computer: ComputerCreate, db: Session = Depends(get_db)):
    try:
        new_computer = crud.create_computer(db, computer)
        return new_computer
    except ValidationError as e:
        raise HTTPException(
            status_code=422, detail="Product is not valid - Exception: " + e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users", tags=["Users"], response_model=list[User])
async def get_users(skip: int=0, limit=100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.post("/api/users", tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = crud.create_user(db, user)
        return new_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="User is not valid - Exception: "+e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/locks", tags=["Locks"])
async def get_locks(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return crud.get_locks(db)

@app.post("/api/locks", tags=["Locks"])
async def create_lock(lock: LockCreate, db: Session = Depends(get_db)):
    try:
        new_lock = crud.create_lock(db, lock)
        return new_lock
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Lock is not valid - Exception: {0}".format(e.errors()))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error has occured - Exception: {0}".format(str(e)))
    
@app.put("/api/computers/{computer_id}/assign-user", response_model=Computer)
def assign_user_to_computer(
    computer_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    return crud.add_computer_to_user(db, computer_id, user_id)