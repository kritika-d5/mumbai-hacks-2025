"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create clusters table
    op.create_table(
        'clusters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('canonical_article_id', postgresql.UUID(as_uuid=True)),
        sa.Column('fact_summary', sa.Text()),
        sa.Column('frame_summary', postgresql.JSON()),
        sa.Column('facts', postgresql.JSON()),
    )
    
    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('url', sa.Text(), unique=True, nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('author', sa.String(255)),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('raw_html', sa.Text()),
        sa.Column('language', sa.String(10), default='en'),
        sa.Column('country', sa.String(10)),
        sa.Column('scraped_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('chunks', postgresql.JSON()),
        sa.Column('ner_entities', postgresql.JSON()),
        sa.Column('tone_score', sa.Float()),
        sa.Column('lexical_bias_score', sa.Float()),
        sa.Column('omission_score', sa.Float()),
        sa.Column('consistency_score', sa.Float()),
        sa.Column('bias_index', sa.Float()),
        sa.Column('cluster_id', postgresql.UUID(as_uuid=True)),
        sa.ForeignKeyConstraint(['cluster_id'], ['clusters.id']),
        sa.ForeignKeyConstraint(['canonical_article_id'], ['articles.id']),
    )
    
    op.create_index('ix_articles_source', 'articles', ['source'])
    op.create_index('ix_articles_published_at', 'articles', ['published_at'])
    op.create_index('ix_articles_cluster_id', 'articles', ['cluster_id'])
    
    # Create article_analyses table
    op.create_table(
        'article_analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('analysis_type', sa.String(50), nullable=False),
        sa.Column('result', postgresql.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
    )


def downgrade() -> None:
    op.drop_table('article_analyses')
    op.drop_table('articles')
    op.drop_table('clusters')

