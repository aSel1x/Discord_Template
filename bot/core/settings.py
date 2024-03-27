from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.dev', '.env')
    )

    DISCORD_BOT_PREFIX: str = Field(default='')
    DISCORD_BOT_TOKEN: str = Field(min_length=1)

    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_PASSWORD: str = Field(default='postgres')
    POSTGRES_HOST: str = Field(default='postgres')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default='postgres')

    @field_validator('POSTGRES_HOST', mode='before')
    @classmethod
    def validate_postgres_host(cls, v: str):
        return 'postgres' if v == '' else v

    @property
    def pg_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
