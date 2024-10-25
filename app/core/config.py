from os import environ as env

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn


class AppConfig(BaseModel):
    name: str = Field('Template', alias='APP_TITLE')
    secret: str = Field('123abc', alias='APP_SECRET_KEY')
    version: str = Field('1.0.0', alias='APP_VERSION')


class DiscordConfig(BaseModel):
    name: str = Field('Template', alias='DISCORD_BOT_TITLE')
    token: str = Field(alias='DISCORD_BOT_TOKEN')
    prefix: str = Field('!', alias='DISCORD_BOT_PREFIX')


class PostgresConfig(BaseModel):
    user: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    host: str = Field('localhost', alias='POSTGRES_HOST')
    port: int = Field(5432, alias='POSTGRES_PORT')
    database: str = Field(alias='POSTGRES_DB')

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.database,
        )


class RedisConfig(BaseModel):
    user: str = Field(alias='REDIS_USERNAME')
    password: str = Field(alias='REDIS_PASSWORD')
    ssl: bool = Field(False, alias='REDIS_SSL')
    host: str = Field('localhost', alias='REDIS_HOST')
    port: int = Field(6379, alias='REDIS_PORT')
    path: int | None = Field(0, alias='REDIS_DB')

    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme='rediss' if self.ssl else 'redis',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=f"/{self.path}"
        )


class Config:
    app = AppConfig(**env)
    discord = DiscordConfig(**env)
    postgres = PostgresConfig(**env)
    redis = RedisConfig(**env)
