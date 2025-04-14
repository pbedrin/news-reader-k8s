from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT


class News(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str = Field(index=True, unique=True)
    title: str | None = Field(default=None, sa_column=Column(TEXT))
    subtitle: str | None = Field(default=None, sa_column=Column(TEXT))
    publication_date: str | None = Field(default=None)
    text: str | None = Field(default=None, sa_column=Column(TEXT))
    author: str | None = Field(default=None)
    tags: str | None = Field(default=None)
    categories: str | None = Field(default=None)
    source: str | None = Field(default=None)
