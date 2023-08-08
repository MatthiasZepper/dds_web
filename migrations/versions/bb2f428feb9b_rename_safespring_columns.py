"""rename-safespring-columns

Revision ID: bb2f428feb9b
Revises: 2cefec51b9bb
Create Date: 2023-07-26 07:11:20.429058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "bb2f428feb9b"
down_revision = "2cefec51b9bb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        table_name="units",
        column_name="safespring_endpoint",
        nullable=False,
        new_column_name="sto2_endpoint",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="safespring_name",
        nullable=False,
        new_column_name="sto2_name",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="safespring_access",
        nullable=False,
        new_column_name="sto2_access",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="safespring_secret",
        nullable=False,
        new_column_name="sto2_secret",
        type_=sa.String(length=255),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        table_name="units",
        column_name="sto2_endpoint",
        nullable=False,
        new_column_name="safespring_endpoint",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="sto2_name",
        nullable=False,
        new_column_name="safespring_name",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="sto2_access",
        nullable=False,
        new_column_name="safespring_access",
        type_=sa.String(length=255),
    )
    op.alter_column(
        table_name="units",
        column_name="sto2_secret",
        nullable=False,
        new_column_name="safespring_secret",
        type_=sa.String(length=255),
    )
    # ### end Alembic commands ###
