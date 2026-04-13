import sys
from loguru import logger
from pydantic import BaseModel
from wclickhouse import WClickHouse

# Configure Loguru
logger.remove()
logger.add(sys.stderr, format="<green>{time}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")

class LoggedUser(BaseModel):
    id: int
    name: str

def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    logger.info("Initializing WClickHouse with loguru tracing...")
    
    try:
        db = WClickHouse(LoggedUser, db_config)
        logger.info("Connection established and schema synced.")
        
        user = LoggedUser(id=1, name="Logged Alice")
        logger.debug(f"Attempting to insert user: {user.id}")
        db.insert(user)
        
        count = db.count()
        logger.info(f"Current total users: {count}")
        
    except Exception as e:
        logger.error(f"Database operation failed: {e}")

if __name__ == "__main__":
    main()
