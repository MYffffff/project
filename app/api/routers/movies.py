from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.models.models import Movie
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieUpdate, MoviePartialUpdate, MovieRead

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=List[MovieRead])
async def get_movies(session: AsyncSession = Depends(get_session)):
    repo = MovieRepository(session)
    movies = await repo.list()
    # map genres to list of ids for read schema
    result = []
    for m in movies:
        result.append(
            MovieRead(
                id=m.id,
                title=m.title,
                description=m.description,
                year=m.year,
                director_id=m.director_id,
                genres=[g.id for g in m.genres],
            )
        )
    return result


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(
    movie_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    repo = MovieRepository(session)
    movie = await repo.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieRead(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        year=movie.year,
        director_id=movie.director_id,
        genres=[g.id for g in movie.genres],
    )


@router.post("/", response_model=MovieRead, status_code=201)
async def create_movie(
    payload: MovieCreate = Body(...),
    session: AsyncSession = Depends(get_session),
):
    repo = MovieRepository(session)
    movie = Movie(
        title=payload.title,
        description=payload.description,
        year=payload.year,
        director_id=payload.director_id,
    )
    created = await repo.create(movie, genre_ids=payload.genre_ids)
    return MovieRead(
        id=created.id,
        title=created.title,
        description=created.description,
        year=created.year,
        director_id=created.director_id,
        genres=[g.id for g in created.genres],
    )


@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    session: AsyncSession = Depends(get_session),
):
    repo = MovieRepository(session)
    movie = await repo.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated = await repo.update(
        movie,
        data={
            "title": payload.title,
            "description": payload.description,
            "year": payload.year,
            "director_id": payload.director_id,
        },
        genre_ids=payload.genre_ids,
    )
    return MovieRead(
        id=updated.id,
        title=updated.title,
        description=updated.description,
        year=updated.year,
        director_id=updated.director_id,
        genres=[g.id for g in updated.genres],
    )


@router.patch("/{movie_id}", response_model=MovieRead)
async def partial_update_movie(
    movie_id: int,
    payload: MoviePartialUpdate,
    session: AsyncSession = Depends(get_session),
):
    repo = MovieRepository(session)
    movie = await repo.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    data = payload.model_dump(exclude_unset=True)
    genre_ids = data.pop("genre_ids", None)
    updated = await repo.update(movie, data=data, genre_ids=genre_ids)
    return MovieRead(
        id=updated.id,
        title=updated.title,
        description=updated.description,
        year=updated.year,
        director_id=updated.director_id,
        genres=[g.id for g in updated.genres],
    )


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: int, session: AsyncSession = Depends(get_session)):
    repo = MovieRepository(session)
    movie = await repo.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await repo.delete(movie)
    return None
