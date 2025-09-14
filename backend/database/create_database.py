from backend.database.db_config import engine, Base
from backend import models  # type: ignore

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")
