"""add-sto4-columns

Revision ID: 1e56b6212479
Revises: bb2f428feb9b
Create Date: 2023-07-26 10:40:22.591583

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "1e56b6212479"
down_revision = "bb2f428feb9b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("units", sa.Column("sto4_start_time", sa.DateTime(), nullable=True))
    op.add_column("units", sa.Column("sto4_endpoint", sa.String(length=255), nullable=True))
    op.add_column("units", sa.Column("sto4_name", sa.String(length=255), nullable=True))
    op.add_column("units", sa.Column("sto4_access", sa.String(length=255), nullable=True))
    op.add_column("units", sa.Column("sto4_secret", sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("units", "sto4_secret")
    op.drop_column("units", "sto4_access")
    op.drop_column("units", "sto4_name")
    op.drop_column("units", "sto4_endpoint")
    op.drop_column("units", "sto4_start_time")
    # ### end Alembic commands ###
