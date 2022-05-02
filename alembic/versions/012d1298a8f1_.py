"""empty message

Revision ID: 012d1298a8f1
Revises: d3692e29f7eb
Create Date: 2022-05-01 22:50:16.587130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "012d1298a8f1"
down_revision = "d3692e29f7eb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("contacts_command_id_fkey", "contacts", type_="foreignkey")
    op.drop_constraint("contacts_email_type_id_fkey", "contacts", type_="foreignkey")
    op.drop_column("contacts", "command_id")
    op.drop_column("contacts", "email_type_id")
    op.add_column("email_types", sa.Column("command_id", sa.Integer(), nullable=True))
    op.add_column(
        "email_types", sa.Column("email_type_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(None, "email_types", "email_types", ["email_type_id"], ["id"])
    op.create_foreign_key(None, "email_types", "commands", ["command_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "email_types", type_="foreignkey")
    op.drop_constraint(None, "email_types", type_="foreignkey")
    op.drop_column("email_types", "email_type_id")
    op.drop_column("email_types", "command_id")
    op.add_column(
        "contacts",
        sa.Column("email_type_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "contacts",
        sa.Column("command_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "contacts_email_type_id_fkey",
        "contacts",
        "email_types",
        ["email_type_id"],
        ["id"],
    )
    op.create_foreign_key(
        "contacts_command_id_fkey", "contacts", "commands", ["command_id"], ["id"]
    )
    # ### end Alembic commands ###
