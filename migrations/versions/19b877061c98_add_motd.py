"""add_motd

Revision ID: 19b877061c98
Revises: 1256117ad629
Create Date: 2022-04-05 13:49:44.087517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "19b877061c98"
down_revision = "1256117ad629"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "motd",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("motd")
    # ### end Alembic commands ###
