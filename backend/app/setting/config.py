import os

class Settings:
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET", "default_access_token_secret")
    refresh_token_secret: str = os.getenv("REFRESH_TOKEN_SECRET", "default_refresh_token_secret")