"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-03-27 16:20:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1"),
        sa.Column("category_default", sa.String(length=32), nullable=False),
        sa.Column("parser_config", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_sources_id"), "sources", ["id"], unique=False)

    op.create_table(
        "news_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("normalized_title", sa.String(length=512), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=True),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.Column("raw_score", sa.String(length=64), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("url"),
    )
    op.create_index(op.f("ix_news_items_id"), "news_items", ["id"], unique=False)

    op.create_table(
        "event_clusters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("canonical_title", sa.String(length=512), nullable=False),
        sa.Column("canonical_summary", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=True),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("first_seen_at", sa.DateTime(), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
        sa.Column("related_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_event_clusters_id"), "event_clusters", ["id"], unique=False)

    op.create_table(
        "cluster_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cluster_id", sa.Integer(), sa.ForeignKey("event_clusters.id"), nullable=False),
        sa.Column("news_item_id", sa.Integer(), sa.ForeignKey("news_items.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_cluster_items_id"), "cluster_items", ["id"], unique=False)

    op.create_table(
        "refresh_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trigger_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("stats_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_refresh_jobs_id"), "refresh_jobs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_refresh_jobs_id"), table_name="refresh_jobs")
    op.drop_table("refresh_jobs")
    op.drop_index(op.f("ix_cluster_items_id"), table_name="cluster_items")
    op.drop_table("cluster_items")
    op.drop_index(op.f("ix_event_clusters_id"), table_name="event_clusters")
    op.drop_table("event_clusters")
    op.drop_index(op.f("ix_news_items_id"), table_name="news_items")
    op.drop_table("news_items")
    op.drop_index(op.f("ix_sources_id"), table_name="sources")
    op.drop_table("sources")
