from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

session = SessionLocal()