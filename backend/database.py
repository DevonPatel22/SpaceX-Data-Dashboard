from sqlmodel import SQLModel, create_engine, Session
from models import Launch, Rocket, Cores
from typing import Generator

database = "database.db"
engine = create_engine(f"sqlite:///{database}", echo=True)

def createTable():
    SQLModel.metadata.create_all(engine)

def getSession() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    print("Creating database and tables...")
    createTable()
    print(f"Database file created at : {database}")
