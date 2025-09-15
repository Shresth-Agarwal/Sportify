from sqlalchemy import text
from db_config import engine


def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)


if __name__ == "__main__":
    test_connection()
