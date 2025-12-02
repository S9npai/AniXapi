from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_settings import settings

load_dotenv()

engine = create_engine(
    str(settings.db_url)
)

SessionLocal = sessionmaker(autoflush=False ,bind=engine)

def db_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
