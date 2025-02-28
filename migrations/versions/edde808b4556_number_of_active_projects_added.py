"""number_of_active_projects_added

Revision ID: edde808b4556
Revises: e07c83ed0bda
Create Date: 2023-05-29 14:34:36.889601

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "edde808b4556"
down_revision = "e07c83ed0bda"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("reporting", sa.Column("active_project_count", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("reporting", "active_project_count")
    # ### end Alembic commands ###
