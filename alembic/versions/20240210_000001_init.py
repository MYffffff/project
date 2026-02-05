"""init schema

Revision ID: 20240210_000001
Revises: 
Create Date: 2024-02-10 00:00:01.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240210_000001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'genres',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index(op.f('ix_genres_id'), 'genres', ['id'], unique=False)

    op.create_table(
        'directors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_index(op.f('ix_directors_id'), 'directors', ['id'], unique=False)

    op.create_table(
        'movies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('director_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movies_id'), 'movies', ['id'], unique=False)

    op.create_table(
        'series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('seasons', sa.Integer(), nullable=True),
        sa.Column('director_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_series_id'), 'series', ['id'], unique=False)

    op.create_table(
        'movie_genre',
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('genre_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('movie_id', 'genre_id')
    )

    op.create_table(
        'series_genre',
        sa.Column('series_id', sa.Integer(), nullable=False),
        sa.Column('genre_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('series_id', 'genre_id')
    )


def downgrade() -> None:
    op.drop_table('series_genre')
    op.drop_table('movie_genre')
    op.drop_index(op.f('ix_series_id'), table_name='series')
    op.drop_table('series')
    op.drop_index(op.f('ix_movies_id'), table_name='movies')
    op.drop_table('movies')
    op.drop_index(op.f('ix_directors_id'), table_name='directors')
    op.drop_table('directors')
    op.drop_index(op.f('ix_genres_id'), table_name='genres')
    op.drop_table('genres')
