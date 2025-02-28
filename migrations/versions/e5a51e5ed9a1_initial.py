"""Initial

Revision ID: e5a51e5ed9a1
Revises: 
Create Date: 2022-02-18 08:43:54.527235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "e5a51e5ed9a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "units",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("external_display_name", sa.String(length=255), nullable=False),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("internal_ref", sa.String(length=50), nullable=False),
        sa.Column("safespring_endpoint", sa.String(length=255), nullable=False),
        sa.Column("safespring_name", sa.String(length=255), nullable=False),
        sa.Column("safespring_access", sa.String(length=255), nullable=False),
        sa.Column("safespring_secret", sa.String(length=255), nullable=False),
        sa.Column("days_in_available", sa.Integer(), nullable=False),
        sa.Column("counter", sa.Integer(), nullable=True),
        sa.Column("days_in_expired", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("internal_ref"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=50), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("_password_hash", sa.String(length=98), nullable=False),
        sa.Column("hotp_secret", sa.LargeBinary(length=20), nullable=False),
        sa.Column("hotp_counter", sa.BigInteger(), nullable=False),
        sa.Column("hotp_issue_time", sa.DateTime(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("kd_salt", sa.LargeBinary(length=32), nullable=True),
        sa.Column("nonce", sa.LargeBinary(length=12), nullable=True),
        sa.Column("public_key", sa.LargeBinary(length=300), nullable=True),
        sa.Column("private_key", sa.LargeBinary(length=300), nullable=True),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_table(
        "deletions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("requester_id", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("issued", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["requester_id"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "emails",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("primary", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "identifiers",
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("identifier", sa.String(length=58), nullable=False),
        sa.ForeignKeyConstraint(["username"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("username", "identifier"),
        sa.UniqueConstraint("identifier"),
    )
    op.create_table(
        "invites",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("nonce", sa.LargeBinary(length=12), nullable=True),
        sa.Column("public_key", sa.LargeBinary(length=300), nullable=True),
        sa.Column("private_key", sa.LargeBinary(length=300), nullable=True),
        sa.ForeignKeyConstraint(["unit_id"], ["units.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=255), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("pi", sa.String(length=255), nullable=True),
        sa.Column("bucket", sa.String(length=255), nullable=False),
        sa.Column("public_key", sa.LargeBinary(length=100), nullable=True),
        sa.Column("is_sensitive", sa.Boolean(), nullable=True),
        sa.Column("released", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.String(length=50), nullable=True),
        sa.Column("last_updated_by", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.username"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["last_updated_by"], ["users.username"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["unit_id"], ["units.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bucket"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index(op.f("ix_projects_is_active"), "projects", ["is_active"], unique=False)
    op.create_table(
        "researchusers",
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["username"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_table(
        "superadmins",
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["username"],
            ["users.username"],
        ),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_table(
        "unitusers",
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["unit_id"], ["units.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["username"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_table(
        "files",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("name_in_bucket", sa.Text(), nullable=False),
        sa.Column("subpath", sa.Text(), nullable=False),
        sa.Column("size_original", sa.BigInteger(), nullable=False),
        sa.Column("size_stored", sa.BigInteger(), nullable=False),
        sa.Column("compressed", sa.Boolean(), nullable=False),
        sa.Column("public_key", sa.String(length=64), nullable=False),
        sa.Column("salt", sa.String(length=32), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("time_latest_download", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_project_id"), "files", ["project_id"], unique=False)
    op.create_table(
        "projectinvitekeys",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("invite_id", sa.Integer(), nullable=False),
        sa.Column("key", sa.LargeBinary(length=300), nullable=False),
        sa.ForeignKeyConstraint(["invite_id"], ["invites.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "invite_id"),
        sa.UniqueConstraint("key"),
    )
    op.create_table(
        "projectinvites",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("invite_id", sa.Integer(), nullable=False),
        sa.Column("owner", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["invite_id"], ["invites.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "invite_id"),
    )
    op.create_table(
        "projectstatuses",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("is_aborted", sa.Boolean(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "status", "date_created"),
    )
    op.create_table(
        "projectuserkeys",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(length=50), nullable=False),
        sa.Column("key", sa.LargeBinary(length=300), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "user_id"),
        sa.UniqueConstraint("key"),
    )
    op.create_table(
        "projectusers",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(length=50), nullable=False),
        sa.Column("owner", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["researchusers.username"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "user_id"),
    )
    op.create_table(
        "versions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("active_file", sa.BigInteger(), nullable=True),
        sa.Column("size_stored", sa.BigInteger(), nullable=False),
        sa.Column("time_uploaded", sa.DateTime(), nullable=False),
        sa.Column("time_deleted", sa.DateTime(), nullable=True),
        sa.Column("time_invoiced", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["active_file"], ["files.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("versions")
    op.drop_table("projectusers")
    op.drop_table("projectuserkeys")
    op.drop_table("projectstatuses")
    op.drop_table("projectinvites")
    op.drop_table("projectinvitekeys")
    op.drop_index(op.f("ix_files_project_id"), table_name="files")
    op.drop_table("files")
    op.drop_table("unitusers")
    op.drop_table("superadmins")
    op.drop_table("researchusers")
    op.drop_index(op.f("ix_projects_is_active"), table_name="projects")
    op.drop_table("projects")
    op.drop_table("invites")
    op.drop_table("identifiers")
    op.drop_table("emails")
    op.drop_table("deletions")
    op.drop_table("users")
    op.drop_table("units")
    # ### end Alembic commands ###
