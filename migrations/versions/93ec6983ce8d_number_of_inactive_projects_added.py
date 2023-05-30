"""number_of_inactive_projects_added

Revision ID: 93ec6983ce8d
Revises: edde808b4556
Create Date: 2023-05-30 08:47:53.926692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '93ec6983ce8d'
down_revision = 'edde808b4556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reporting', sa.Column('inactive_project_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reporting', 'inactive_project_count')
    # ### end Alembic commands ###
