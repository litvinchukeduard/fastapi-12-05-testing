from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources, typically in module scope
POSTGRES_URL = "postgresql+psycopg2://postgres:example@localhost:5432/pyrecipe"
engine = create_engine(POSTGRES_URL)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

def get_postgres_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
