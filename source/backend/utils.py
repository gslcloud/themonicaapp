import redis
from sqlalchemy.orm import Session
from typing import Optional


class RedisClient:
    def __init__(self, host: str, port: int):
        self.redis_client = redis.Redis(host=host, port=port)

    def create_cookie(self, name: str, value: str, ttl: Optional[int] = None) -> bool:
        """
        Create a cookie in Redis.

        Args:
            name (str): The name of the cookie.
            value (str): The value of the cookie.
            ttl (int, optional): The time-to-live (in seconds) for the cookie. Defaults to None.

        Returns:
            bool: True if the cookie is created successfully, False otherwise.
        """
        try:
            self.redis_client.set(name, value, ex=ttl)
            return True
        except Exception as e:
            raise ValueError(f"Error creating cookie: {str(e)}")

    def get_cookie(self, name: str) -> Optional[str]:
        """
        Get the value of a cookie from Redis.

        Args:
            name (str): The name of the cookie.

        Returns:
            Optional[str]: The value of the cookie or None if the cookie does not exist.
        """
        try:
            value = self.redis_client.get(name)
            return value.decode() if value else None
        except Exception as e:
            raise ValueError(f"Error getting cookie: {str(e)}")

    def delete_cookie(self, name: str) -> bool:
        """
        Delete a cookie from Redis.

        Args:
            name (str): The name of the cookie.

        Returns:
            bool: True if the cookie is deleted successfully, False otherwise.
        """
        try:
            self.redis_client.delete(name)
            return True
        except Exception as e:
            raise ValueError(f"Error deleting cookie: {str(e)}")

def get_db() -> Session:
    """
    Create a SQLAlchemy database session.

    Returns:
        Session: The SQLAlchemy database session.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()