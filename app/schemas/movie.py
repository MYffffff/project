from typing import Optional, List
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    year: Optional[int] = None
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None


class MovieCreate(MovieBase):
    title: str


class MovieUpdate(MovieBase):
    pass


class MoviePartialUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    year: Optional[int] = None
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None


class MovieRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    year: Optional[int]
    director_id: Optional[int]
    genres: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True
