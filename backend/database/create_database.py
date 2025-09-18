from backend.database.db_config import Base, engine
from backend.models import User, Auth, Exercise, ExerciseRecord

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

print("All tables dropped and recreated.")
