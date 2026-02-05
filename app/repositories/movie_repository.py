from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Movie, Genre


class MovieRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Movie]:
        stmt = select(Movie).options(selectinload(Movie.genres)).order_by(Movie.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get(self, movie_id: int) -> Optional[Movie]:
        stmt = select(Movie).options(selectinload(Movie.genres)).where(Movie.id == movie_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, movie: Movie, genre_ids: Optional[list[int]] = None) -> Movie:
        if genre_ids:
            genres = (await self.session.execute(select(Genre).where(Genre.id.in_(genre_ids)))).scalars().all()
            movie.genres = list(genres)
        self.session.add(movie)
        await self.session.flush()
        return movie

    async def update(self, db_movie: Movie, data: dict, genre_ids: Optional[list[int]] = None) -> Movie:
        for k, v in data.items():
            if hasattr(db_movie, k) and k != "id":
                setattr(db_movie, k, v)
        if genre_ids is not None:
            genres = (await self.session.execute(select(Genre).where(Genre.id.in_(genre_ids)))).scalars().all()
            db_movie.genres = list(genres)
        await self.session.flush()
        return db_movie

    async def delete(self, movie: Movie) -> None:
        await self.session.delete(movie)
        await self.session.flush()
