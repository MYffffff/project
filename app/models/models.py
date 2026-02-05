from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base

# Association tables
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

series_genre = Table(
    "series_genre",
    Base.metadata,
    Column("series_id", ForeignKey("series.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")
    series = relationship("Series", secondary=series_genre, back_populates="genres")


class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    movies = relationship("Movie", back_populates="director", cascade="all,delete")
    series = relationship("Series", back_populates="director", cascade="all,delete")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    director_id: Mapped[int | None] = mapped_column(ForeignKey("directors.id", ondelete="SET NULL"))
    director = relationship("Director", back_populates="movies")

    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    seasons: Mapped[int | None] = mapped_column(Integer, nullable=True)

    director_id: Mapped[int | None] = mapped_column(ForeignKey("directors.id", ondelete="SET NULL"))
    director = relationship("Director", back_populates="series")

    genres = relationship("Genre", secondary=series_genre, back_populates="series")
