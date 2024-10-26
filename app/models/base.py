import datetime as dt
import uuid
from functools import partial

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from . import types

datetime_utcnow = partial(dt.datetime.now, tz=dt.UTC)


class IDModel(SQLModel):
    id: int | None = Field(
        default=None,
        primary_key=True,
        nullable=False,
        index=True,
    )

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)


class UUIDModel(SQLModel):
    external_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, unique=True, nullable=False
    )


class TimestampModel(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    created_at: dt.datetime | int | str = Field(
        default_factory=datetime_utcnow,
        sa_type=types.Unixepoch,
        nullable=False,
    )
    updated_at: dt.datetime | int | str | None = Field(
        default=None,
        sa_type=types.Unixepoch,
        nullable=True,
        sa_column_kwargs={"onupdate": datetime_utcnow},
    )