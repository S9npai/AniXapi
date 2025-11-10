import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))
SessionLocal = sessionmaker(autoflush=False ,bind=engine)

def db_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
