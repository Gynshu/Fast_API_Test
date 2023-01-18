from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    EMAIL_VERIFICATION_KEY: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    CLIENT_ORIGIN: str

    # all in one env db and jwt
    class Config:
        env_file = '.env'


settings = Settings()
